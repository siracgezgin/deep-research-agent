# 03 - Web Scraping ile Veri Toplama

## 🎯 Bu Bölümde Neler Öğreneceğiz?

1. Crawl4AI nedir ve neden kullanıyoruz?
2. Basit web scraping işlemleri
3. Asenkron (paralel) scraping
4. LLM-friendly veri çıkarma
5. Crawl4AI'yı ADK ajanlarına entegre etme

---

## Neden Crawl4AI?

### Geleneksel Yöntemler vs Crawl4AI

| Özellik | requests + BeautifulSoup | Selenium | Crawl4AI |
|---------|-------------------------|----------|----------|
| JavaScript desteği | ❌ Yok | ✅ Var | ✅ Var |
| Hız | ⚡ Çok hızlı | 🐌 Yavaş | ⚡ Hızlı |
| Async/Paralel | 🔧 Manuel | 🔧 Zor | ✅ Hazır |
| LLM-friendly çıktı | 🔧 Manuel temizlik | 🔧 Manuel temizlik | ✅ Otomatik Markdown |
| AI ajanları için tasarım | ❌ | ❌ | ✅ |

### Crawl4AI'ın Avantajları

1. **Markdown Çıktısı**: HTML yerine temiz Markdown → LLM'e daha az token
2. **Akıllı Temizleme**: Menü, reklam, footer otomatik temizlenir
3. **JavaScript Desteği**: Modern SPA'ler (React, Vue) çalışır
4. **Asenkron**: Aynı anda 10-20 site taranabilir
5. **Açık Kaynak**: Ücretsiz, özelleştirilebilir

---

## Adım 1: Crawl4AI Kurulumu (Tekrar)

Eğer kurulum bölümünde yaptıysanız atla, yoksa:

```bash
# Sanal ortamı aktifleştir
source venv/bin/activate

# Crawl4AI'yı kur
pip install 'crawl4ai[all]'

# Playwright browser'ı kur
playwright install chromium
```

### Test Edelim

```bash
python -c "from crawl4ai import AsyncWebCrawler; print('✅ Crawl4AI hazır!')"
```

---

## Adım 2: İlk Scraping İşlemi

### Dosya: `examples/04_basic_scraping.py`

```python
"""
Crawl4AI ile basit web scraping
"""

import asyncio
from crawl4ai import AsyncWebCrawler

async def scrape_single_page(url: str):
    """Tek bir sayfayı tarar"""
    
    print(f"🌐 Taranan URL: {url}\n")
    
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Sayfayı tara
        result = await crawler.arun(url=url)
        
        # Sonuçları göster
        print("=" * 70)
        print("📊 SCRAPING SONUÇLARI")
        print("=" * 70)
        print(f"✅ Başarılı: {result.success}")
        print(f"📏 HTML boyutu: {len(result.html)} karakter")
        print(f"📝 Markdown boyutu: {len(result.markdown)} karakter")
        print(f"🔗 Bulunan link sayısı: {len(result.links)}")
        
        print("\n" + "=" * 70)
        print("📄 İÇERİK ÖNİZLEMESİ (İlk 1000 karakter)")
        print("=" * 70)
        print(result.markdown[:1000])
        print("\n...")
        
        return result

def main():
    print("=" * 70)
    print("CRAWL4AI - TEMEL WEB SCRAPING")
    print("=" * 70 + "\n")
    
    # Test URL'i (Wikipedia - stabil ve hızlı)
    test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    
    # Async fonksiyonu çalıştır
    result = asyncio.run(scrape_single_page(test_url))
    
    print("\n✅ Scraping tamamlandı!")

if __name__ == "__main__":
    main()
```

### Çalıştırma

```bash
python examples/04_basic_scraping.py
```

### Ne Oldu?

1. Crawl4AI bir Chromium browser açtı (görünmez - headless)
2. Wikipedia sayfasını yükledi
3. JavaScript'leri çalıştırdı
4. İçeriği temizleyip Markdown'a çevirdi
5. Link'leri, görselleri extract etti

---

## Adım 3: Paralel (Asenkron) Scraping

Gerçek "Deep Research" için tek tek taramak çok yavaş. Crawl4AI birden fazla siteyi aynı anda tarayabilir.

### Dosya: `examples/05_parallel_scraping.py`

