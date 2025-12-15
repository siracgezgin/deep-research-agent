"""
Writer Agent - Rapor Yazarı
===========================

Görev: Araştırma bulgularını profesyonel rapora dönüştür

Çıktı:
- Markdown formatında rapor
- Executive summary
- Detaylı bölümler
- Kaynakça
- Görselleştirme önerileri
"""

import os
import sys
import time
from typing import List, Dict, Generator, Optional
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Proje utils'leri
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.perspective_analyzer import PerspectiveAnalyzer
from src.utils.quality_metrics import QualityMetrics
from src.utils.logger import logger, log_agent_action

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


class WriterAgent:
    """Araştırma raporu yazan ajan"""
    
    def __init__(self, model_name='gemini-2.5-flash'):
        self.model_name = model_name
        
        system_instruction = """Sen bir profesyonel rapor yazarısısın.

GÖREV:
Araştırma bulgularını kapsamlı, akıcı ve profesyonel bir rapora dönüştür.

RAPOR YAPISI:
1. Başlık ve metadata
2. Executive Summary (yönetici özeti)
3. Giriş
4. Ana bölümler (her alt başlık için)
5. Sonuç ve öneriler
6. Kaynakça

YAZIM KURALLARI:
- Akademik ama anlaşılır dil
- Pasif yapılardan kaçın
- Bulgular arasında bağlantı kurun
- Önemli noktaları vurgulayın
- Markdown formatı kullanın
- Her iddiayı kaynak ile destekleyin

FORMAT:
Markdown (.md) formatında profesyonel rapor.
"""
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_instruction,
            generation_config={
                "temperature": 0.7,  # Akıcı yazım için
                "max_output_tokens": 8000  # Uzun rapor için
            }
        )
    
    def write_report(
        self,
        topic: str,
        plan: Dict,
        research_results: List[Dict],
        style: str = "professional",
        include_perspectives: bool = True
    ) -> Dict:
        """
        Tam rapor yaz (perspective analysis ile)
        
        Args:
            topic: Ana konu
            plan: Planner'dan gelen plan (subtopics)
            research_results: Her subtopic için research sonuçları
            style: "professional", "academic", "casual"
            include_perspectives: Perspektif analizi dahil et mi?
        
        Returns:
            dict: {
                'report': str (Markdown raporu),
                'perspectives': dict (perspektif analizi),
                'quality_metrics': dict (kalite metrikleri)
            }
        """
        print(f"\n✍️  Rapor yazılıyor: {topic}")
        print(f"   📊 {len(research_results)} bölüm işlenecek...")
        
        log_agent_action("WriterAgent", "write_report_start", {"topic": topic[:50]})
        
        # 1. Perspektif analizi yap (varsa)
        perspectives = None
        if include_perspectives:
            try:
                print("   🔍 Perspektif analizi yapılıyor...")
                analyzer = PerspectiveAnalyzer()
                perspectives = analyzer.analyze_perspectives(topic, research_results)
                print(f"   ✅ {len(perspectives.get('perspectives', []))} perspektif bulundu")
            except Exception as e:
                logger.warning(f"Perspektif analizi başarısız: {e}")
                perspectives = None
        
        # 2. Ana raporu bölümler halinde yaz
        print("   🤖 LLM rapor yazıyor (bölümler halinde)...")
        
        # Giriş ve özet
        intro_prompt = self._build_intro_prompt(topic, plan, research_results, perspectives)
        intro_response = self.model.generate_content(intro_prompt)
        time.sleep(13)
        intro_section = intro_response.text
        
        # Her alt başlık için bölüm yaz
        sections = []
        for i, result in enumerate(research_results):
            print(f"   📝 Bölüm {i+1}/{len(research_results)} yazılıyor...")
            section_prompt = self._build_section_prompt(
                topic=topic,
                subtopic=result.get('subtopic', f'Bölüm {i+1}'),
                research_data=result,
                section_number=i+1
            )
            section_response = self.model.generate_content(section_prompt)
            time.sleep(13)
            sections.append(section_response.text)
        
        # Sonuç bölümü
        conclusion_prompt = self._build_conclusion_prompt(topic, research_results, perspectives)
        conclusion_response = self.model.generate_content(conclusion_prompt)
        time.sleep(13)
        conclusion_section = conclusion_response.text
        
        # Tüm bölümleri birleştir
        report = intro_section + "\n\n" + "\n\n".join(sections) + "\n\n" + conclusion_section
        
        # Metadata ekle
        report = self._add_metadata(report, topic)
        
        # 3. Kalite metrikleri hesapla
        print("   📊 Kalite metrikleri hesaplanıyor...")
        quality_calculator = QualityMetrics()
        
        # Tüm kaynakları topla
        all_sources = []
        for result in research_results:
            if 'scored_sources' in result:
                all_sources.extend(result['scored_sources'])
        
        quality_metrics = quality_calculator.calculate_report_quality(
            sources=all_sources,
            research_results=research_results,
            report=report,
            topic=topic
        )
        
        log_agent_action("WriterAgent", "write_report_complete", {
            "report_length": len(report),
            "quality_score": quality_metrics['overall_score']
        })
        
        print(f"   ✅ Rapor hazır! ({len(report):,} karakter)")
        print(f"   📊 Kalite Skoru: {quality_metrics['overall_score']}/100 ({quality_metrics['grade']})\n")
        
        return {
            'report': report,
            'perspectives': perspectives,
            'quality_metrics': quality_metrics
        }
    
    def write_report_streaming(
        self,
        topic: str,
        plan: Dict,
        research_results: List[Dict],
        style: str = "professional",
        include_perspectives: bool = True
    ) -> Generator[Dict, None, None]:
        """
        Streaming rapor yaz - her chunk'ı anında döndür
        
        Args:
            topic: Ana konu
            plan: Planner'dan gelen plan
            research_results: Araştırma sonuçları
            style: Yazım stili
            include_perspectives: Perspektif analizi dahil et
            
        Yields:
            dict: {
                'type': 'metadata' | 'intro' | 'section' | 'conclusion' | 'quality',
                'content': str (metin chunk'ı),
                'section_number': int (optional),
                'section_title': str (optional)
            }
        """
        log_agent_action("WriterAgent", "write_report_streaming_start", {"topic": topic[:50]})
        
        # 1. Metadata yield et
        yield {
            'type': 'metadata',
            'content': f"# {topic}\n\n*Oluşturulma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}*\n\n",
            'timestamp': time.time()
        }
        
        # 2. Perspektif analizi (eğer istenmişse)
        perspectives = None
        if include_perspectives:
            try:
                yield {
                    'type': 'status',
                    'content': '🔍 Perspektif analizi yapılıyor...',
                    'timestamp': time.time()
                }
                analyzer = PerspectiveAnalyzer()
                perspectives = analyzer.analyze_perspectives(topic, research_results)
                yield {
                    'type': 'status',
                    'content': f'✅ {len(perspectives.get("perspectives", []))} perspektif bulundu',
                    'timestamp': time.time()
                }
            except Exception as e:
                logger.warning(f"Perspektif analizi başarısız: {e}")
                perspectives = None
        
        # 3. Giriş ve özet - STREAMING
        yield {
            'type': 'status',
            'content': '📝 Giriş bölümü yazılıyor...',
            'timestamp': time.time()
        }
        
        intro_prompt = self._build_intro_prompt(topic, plan, research_results, perspectives)
        intro_chunks = self.model.generate_content(intro_prompt, stream=True)
        
        for chunk in intro_chunks:
            if chunk.text:
                yield {
                    'type': 'intro',
                    'content': chunk.text,
                    'timestamp': time.time()
                }
        
        yield {
            'type': 'intro',
            'content': '\n\n',
            'timestamp': time.time()
        }
        
        # Rate limit delay
        time.sleep(13)
        
        # 4. Her bölüm için - STREAMING
        for i, result in enumerate(research_results):
            section_title = result.get('subtopic', f'Bölüm {i+1}')
            
            yield {
                'type': 'status',
                'content': f'📝 Bölüm {i+1}/{len(research_results)}: {section_title}',
                'timestamp': time.time()
            }
            
            section_prompt = self._build_section_prompt(
                topic=topic,
                subtopic=section_title,
                research_data=result,
                section_number=i+1
            )
            
            section_chunks = self.model.generate_content(section_prompt, stream=True)
            
            for chunk in section_chunks:
                if chunk.text:
                    yield {
                        'type': 'section',
                        'content': chunk.text,
                        'section_number': i+1,
                        'section_title': section_title,
                        'timestamp': time.time()
                    }
            
            yield {
                'type': 'section',
                'content': '\n\n',
                'section_number': i+1,
                'section_title': section_title,
                'timestamp': time.time()
            }
            
            # Rate limit delay
            time.sleep(13)
        
        # 5. Sonuç bölümü - STREAMING
        yield {
            'type': 'status',
            'content': '📝 Sonuç bölümü yazılıyor...',
            'timestamp': time.time()
        }
        
        conclusion_prompt = self._build_conclusion_prompt(topic, research_results, perspectives)
        conclusion_chunks = self.model.generate_content(conclusion_prompt, stream=True)
        
        for chunk in conclusion_chunks:
            if chunk.text:
                yield {
                    'type': 'conclusion',
                    'content': chunk.text,
                    'timestamp': time.time()
                }
        
        # 6. Kalite metrikleri hesapla
        yield {
            'type': 'status',
            'content': '📊 Kalite metrikleri hesaplanıyor...',
            'timestamp': time.time()
        }
        
        quality_calculator = QualityMetrics()
        all_sources = []
        for result in research_results:
            if 'scored_sources' in result:
                all_sources.extend(result['scored_sources'])
        
        # Not: Full report text'e ihtiyacımız var, bu yüzden kalite metriği basitleştirilmiş
        quality_metrics = quality_calculator.calculate_report_quality(
            sources=all_sources,
            research_results=research_results,
            report="",  # Streaming sırasında tam rapor yok
            topic=topic
        )
        
        yield {
            'type': 'quality',
            'content': quality_metrics,
            'timestamp': time.time()
        }
        
        log_agent_action("WriterAgent", "write_report_streaming_complete", {
            "quality_score": quality_metrics['overall_score']
        })
    
    
    def _build_intro_prompt(self, topic: str, plan: Dict, research_results: List[Dict], perspectives: Dict = None) -> str:
        """Giriş ve özet bölümü için prompt"""
        
        prompt = f"""SEN BİR UZMAN ARAŞTIRMA RAPORU YAZICISISIN.

GÖREV: "{topic}" konusunda profesyonel bir araştırma raporunun GİRİŞ VE YÖNETİCİ ÖZETİ bölümlerini yaz.

Plan ({len(plan.get('subtopics', []))} alt başlık):
"""
        for i, subtopic in enumerate(plan.get('subtopics', []), 1):
            prompt += f"\n{i}. {subtopic['title']}"
        
        if perspectives and perspectives.get('has_conflict'):
            prompt += f"\n\n⚠️ Bu konuda {len(perspectives.get('perspectives', []))} farklı perspektif tespit edildi."
        
        prompt += f"""

YAZILACAKLAR:

1. BAŞLIK
   - Çarpıcı, bilgilendirici başlık

2. YÖNETİCİ ÖZETİ (Executive Summary)
   - Tüm araştırmayı özetleyen 1-2 paragraf
   - Temel bulgular ve sonuçlar

3. GİRİŞ
   - Konunun önemi
   - Araştırma kapsamı
   - Metodoloji
   - Raporun yapısı

Markdown formatında yaz. Doğrudan içeriğe başla, açıklama yapma.
"""
        return prompt
    
    def _build_section_prompt(self, topic: str, subtopic: str, research_data: Dict, section_number: int) -> str:
        """Tek bir alt başlık bölümü için prompt"""
        
        prompt = f"""SEN BİR UZMAN ARAŞTIRMA RAPORU YAZICISISIN.

ANA KONU: {topic}
ALT BAŞLIK: {subtopic}
BÖLÜM NUMARASI: {section_number}

ARAŞTIRMA BULGULARI:
"""
        
        # Ana bulgular
        if 'key_findings' in research_data:
            prompt += "\nAna Bulgular:\n"
            for finding in research_data['key_findings']:
                prompt += f"- {finding}\n"
        
        # Özet
        if 'summary' in research_data:
            prompt += f"\nÖzet: {research_data['summary']}\n"
        
        # Güven skoru
        if 'confidence_score' in research_data:
            prompt += f"\nGüven Skoru: {research_data['confidence_score']}/5\n"
        
        prompt += """

YAZIM TALİMATI:

Bu bölüm için kapsamlı, detaylı bir açıklama yaz:

- Başlık olarak "## {section_number}. {subtopic}" kullan
- Alt başlıklar ekle (###)
- Bulgulara dayanarak derinlemesine analiz yap
- Örnekler, sayısal veriler, karşılaştırmalar ekle
- 3-5 paragraf uzunluğunda olsun
- Akademik ama anlaşılır dil kullan

Markdown formatında yaz. Doğrudan başlıkla başla, açıklama yapma.
"""
        return prompt
    
    def _build_conclusion_prompt(self, topic: str, research_results: List[Dict], perspectives: Dict = None) -> str:
        """Sonuç bölümü için prompt"""
        
        prompt = f"""SEN BİR UZMAN ARAŞTIRMA RAPORU YAZICISISIN.

ANA KONU: {topic}

ARAŞTIRMA ÖZETİ:
{len(research_results)} farklı alt başlık incelendi.
"""
        
        if perspectives and perspectives.get('has_conflict'):
            prompt += f"\n{len(perspectives.get('perspectives', []))} farklı perspektif tespit edildi."
            if perspectives.get('conflicts'):
                prompt += f"\n{len(perspectives['conflicts'])} önemli çelişki bulundu."
        
        prompt += """

YAZIM TALİMATI:

SONUÇ bölümünü yaz:

## 6. Sonuç

- Temel çıkarımlar
- Ana bulgular özeti
- Öneriler (uygulanabilir)
- Gelecek perspektifi
- 2-3 paragraf

Tüm bölümleri kapsayan, tutarlı bir sonuç yaz.

Markdown formatında yaz. Doğrudan başlıkla başla, açıklama yapma. 
ÖNEMLİ: Cümleyi yarım bırakma, tam bitir!
"""
        return prompt
    
    def _build_report_prompt(
        self,
        topic: str,
        plan: Dict,
        research_results: List[Dict],
        style: str,
        perspectives: Dict = None
    ) -> str:
        """Rapor yazma prompt'u oluştur (perspectives dahil)"""
        
        prompt = f"""RAPOR YAZMA GÖREVİ

Ana Konu: {topic}
Stil: {style}

Plan:
"""
        
        # Plan bilgisi
        for i, subtopic in enumerate(plan.get('subtopics', []), 1):
            prompt += f"\n{i}. {subtopic['title']}"
            prompt += f"\n   Soru: {subtopic['question']}"
        
        # Araştırma sonuçları
        prompt += "\n\nAraştırma Bulguları:\n"
        
        for i, result in enumerate(research_results, 1):
            prompt += f"\n--- Bölüm {i} ---\n"
            prompt += f"Konu: {result.get('topic', 'N/A')}\n"
            
            # Ana bulgular
            if 'key_findings' in result:
                prompt += "Bulgular:\n"
                for finding in result['key_findings']:
                    prompt += f"- {finding}\n"
            
            # Özet
            if 'summary' in result:
                prompt += f"\nÖzet: {result['summary'][:500]}...\n"
        
        # Perspektif analizi varsa ekle
        if perspectives and perspectives.get('has_conflict'):
            prompt += "\n\nPERSPEKTİF ANALİZİ:\n"
            prompt += f"Bu konuda {len(perspectives.get('perspectives', []))} farklı perspektif tespit edildi.\n\n"
            
            for p in perspectives.get('perspectives', []):
                prompt += f"- {p['label'].upper()}: {p['summary'][:200]}\n"
            
            if perspectives.get('conflicts'):
                prompt += f"\n⚠️  {len(perspectives['conflicts'])} çelişki tespit edildi. Raporda bunları dengeli şekilde ele al.\n"
        
        # Yazım talimatları
        prompt += """

YAZIM TALİMATLARI:

1. BAŞLIK ve METAData:
   - Çarpıcı bir başlık
   - Tarih, yazar (AI Research Agent), konu

2. EXECUTIVE SUMMARY:
   - 1 paragraf, tüm raporu özetleyen
   - Temel bulgular ve sonuçlar

3. GİRİŞ:
   - Konunun önemi
   - Araştırma kapsamı
   - Metodoloji (web araştırması, kaynak analizi)

4. ANA BÖLÜMLER:
   - Her alt başlık için bir bölüm
   - Her bölümde: bulgular, analiz, yorumlar
   - Başlıklar: ##, ###, #### kullan
   - ÖNEMLİ: Eğer çelişkili görüşler varsa, her iki perspektifi de dengeli şekilde sun

5. SONUÇ:
   - Temel çıkarımlar
   - Öneriler
   - Gelecek perspektifi

6. KAYNAKÇA:
   - Kullanılan kaynakların listesi

Markdown formatında profesyonel rapor yaz. ÇOK ÖNEMLİ: Doğrudan rapora başla, 
"İşte rapor:" gibi giriş yapma.
"""
        
        return prompt
    
    def _add_metadata(self, report: str, topic: str) -> str:
        """Rapora metadata ekle"""
        
        now = datetime.now()
        
        metadata = f"""# {topic}

**Yazar:** AI Deep Research Agent  
**Tarih:** {now.strftime('%d %B %Y')}  
**Oluşturma:** {now.strftime('%d.%m.%Y %H:%M')}

---

"""
        
        return metadata + report
    
    def write_executive_summary(self, report: str) -> str:
        """Rapor için executive summary yaz (ayrı)"""
        
        prompt = f"""Bu rapordan kısa bir yönetici özeti (executive summary) çıkar.

Rapor:
{report[:5000]}  # İlk 5000 karakter

Özet:
- 150-200 kelime
- Temel bulgular
- Ana sonuçlar
- Aksiyon önerileri

Sadece özeti yaz, başka açıklama ekleme.
"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def improve_section(self, section: str, feedback: str) -> str:
        """Raporun bir bölümünü iyileştir"""
        
        prompt = f"""Bu rapor bölümünü iyileştir:

