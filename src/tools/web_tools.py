"""
Web Araçları - Web search ve scraping
====================================
Bu modülde ajanların kullanabileceği web tool'ları var.

- Tavily API ile gerçek web search
- Mock data fallback
"""

import os
from typing import List, Dict
import time
from dotenv import load_dotenv

load_dotenv()


def search_web_simple(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Web'de arama yapar (Tavily API)
    
    Args:
        query: Arama sorgusu
        max_results: Döndürülecek maksimum sonuç sayısı
        
    Returns:
        Arama sonuçları listesi
        
    Her sonuç şu bilgileri içerir:
    - title: Sayfa başlığı
    - url: Sayfa URL'i
    - snippet: Kısa açıklama
    """
    
    # Tip dönüşümü (Gemini bazen string gönderebilir)
    max_results = int(max_results)
    
    print(f"  🔍 Web'de aranıyor: '{query}'")
    
    # Tavily API key kontrolü
    tavily_api_key = os.getenv('TAVILY_API_KEY')
    
    if tavily_api_key and tavily_api_key != 'your_tavily_api_key_here':
        # Gerçek Tavily API kullan
        try:
            from tavily import TavilyClient
            
            client = TavilyClient(api_key=tavily_api_key)
            
            # Arama yap
            response = client.search(
                query=query,
                max_results=max_results,
                search_depth="basic"  # "basic" veya "advanced"
            )
            
            # Sonuçları formatla
            results = []
            for item in response.get('results', []):
                results.append({
                    'title': item.get('title', 'No title'),
                    'url': item.get('url', ''),
                    'snippet': item.get('content', '')[:200]  # İlk 200 karakter
                })
            
            print(f"  ✅ {len(results)} sonuç bulundu (Tavily API)")
            return results
            
        except ImportError:
            print("  ⚠️  Tavily kütüphanesi yüklü değil, mock data kullanılıyor")
            return _mock_search_results(query, max_results)
        except Exception as e:
            print(f"  ⚠️  Tavily API hatası: {e}, mock data kullanılıyor")
            return _mock_search_results(query, max_results)
    else:
        # Mock data kullan
        print("  ℹ️  Tavily API key bulunamadı, mock data kullanılıyor")
        return _mock_search_results(query, max_results)


def _mock_search_results(query: str, max_results: int) -> List[Dict[str, str]]:
    """Mock search results (Tavily API olmadığında)"""
    time.sleep(0.5)  # Gerçekçi olsun diye
    
    mock_results = [
        {
            "title": f"Wikipedia - {query}",
            "url": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
            "snippet": f"{query} hakkında detaylı Wikipedia makalesi. Tanımlar, tarihçe ve örnekler içerir."
        },
        {
            "title": f"{query} Nedir? - Kapsamlı Rehber",
            "url": "https://example.com/rehber",
            "snippet": f"{query} konusunda başlangıç seviyesinden ileri seviyeye kapsamlı bilgiler."
        },
        {
            "title": f"Son Gelişmeler: {query}",
            "url": "https://example.com/haberler",
            "snippet": f"{query} alanındaki en son gelişmeler ve trendler hakkında güncel bilgiler."
        },
        {
            "title": f"{query} Uygulamaları",
            "url": "https://example.com/uygulamalar",
            "snippet": f"Gerçek dünyada {query} nasıl kullanılıyor? Örnekler ve vaka çalışmaları."
        },
        {
            "title": f"{query} Araştırmaları ve İstatistikler",
            "url": "https://example.com/arastirma",
            "snippet": f"{query} hakkında bilimsel araştırmalar, raporlar ve istatistiksel veriler."
        }
    ]
    
    results = mock_results[:max_results]
    print(f"  ✅ {len(results)} sonuç bulundu\n")
    
    return results

def fetch_url_content_simple(url: str) -> str:
    """
    Bir URL'in içeriğini getirir (şimdilik mock data)
    
    Args:
        url: İndirilecek URL
        
    Returns:
        Sayfa içeriği (metin)
    """
    
    print(f"  🌐 Sayfa indiriliyor: {url}")
    time.sleep(0.5)
    
    # Mock içerik - Crawl4AI ekleyince gerçek içerik gelecek
    mock_content = f"""
    Bu sayfa {url} adresinden mock (sahte) içeriktir.
    
    Gerçek implementasyonda burada sayfanın tam içeriği olacak.
    Şimdilik ajanın tool'ları nasıl kullandığını görmek için
    bu mock data'yı kullanıyoruz.
    
    İleride:
    - Crawl4AI ile gerçek sayfalar taranacak
    - HTML temizlenip Markdown'a çevrilecek
    - Sadece önemli içerik gelecek
    """
    
    print(f"  ✅ İçerik indirildi ({len(mock_content)} karakter)\n")
    return mock_content.strip()

# Test fonksiyonu
if __name__ == "__main__":
    print("=" * 70)
    print("WEB TOOLS TEST")
    print("=" * 70)
    print()
    
    # Arama testi
    print("📍 Test 1: Web Araması")
    print("-" * 70)
    results = search_web_simple("yapay zeka", max_results=3)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Özet: {result['snippet'][:80]}...")
        print()
    
    # İçerik getirme testi
    print("📍 Test 2: URL İçerik Getirme")
    print("-" * 70)
    content = fetch_url_content_simple(results[0]['url'])
    print(content)