```python
"""
Birden fazla URL'i paralel olarak tara
"""

import asyncio
from crawl4ai import AsyncWebCrawler
from typing import List, Dict

async def scrape_multiple_urls(urls: List[str]) -> Dict[str, str]:
    """
    Birden fazla URL'i paralel olarak tarar
    
    Args:
        urls: Taranacak URL listesi
        
    Returns:
        {url: markdown_content} dictionary
    """
    
    results = {}
    
    async with AsyncWebCrawler(verbose=False) as crawler:
        print(f"🚀 {len(urls)} URL paralel olarak taranıyor...\n")
        
        # Tüm URL'ler için task oluştur
        tasks = [crawler.arun(url=url) for url in urls]
        
        # Hepsini aynı anda çalıştır ve bekle
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Sonuçları işle
        for url, response in zip(urls, responses):
            if isinstance(response, Exception):
                print(f"❌ Hata [{url}]: {response}")
                results[url] = f"ERROR: {response}"
            elif response.success:
                print(f"✅ Başarılı [{url}] - {len(response.markdown)} karakter")
                results[url] = response.markdown
            else:
                print(f"⚠️  Başarısız [{url}]")
                results[url] = "ERROR: Scraping failed"
    
    return results

def main():
    print("=" * 70)
    print("PARALEL WEB SCRAPING")
    print("=" * 70 + "\n")
    
    # Test URL'leri
    urls = [
        "https://en.wikipedia.org/wiki/Electric_vehicle",
        "https://en.wikipedia.org/wiki/Lithium-ion_battery",
        "https://en.wikipedia.org/wiki/Tesla,_Inc.",
    ]
    
    print(f"📋 Taranacak URL sayısı: {len(urls)}\n")
    
    # Paralel scraping
    import time
    start_time = time.time()
    
    results = asyncio.run(scrape_multiple_urls(urls))
    
    elapsed = time.time() - start_time
    
    print(f"\n⏱️  Toplam süre: {elapsed:.2f} saniye")
    print(f"📊 Ortalama: {elapsed/len(urls):.2f} saniye/URL")
    
    print("\n" + "=" * 70)
    print("SONUÇLAR")
    print("=" * 70)
    
    for url, content in results.items():
        preview = content[:200] if not content.startswith("ERROR") else content
        print(f"\n🔗 {url}")
        print(f"   📝 {len(content)} karakter")
        print(f"   👁️  Önizleme: {preview}...")

if __name__ == "__main__":
    main()
```

### Çalıştırma

```bash
python examples/05_parallel_scraping.py
```

### Seri vs Paralel Karşılaştırma

| Yöntem | 3 URL için Süre | 10 URL için Süre |
|--------|-----------------|------------------|
| Seri (tek tek) | ~15 saniye | ~50 saniye |
| Paralel (aynı anda) | ~5 saniye | ~8 saniye |

---

## Adım 4: LLM-Friendly Scraping

Crawl4AI'ın en güçlü özelliği: Sadece bize değil, **LLM'e** de uygun içerik çıkarması.

### Özellikler

1. **Otomatik Temizleme**: Gereksiz elementler çıkarılır
2. **Yapılandırılmış Markdown**: Başlıklar, listeler, tablolar korunur
3. **Link Extraction**: Tüm link'ler ayrıca listelenir
4. **Media Extraction**: Görseller, videolar metadata olarak

### Gelişmiş Scraping Ayarları

### Dosya: `src/tools/advanced_scraper.py`