Mevcut Bölüm:
{section}

Geri Bildirim:
{feedback}

İyileştirilmiş bölümü yaz (sadece bölüm, başka açıklama yok).
"""
        
        response = self.model.generate_content(prompt)
        return response.text


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 WRITER AGENT TEST")
    print("="*70 + "\n")
    
    # Agent oluştur
    writer = WriterAgent()
    
    # Mock data
    topic = "Yapay Zeka Etiği ve Toplumsal Etkiler"
    
    plan = {
        'topic': topic,
        'description': 'AI etik ve toplum üzerindeki etkilerini araştırma',
        'subtopics': [
            {
                'title': 'Yapay Zeka Etiğinin Temelleri',
                'question': 'AI etiği nedir ve neden önemlidir?',
                'source_type': 'web',
                'priority': 5
            },
            {
                'title': 'Güncel Etik Sorunlar',
                'question': 'Bugün karşılaştığımız başlıca AI etik sorunları nelerdir?',
                'source_type': 'news',
                'priority': 5
            },
            {
                'title': 'Toplumsal Etkiler',
                'question': 'AI toplumu nasıl etkiliyor?',
                'source_type': 'academic',
                'priority': 4
            }
        ]
    }
    
    research_results = [
        {
            'topic': 'Yapay Zeka Etiğinin Temelleri',
            'key_findings': [
                'AI etiği, adalet, şeffaflık ve hesap verebilirlik prensipleri üzerine kuruludur',
                'Bias ve ayrımcılık temel endişelerdir',
                'Düzenleyici çerçeveler hala gelişmekte'
            ],
            'summary': 'AI etiği, yapay zeka sistemlerinin geliştirilmesi ve kullanımında ahlaki ilkelerin uygulanmasını içerir. Temel prensipler arasında adalet, şeffaflık, hesap verebilirlik ve gizlilik yer alır.',
            'confidence': 4
        },
        {
            'topic': 'Güncel Etik Sorunlar',
            'key_findings': [
                'Deepfake teknolojisi bilgi kirliliğine yol açıyor',
                'İş piyasası otomasyon nedeniyle dönüşüyor',
                'Gözetim teknolojileri gizlilik endişelerini artırıyor'
            ],
            'summary': 'Günümüzde AI ile ilgili başlıca etik sorunlar deepfake, iş kaybı, gözetim ve bias içerir.',
            'confidence': 5
        },
        {
            'topic': 'Toplumsal Etkiler',
            'key_findings': [
                'AI eğitim ve sağlık alanlarında fırsatlar sunuyor',
                'Dijital uçurum toplumsal eşitsizliği artırabilir',
                'Demokratik süreçler AI manipülasyonuna açık'
            ],
            'summary': 'AI toplum üzerinde hem olumlu hem olumsuz etkiler yaratmaktadır.',
            'confidence': 4
        }
    ]
    
    # Rapor yaz
    print(f"📝 Test: {topic}\n")
    
    report = writer.write_report(
        topic=topic,
        plan=plan,
        research_results=research_results,
        style="professional"
    )
    
    # Rapora kaydet
    output_file = "examples/output_writer_report.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"💾 Rapor kaydedildi: {output_file}")
    print(f"📏 Uzunluk: {len(report):,} karakter\n")
    
    # İlk 500 karakteri göster
    print("="*70)
    print("📄 RAPOR ÖNİZLEMESİ (İlk 500 karakter)")
    print("="*70 + "\n")
    print(report[:500] + "...")
    
    print("\n" + "="*70)
    print("✅ TEST TAMAMLANDI")
    print("="*70 + "\n")
