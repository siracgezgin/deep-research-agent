"""
Researcher Agent - Web Araştırmacısı
====================================

Görev: Verilen konuyu web'de araştır, kaynak topla, analiz et

Yetenekler:
- Web search (Tavily)
- Web scraping (Crawl4AI)
- İçerik analizi (Gemini)
- Multi-source sentez
"""

import os
import sys
import asyncio
import time
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai
from crawl4ai import AsyncWebCrawler

# Proje root'unu path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.tools.web_tools import search_web_simple
from src.utils.source_scorer import SourceScorer
from src.utils.logger import logger, log_agent_action

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


class ResearcherAgent:
    """Web araştırması yapan ajan"""
    
    def __init__(self, model_name='gemini-2.5-flash'):
        self.model_name = model_name
        
        system_instruction = """Sen bir uzman araştırmacısın.

GÖREV:
Verilen konuyu araştır, güvenilir kaynaklar bul, içerikleri analiz et.

YETENEKLERİN:
1. Web'de arama yap (search tool)
2. URL'lerden içerik çek (scraping)
3. İçerikleri özetle ve sentezle
4. Çelişkileri/farklı görüşleri belirle

ÇIKTI FORMATI:
{
  "topic": "Araştırılan konu",
  "sources": [
    {"url": "...", "title": "...", "summary": "..."}
  ],
  "key_findings": ["Bulgu 1", "Bulgu 2", ...],
  "summary": "Genel özet",
  "confidence": 1-5
}

JSON formatında yanıt ver.
"""
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            tools=[search_web_simple],  # Web search tool
            system_instruction=system_instruction
        )
    
    async def research_topic(
        self,
        topic: str,
        max_sources: int = 5,
        scrape_content: bool = True
    ) -> Dict:
        """
        Konuyu araştır
        
        Args:
            topic: Araştırılacak konu
            max_sources: Maksimum kaynak sayısı
            scrape_content: URL içeriklerini scrape et mi?
        
        Returns:
            dict: Araştırma sonuçları (source scores dahil)
        """
        print(f"\n🔍 Araştırma başlıyor: {topic}")
        log_agent_action("ResearcherAgent", "research_start", {"topic": topic[:50]})
        
        # Source scorer başlat
        scorer = SourceScorer()
        
        # 1. Web search yap (LLM tool kullanır)
        chat = self.model.start_chat(enable_automatic_function_calling=True)
        
        search_prompt = f"""Bu konuyu web'de ara ve ilgili kaynakları bul: {topic}

En fazla {max_sources} kaynak kullan."""
        
        print("   📡 Web search...")
        response = chat.send_message(search_prompt)
        
        # LLM'in bulduğu kaynakları içeren yanıtı al
        initial_findings = response.text
        
        # Search'ten gelen kaynakları al ve skorla
        search_results = search_web_simple(topic, max_sources)
        scored_sources = scorer.score_multiple_sources(search_results)
        
        print(f"   ✅ İlk bulgular toplandı ({len(scored_sources)} kaynak)")
        
        # Rate limit: 5 req/min = 12 saniye arası gerekli
        time.sleep(13)
        
        # 2. Eğer scraping istenmişse, URL'leri scrape et
        scraped_data = []
        if scrape_content:
            urls = [s['url'] for s in scored_sources[:3]]  # En güvenilir 3 URL
            
            print(f"   🕷️  {len(urls)} URL scraping...")
            scraped_data = await self._scrape_urls(urls)
            print(f"   ✅ {len(scraped_data)} URL scrape edildi")
        
        # 3. Final analiz: Tüm verileri sentezle
        print("   🧠 Final analiz...")
        analysis = self._synthesize_findings(
            topic=topic,
            initial_findings=initial_findings,
            scraped_data=scraped_data
        )
        
        # Kaynak skorlarını ekle
        analysis['scored_sources'] = scored_sources
        analysis['source_diversity'] = scorer.calculate_diversity_score(scored_sources)
        
        log_agent_action("ResearcherAgent", "research_complete", {
            "sources_found": len(scored_sources),
            "avg_score": sum(s['score'] for s in scored_sources) / len(scored_sources) if scored_sources else 0
        })
        
        print(f"   ✅ Araştırma tamamlandı!\n")
        
        return analysis
    
    async def _scrape_urls(self, urls: List[str]) -> List[Dict]:
        """URL'leri scrape et"""
        results = []
        
        async with AsyncWebCrawler(verbose=False) as crawler:
            for url in urls:
                try:
                    result = await crawler.arun(url=url)
                    
                    if result.success:
                        # İlk 3000 karakter al
                        content = result.markdown[:3000]
                        results.append({
                            'url': url,
                            'content': content,
                            'success': True
                        })
                    else:
                        results.append({
                            'url': url,
                            'error': result.error_message,
                            'success': False
                        })
                except Exception as e:
                    results.append({
                        'url': url,
                        'error': str(e),
                        'success': False
                    })
                
                # Rate limiting
                await asyncio.sleep(0.5)
        
        return results
    
    def _synthesize_findings(
        self,
        topic: str,
        initial_findings: str,
        scraped_data: List[Dict]
    ) -> Dict:
        """Tüm bulguları sentezle"""
        
        # Synthesis prompt
        synthesis_prompt = f"""Konu: {topic}

Web Search Bulguları:
{initial_findings}

"""
        
        # Scrape edilen içerikleri ekle
        if scraped_data:
            synthesis_prompt += "\nScrape Edilen İçerikler:\n"
            for i, data in enumerate(scraped_data, 1):
                if data['success']:
                    synthesis_prompt += f"\n[Kaynak {i}] {data['url']}\n{data['content'][:500]}...\n"
        
        synthesis_prompt += """

Tüm bu bilgileri analiz et ve şu formatta JSON döndür:
{
  "topic": "...",
  "key_findings": ["Ana bulgu 1", "Ana bulgu 2", ...],
  "summary": "Genel özet (3-4 paragraf)",
  "sources_analyzed": sayı,
  "confidence": 1-5 (veri kalitesine göre)
}
"""
        
        # Synthesis model (JSON zorla)
        synthesis_model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": 0.5,
                "response_mime_type": "application/json"
            }
        )
        
        response = synthesis_model.generate_content(synthesis_prompt)
        
        # Rate limit için bekle
        time.sleep(13)
        
        import json
        analysis = json.loads(response.text)
        
        # Scrape edilen URL'leri ekle
        analysis['scraped_sources'] = [
            {'url': d['url'], 'success': d['success']}
            for d in scraped_data
        ]
        
        return analysis


