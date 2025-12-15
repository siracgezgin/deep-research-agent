"""
Research Orchestrator - Ana Koordinatör
=======================================

Tüm research workflow'unu yöneten ana sistem:
1. Planner ile plan oluştur
2. Her alt başlık için Researcher çalıştır (PARALEL)
3. Tüm bulguları Writer'a gönder (STREAMING)
4. Final raporu üret

Ayrıca:
- Progress tracking
- Error handling
- Retry mantığı
- Results caching
- Paralel araştırma (asyncio)
- Streaming report generation
"""

import os
import sys
import asyncio
from typing import Dict, List, Optional, AsyncGenerator
from datetime import datetime
import json
import time

# Proje root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agents.planner_agent import PlannerAgent
from src.agents.researcher_agent import ResearcherAgent
from src.agents.writer_agent import WriterAgent
from src.utils.config_loader import config as config_loader

# Config instance
config = config_loader.get_all()


class ResearchOrchestrator:
    """Tüm research sürecini koordine eder - Paralel + Streaming destekli"""
    
    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()
        self.config = config
        
        # Paralel request limiti (rate limit koruması)
        max_concurrent = config.get('performance', {}).get('max_concurrent_requests', 5)
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        self.current_state = {
            'stage': 'idle',  # idle, planning, researching, writing, done
            'progress': 0,  # 0-100
            'plan': None,
            'research_results': [],
            'report': None,
            'errors': []
        }
    
    async def run_research(
        self,
        topic: str,
        context: Optional[str] = None,
        progress_callback=None
    ) -> Dict:
        """
        Tam research workflow'unu çalıştır
        
        Args:
            topic: Araştırma konusu
            context: Ek bağlam (opsiyonel)
            progress_callback: Progress güncellemeleri için callback
        
        Returns:
            dict: {plan, research_results, report, metadata}
        """
        print("\n" + "="*70)
        print("🚀 DEEP RESEARCH BAŞLATILIYOR")
        print("="*70)
        print(f"📋 Konu: {topic}\n")
        
        start_time = datetime.now()
        
        try:
            # =================================================================
            # STAGE 1: PLANNING
            # =================================================================
            self._update_stage('planning', 10, progress_callback)
            print("📋 STAGE 1/3: Planlama...")
            
            plan = self.planner.create_plan(topic, context)
            self.current_state['plan'] = plan
            
            print(f"   ✅ Plan hazır: {len(plan['subtopics'])} alt başlık\n")
            
            # Planı validate et
            validation = self.planner.validate_plan(plan)
            if not validation['is_valid']:
                raise ValueError(f"Plan geçersiz: {validation['issues']}")
            
            # =================================================================
            # STAGE 2: RESEARCH (PARALEL)
            # =================================================================
            self._update_stage('researching', 20, progress_callback)
            print("🔍 STAGE 2/3: Araştırma (Paralel Mod)...")
            print(f"   {len(plan['subtopics'])} alt başlık araştırılacak...\n")
            
            # Paralel araştırma mı yoksa sequential mı?
            use_parallel = self.config.get('performance', {}).get('parallel_research', True)
            
            if use_parallel:
                research_results = await self._parallel_research(
                    plan['subtopics'], 
                    progress_callback
                )
            else:
                research_results = await self._sequential_research(
                    plan['subtopics'],
                    progress_callback
                )
            
            self.current_state['research_results'] = research_results
            print(f"   ✅ Araştırma tamamlandı: {len(research_results)} bölüm\n")
            
            # =================================================================
            # STAGE 3: WRITING
            # =================================================================
            self._update_stage('writing', 85, progress_callback)
            print("✍️  STAGE 3/3: Rapor yazımı...")
            
            # Writer agent artık dict döndürüyor (report + perspectives + quality)
            writer_output = self.writer.write_report(
                topic=topic,
                plan=plan,
                research_results=research_results,
                style="professional",
                include_perspectives=True
            )
            
            # State'e kaydet
            self.current_state['report'] = writer_output['report']
            self.current_state['perspectives'] = writer_output.get('perspectives')
            self.current_state['quality_metrics'] = writer_output.get('quality_metrics')
            
            print(f"   ✅ Rapor hazır ({len(writer_output['report']):,} karakter)")
            if writer_output.get('quality_metrics'):
                qm = writer_output['quality_metrics']
                print(f"   📊 Kalite: {qm['overall_score']}/100 ({qm['grade']})\n")
            
            # =================================================================
            # DONE
            # =================================================================
            self._update_stage('done', 100, progress_callback)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print("="*70)
            print("✅ RESEARCH TAMAMLANDI")
            print("="*70)
            print(f"⏱️  Süre: {duration:.1f} saniye")
            print(f"📊 Alt başlık: {len(plan['subtopics'])}")
            print(f"📝 Rapor: {len(writer_output['report']):,} karakter")
            
            if writer_output.get('quality_metrics'):
                qm = writer_output['quality_metrics']
                print(f"🎯 Kalite: {qm['overall_score']}/100 ({qm['grade']})")
            
            if writer_output.get('perspectives') and writer_output['perspectives'].get('has_conflict'):
                print(f"⚖️  Perspektifler: {len(writer_output['perspectives']['perspectives'])}")
            
            print(f"❌ Hata: {len(self.current_state['errors'])}\n")
            
            return {
                'success': True,
                'topic': topic,
                'plan': plan,
                'research_results': research_results,
                'report': writer_output['report'],
                'perspectives': writer_output.get('perspectives'),
                'quality_metrics': writer_output.get('quality_metrics'),
                'metadata': {
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'duration_seconds': duration,
                    'subtopics_count': len(plan['subtopics']),
                    'errors_count': len(self.current_state['errors']),
                    'errors': self.current_state['errors']
                }
            }
            
        except Exception as e:
            print(f"\n❌ FATAL ERROR: {e}\n")
            self.current_state['errors'].append({
                'stage': 'orchestrator',
                'error': str(e),
                'fatal': True
            })
            
            return {
                'success': False,
                'error': str(e),
                'partial_state': self.current_state
            }
    
    async def run_research_streaming(
        self,
        topic: str,
        context: Optional[str] = None,
        progress_callback=None
    ) -> AsyncGenerator[Dict, None]:
        """
        Streaming research workflow - her güncellemeyi anında yield et
        
        Args:
            topic: Araştırma konusu
            context: Ek bağlam
            progress_callback: Progress callback
            
        Yields:
            dict: {
                'stage': 'planning' | 'researching' | 'writing' | 'done',
                'type': 'status' | 'plan' | 'research' | 'report_chunk' | 'quality' | 'final',
                'data': Any (stage'e göre)
            }
        """
        start_time = datetime.now()
        
        try:
            # STAGE 1: PLANNING
            yield {
                'stage': 'planning',
                'type': 'status',
                'data': {'message': '📋 Plan oluşturuluyor...', 'progress': 10}
            }
            
            plan = self.planner.create_plan(topic, context)
            self.current_state['plan'] = plan
            
            yield {
                'stage': 'planning',
                'type': 'plan',
                'data': {
                    'plan': plan,
                    'subtopics_count': len(plan['subtopics']),
                    'message': f"✅ Plan hazır: {len(plan['subtopics'])} alt başlık"
                }
            }
            
            # Plan validation
            validation = self.planner.validate_plan(plan)
            if not validation['is_valid']:
                raise ValueError(f"Plan geçersiz: {validation['issues']}")
            
            # STAGE 2: RESEARCH (PARALLEL)
            yield {
                'stage': 'researching',
                'type': 'status',
                'data': {
                    'message': f'🔍 Araştırma başlıyor ({len(plan["subtopics"])} alt başlık)...',
                    'progress': 20
                }
            }
            
            use_parallel = self.config.get('performance', {}).get('parallel_research', True)
            
            if use_parallel:
                research_results = await self._parallel_research(plan['subtopics'], progress_callback)
            else:
                research_results = await self._sequential_research(plan['subtopics'], progress_callback)
            
            self.current_state['research_results'] = research_results
            
            yield {
                'stage': 'researching',
                'type': 'research',
                'data': {
                    'research_results': research_results,
                    'message': f'✅ Araştırma tamamlandı: {len(research_results)} bölüm',
                    'progress': 80
                }
            }
            
            # STAGE 3: WRITING (STREAMING)
            yield {
                'stage': 'writing',
                'type': 'status',
                'data': {
                    'message': '✍️ Rapor yazılıyor (streaming)...',
                    'progress': 85
                }
            }
            
            # Writer'ın streaming modunu kullan
            full_report = ""
            perspectives = None
            quality_metrics = None
            
            for chunk in self.writer.write_report_streaming(
                topic=topic,
                plan=plan,
                research_results=research_results,
                style="professional",
                include_perspectives=True
            ):
                # Metin chunk'larını topla
                if chunk['type'] in ['metadata', 'intro', 'section', 'conclusion']:
                    full_report += chunk['content']
                
                # Perspektif sonuçlarını sakla
                if chunk['type'] == 'quality':
                    quality_metrics = chunk['content']
                
                # Her chunk'ı yield et
                yield {
                    'stage': 'writing',
                    'type': 'report_chunk',
                    'data': chunk
                }
            
            self.current_state['report'] = full_report
            self.current_state['quality_metrics'] = quality_metrics
            
            # DONE
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            yield {
                'stage': 'done',
                'type': 'final',
                'data': {
                    'success': True,
                    'topic': topic,
                    'plan': plan,
                    'research_results': research_results,
                    'report': full_report,
                    'quality_metrics': quality_metrics,
                    'metadata': {
                        'start_time': start_time.isoformat(),
                        'end_time': end_time.isoformat(),
                        'duration_seconds': duration,
                        'subtopics_count': len(plan['subtopics']),
                        'errors_count': len(self.current_state['errors'])
                    },
                    'message': f'✅ Tamamlandı! Süre: {duration:.1f}s'
                }
            }
            
        except Exception as e:
            self.current_state['errors'].append({
                'stage': 'orchestrator_streaming',
                'error': str(e),
                'fatal': True
            })
            
            yield {
                'stage': 'error',
                'type': 'error',
                'data': {
                    'success': False,
                    'error': str(e),
                    'state': self.current_state
                }
            }
    
    def _update_stage(self, stage: str, progress: int, callback=None):
        """İç kullanım: stage ve progress güncelle"""
        self.current_state['stage'] = stage
        self.current_state['progress'] = progress
        
        if callback:
            callback(stage, progress)
    
    def get_state(self) -> Dict:
        """Mevcut durumu döndür"""
        return self.current_state.copy()
    
    def save_results(self, results: Dict, output_dir: str = "output"):
        """Sonuçları dosyalara kaydet (perspectives + quality metrics dahil)"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"research_{timestamp}"
        
        # 1. Rapor (Markdown)
        report_file = os.path.join(output_dir, f"{base_name}_report.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(results['report'])
        
        # 2. Plan (JSON)
        plan_file = os.path.join(output_dir, f"{base_name}_plan.json")
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(results['plan'], f, indent=2, ensure_ascii=False)
        
        # 3. Research Results (JSON)
        research_file = os.path.join(output_dir, f"{base_name}_research.json")
        with open(research_file, 'w', encoding='utf-8') as f:
            json.dump(results['research_results'], f, indent=2, ensure_ascii=False)
        
        # 4. Quality Metrics (JSON) - YENİ
        if results.get('quality_metrics'):
            quality_file = os.path.join(output_dir, f"{base_name}_quality.json")
            with open(quality_file, 'w', encoding='utf-8') as f:
                json.dump(results['quality_metrics'], f, indent=2, ensure_ascii=False)
        
        # 5. Perspectives (JSON) - YENİ
        if results.get('perspectives'):
            perspectives_file = os.path.join(output_dir, f"{base_name}_perspectives.json")
            with open(perspectives_file, 'w', encoding='utf-8') as f:
                json.dump(results['perspectives'], f, indent=2, ensure_ascii=False)
        
        # 6. Metadata (JSON)
        meta_file = os.path.join(output_dir, f"{base_name}_metadata.json")
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(results['metadata'], f, indent=2, ensure_ascii=False)
        
        print(f"💾 Sonuçlar kaydedildi:")
        print(f"   📄 Rapor: {report_file}")
        print(f"   📋 Plan: {plan_file}")
        print(f"   🔍 Araştırma: {research_file}")
        
        if results.get('quality_metrics'):
            print(f"   📊 Kalite: {quality_file}")
        if results.get('perspectives'):
            print(f"   ⚖️  Perspektifler: {perspectives_file}")
        
        print(f"   ℹ️  Metadata: {meta_file}\n")
        
        return {
            'report': report_file,
            'plan': plan_file,
            'research': research_file,
            'quality': quality_file if results.get('quality_metrics') else None,
            'perspectives': perspectives_file if results.get('perspectives') else None,
            'metadata': meta_file
        }
    
    # =========================================================================
    # HELPER METHODS - PARALEL RESEARCH
    # =========================================================================
    
    async def _parallel_research(
        self,
        subtopics: List[Dict],
        progress_callback=None
    ) -> List[Dict]:
        """
        Paralel araştırma - Tüm subtopic'leri aynı anda araştır
        Rate limit koruması ile (semaphore)
        """
        print("   🚀 Paralel mod aktif (max 5 concurrent request)")
        
        # Her subtopic için task oluştur
        tasks = []
        for i, subtopic in enumerate(subtopics, 1):
            task = self._research_single_subtopic(
                subtopic=subtopic,
                index=i,
                total=len(subtopics),
                progress_callback=progress_callback
            )
            tasks.append(task)
        
        # Paralel çalıştır (gather all)
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        duration = time.time() - start_time
        
        print(f"\n   ⚡ Paralel araştırma tamamlandı: {duration:.1f} saniye")
        
        # Exception'ları handle et
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"   ❌ Subtopic {i+1} başarısız: {result}")
                # Fallback result
                valid_results.append({
                    'topic': subtopics[i]['question'],
                    'subtopic_title': subtopics[i]['title'],
                    'error': str(result),
                    'key_findings': [],
                    'summary': f"Bu bölüm için araştırma başarısız oldu: {result}",
                    'confidence': 0
                })
            else:
                valid_results.append(result)
        
        return valid_results
    
    async def _sequential_research(
        self,
        subtopics: List[Dict],
        progress_callback=None
    ) -> List[Dict]:
        """
        Sequential araştırma - Eski metod (fallback)
        """
        print("   📝 Sequential mod (yavaş ama güvenli)")
        
        research_results = []
        total_subtopics = len(subtopics)
        
        for i, subtopic in enumerate(subtopics, 1):
            print(f"   [{i}/{total_subtopics}] {subtopic['title']}")
            
            # Progress güncelle
            progress = 20 + (60 * i / total_subtopics)  # 20-80 arası
            self._update_stage('researching', progress, progress_callback)
            
            try:
                result = await self.researcher.research_topic(
                    topic=subtopic['question'],
                    max_sources=5,
                    scrape_content=False
                )
                
                result['subtopic_title'] = subtopic['title']
                research_results.append(result)
                
                print(f"   ✅ Tamamlandı (güven: {result.get('confidence', 0)}/5)\n")
                
            except Exception as e:
                print(f"   ❌ Hata: {e}\n")
                self.current_state['errors'].append({
                    'stage': 'research',
                    'subtopic': subtopic['title'],
                    'error': str(e)
                })
                
                research_results.append({
                    'topic': subtopic['question'],
                    'error': str(e),
                    'key_findings': [],
                    'summary': f"Bu bölüm için araştırma başarısız oldu: {e}",
                    'confidence': 0
                })
            
            # Rate limiting
            if i < total_subtopics:
                print(f"   ⏳ Rate limit için 15 saniye bekleniyor...")
                await asyncio.sleep(15)
        
        return research_results
    
    async def _research_single_subtopic(
        self,
        subtopic: Dict,
        index: int,
        total: int,
        progress_callback=None
    ) -> Dict:
        """
        Tek bir subtopic'i araştır (rate limit korumalı)
        """
        async with self.semaphore:  # Rate limit koruması
            print(f"   [{index}/{total}] Başlatılıyor: {subtopic['title'][:50]}...")
            
            try:
                result = await self.researcher.research_topic(
                    topic=subtopic['question'],
                    max_sources=5,
                    scrape_content=False
                )
                
                result['subtopic_title'] = subtopic['title']
                
                print(f"   [{index}/{total}] ✅ Tamamlandı (güven: {result.get('confidence', 0)}/5)")
                
                # Progress güncelle (yaklaşık)
                progress = 20 + (60 * index / total)
                self._update_stage('researching', progress, progress_callback)
                
                return result
                
            except Exception as e:
                print(f"   [{index}/{total}] ❌ Hata: {e}")
                raise  # asyncio.gather exception olarak handle edecek


# =============================================================================
# TEST
# =============================================================================

async def test_orchestrator():
    print("\n" + "#"*70)
    print("🧪 ORCHESTRATOR TEST")
    print("#"*70 + "\n")
    
    # Progress callback
    def on_progress(stage, progress):
        bar_length = 30
        filled = int(bar_length * progress / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r   [{bar}] {progress}% - {stage}", end='', flush=True)
    
    # Orchestrator oluştur
    orchestrator = ResearchOrchestrator()
    
    # Test konusu
    topic = "Kuantum hesaplama ve yapay zeka"
    
    # Research çalıştır
    results = await orchestrator.run_research(
        topic=topic,
        context="Geleceğe odaklanarak, pratik uygulamalar dahil",
        progress_callback=on_progress
    )
    
    print("\n")  # Progress bar'dan sonra yeni satır
    
    if results['success']:
        # Sonuçları kaydet
        files = orchestrator.save_results(results, output_dir="output")
        
        print("\n" + "="*70)
        print("✅ TEST BAŞARILI")
        print("="*70 + "\n")
    else:
        print(f"\n❌ Test başarısız: {results.get('error')}\n")


if __name__ == "__main__":
    asyncio.run(test_orchestrator())