```python
"""
Gelişmiş scraping fonksiyonları
LLM'ler için optimize edilmiş
"""

import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AdvancedScraper:
    """Gelişmiş web scraping sınıfı"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
        # Browser konfigürasyonu
        self.browser_config = BrowserConfig(
            headless=True,  # Görünmez mod
            viewport_width=1920,
            viewport_height=1080,
            user_agent="Mozilla/5.0 (Martur Research Agent)"
        )
    
    async def scrape_for_llm(
        self, 
        url: str,
        wait_for: Optional[str] = None  # CSS selector - beklenecek element
    ) -> Dict[str, any]:
        """
        LLM için optimize edilmiş scraping
        
        Args:
            url: Taranacak URL
            wait_for: JavaScript yüklenmesini beklemek için CSS selector
            
        Returns:
            Temizlenmiş içerik ve metadata
        """
        
        async with AsyncWebCrawler(
            config=self.browser_config,
            verbose=self.verbose
        ) as crawler:
            
            # Crawler ayarları
            run_config = CrawlerRunConfig(
                # JavaScript'lerin yüklenmesini bekle
                js_code="window.scrollTo(0, document.body.scrollHeight);",  # Sayfayı kaydır
                wait_for=wait_for,
                
                # Sadece ana içeriği al
                exclude_external_links=True,  # Dış link'leri çıkar
                
                # Medya ayarları
                screenshot=False,  # Screenshot'a gerek yok (token tasarrufu)
            )
            
            result = await crawler.arun(
                url=url,
                config=run_config
            )
            
            if not result.success:
                return {
                    "success": False,
                    "error": "Scraping failed",
                    "url": url
                }
            
            # LLM-friendly output
            return {
                "success": True,
                "url": url,
                "title": self._extract_title(result.html),
                "markdown": result.markdown,
                "markdown_length": len(result.markdown),
                "links": result.links[:10],  # İlk 10 link
                "summary": result.markdown[:500]  # İlk 500 karakter özet
            }
    
    async def scrape_multiple_for_llm(
        self,
        urls: List[str],
        max_concurrent: int = 5
    ) -> List[Dict[str, any]]:
        """
        Birden fazla URL'i paralel tara (rate limit ile)
        
        Args:
            urls: URL listesi
            max_concurrent: Aynı anda maksimum tarama sayısı
            
        Returns:
            Sonuç listesi
        """
        
        results = []
        
        # URL'leri gruplara böl (rate limiting için)
        for i in range(0, len(urls), max_concurrent):
            batch = urls[i:i + max_concurrent]
            
            print(f"🔄 Batch {i//max_concurrent + 1} taranıyor ({len(batch)} URL)...")
            
            tasks = [self.scrape_for_llm(url) for url in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, Exception):
                    results.append({"success": False, "error": str(result)})
                else:
                    results.append(result)
            
            # Batch'ler arası bekleme (rate limit)
            if i + max_concurrent < len(urls):
                await asyncio.sleep(1)
        
        return results
    
    def _extract_title(self, html: str) -> str:
        """HTML'den title tag'ini çıkar"""
        import re
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        return match.group(1) if match else "No title"


# Test fonksiyonu
async def test_advanced_scraper():
    """Test için örnek kullanım"""
    
    scraper = AdvancedScraper(verbose=True)
    
    # Tek URL test
    result = await scraper.scrape_for_llm(
        "https://en.wikipedia.org/wiki/Web_scraping"
    )
    
    print("\n" + "=" * 70)
    print("TEST SONUCU")
    print("=" * 70)
    print(f"Başarılı: {result['success']}")
    print(f"Başlık: {result['title']}")
    print(f"İçerik uzunluğu: {result['markdown_length']} karakter")
    print(f"\nÖzet:\n{result['summary']}")

if __name__ == "__main__":
    asyncio.run(test_advanced_scraper())
```

### Test

```bash
python src/tools/advanced_scraper.py
```

---

## Adım 5: Scraper'ı ADK Ajanına Entegre Etme

Şimdi bu scraper'ı bir ADK ajanının kullanabileceği tool'a dönüştürelim.

### Dosya: `src/tools/scraping_tools.py`

```python
"""
ADK ajanları için scraping tool'ları
"""

import asyncio
from typing import List, Dict
from .advanced_scraper import AdvancedScraper

# Global scraper instance (performans için)
_scraper = AdvancedScraper(verbose=False)

def scrape_url_sync(url: str) -> Dict[str, any]:
    """
    Tek bir URL'i tara (senkron - ADK için)
    
    Bu fonksiyon ADK FunctionTool olarak kullanılacak.
    ADK async desteklese de, basitlik için sync versiyon.
    
    Args:
        url: Taranacak web sayfası URL'i
        
    Returns:
        İçerik ve metadata
    """
    # Async fonksiyonu sync çağır
    result = asyncio.run(_scraper.scrape_for_llm(url))
    
    # LLM'e gönderilecek formatta döndür
    if result["success"]:
        return {
            "status": "success",
            "url": url,
            "title": result["title"],
            "content": result["markdown"][:10000],  # İlk 10k karakter (token limiti)
            "content_length": result["markdown_length"]
        }
    else:
        return {
            "status": "error",
            "url": url,
            "error": result.get("error", "Unknown error")
        }

def scrape_multiple_urls_sync(urls: List[str]) -> List[Dict[str, any]]:
    """
    Birden fazla URL'i paralel tara (senkron wrapper)
    
    Args:
        urls: URL listesi (maksimum 10)
        
    Returns:
        Her URL için sonuç listesi
    """
    # Güvenlik: Maksimum 10 URL
    urls = urls[:10]
    
    # Async fonksiyonu çalıştır
    results = asyncio.run(_scraper.scrape_multiple_for_llm(urls))
    
    # Format dönüşümü
    formatted_results = []
    for result in results:
        if result["success"]:
            formatted_results.append({
                "status": "success",
                "url": result["url"],
                "title": result["title"],
                "content": result["markdown"][:5000],  # 5k karakter (birden fazla URL olduğu için daha kısa)
                "content_length": result["markdown_length"]
            })
        else:
            formatted_results.append({
                "status": "error",
                "url": result.get("url", "unknown"),
                "error": result.get("error", "Unknown error")
            })
    
    return formatted_results
```