# =============================================================================
# TEST
# =============================================================================

async def test_researcher():
    print("\n" + "="*70)
    print("🧪 RESEARCHER AGENT TEST")
    print("="*70 + "\n")
    
    # Agent oluştur
    researcher = ResearcherAgent()
    
    # Test
    topic = "Yapay zeka güvenliği ve etik"
    
    print(f"📋 Konu: {topic}\n")
    
    # Araştır (scraping kapalı - çok uzun sürer)
    result = await researcher.research_topic(
        topic=topic,
        max_sources=3,
        scrape_content=False  # Test için kapalı
    )
    
    # Sonuçları göster
    print("\n" + "="*70)
    print("📊 ARAŞTIRMA SONUÇLARI")
    print("="*70 + "\n")
    
    print(f"📌 Konu: {result['topic']}")
    print(f"🔢 Kaynak sayısı: {result['sources_analyzed']}")
    print(f"⭐ Güven: {result['confidence']}/5\n")
    
    print("🔑 Ana Bulgular:")
    for i, finding in enumerate(result['key_findings'], 1):
        print(f"{i}. {finding}")
    
    print(f"\n📝 Özet:\n{result['summary']}\n")
    
    # Kaydet
    import json
    output_file = "examples/output_researcher_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Kaydedildi: {output_file}\n")
    
    print("="*70)
    print("✅ TEST TAMAMLANDI")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(test_researcher())