### Ajanla Kullanımı

### Dosya: `examples/06_agent_with_scraper.py`

```python
"""
Scraping tool'u kullanan ajan
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from google.adk.agents import LlmAgent
from google.adk.models import GeminiModel
from google.adk.tools import FunctionTool

from src.tools.scraping_tools import scrape_url_sync

load_dotenv()

def create_scraping_agent():
    """Web scraping yapabilen bir ajan"""
    
    model = GeminiModel(
        model_id="gemini-1.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Scraping tool'unu ekle
    scrape_tool = FunctionTool(scrape_url_sync)
    
    agent = LlmAgent(
        model=model,
        name="WebScrapingAgent",
        instruction="""
        Sen bir web içerik analiz uzmanısın.
        
        Kullanıcı bir URL verdiğinde:
        1. scrape_url_sync tool'unu kullanarak sayfayı oku
        2. İçeriği analiz et
        3. Ana noktaları özetleyerek sun
        
        Kullanıcının sorusuna göre içerikten ilgili bilgileri çıkar.
        """,
        tools=[scrape_tool]
    )
    
    return agent

def main():
    print("=" * 70)
    print("WEB SCRAPING AJANI")
    print("=" * 70 + "\n")
    
    agent = create_scraping_agent()
    
    # Test
    url = "https://en.wikipedia.org/wiki/Machine_learning"
    query = f"Bu sayfayı oku ve machine learning'in ne olduğunu özetle: {url}"
    
    print(f"👤 Kullanıcı: {query}\n")
    print("🤖 Ajan çalışıyor...\n")
    
    result = agent.run(query)
    
    print("=" * 70)
    print("YANIT")
    print("=" * 70)
    print(result.output)

if __name__ == "__main__":
    main()
```

### Test

```bash
python examples/06_agent_with_scraper.py
```

---

## 📊 Performans İpuçları

### 1. Token Yönetimi

```python
# ❌ Kötü: Tüm HTML'i LLM'e gönderme
content = result.html  # 50,000+ karakter

# ✅ İyi: Sadece Markdown ve kısalt
content = result.markdown[:10000]  # 10k karakter
```

### 2. Rate Limiting

```python
# Aynı domain'e çok istek gönderme
await asyncio.sleep(1)  # İstekler arası bekleme
```

### 3. Error Handling

```python
try:
    result = await crawler.arun(url)
except Exception as e:
    print(f"Scraping hatası: {e}")
    return default_response
```

---

## 🎓 Özet

Bu bölümde öğrendikleriniz:

- ✅ Crawl4AI ile temel scraping
- ✅ Paralel/asenkron scraping
- ✅ LLM-friendly içerik çıkarma
- ✅ ADK tool olarak entegrasyon

---

## 🧪 Alıştırma

Aşağıdaki görevi tamamlayın:

1. `examples/06_agent_with_scraper.py`'yi çalıştırın
2. Farklı bir URL ile test edin
3. Ajana "Bu sayfadaki tabloları listele" gibi özel bir görev verin

---

## 🎉 Tebrikler!

Web scraping altyapınız hazır! Artık gerçek "Deep Research" ajanını inşa etmeye hazırsınız.

**Sıradaki Adım**: [04-research-agent.md](./04-research-agent.md) - Tam teşekküllü araştırma ajanı
