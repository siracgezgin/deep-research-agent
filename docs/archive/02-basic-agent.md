# 02 - Temel Ajan Geliştirme

## 🎯 Bu Bölümde Neler Öğreneceğiz?

1. Google ADK'da ajan nedir?
2. İlk basit ajanımızı oluşturmak
3. Ajan tiplerine giriş (LlmAgent, SequentialAgent)
4. Custom tool (araç) nasıl yazılır?

---

## Google ADK'da Ajan Kavramı

### Ajan Nedir?

Basitçe: **Bir görevi yerine getirmek için LLM (Gemini) kullanan otonom bir birimdir.**

Bir ajan şunları yapabilir:
- Bir görevi analiz eder
- Hangi araçları kullanacağına karar verir
- Araçları çalıştırır
- Sonuçları değerlendirir
- Gerekirse adımları tekrarlar

### ADK'daki Ajan Tipleri

| Tip | Ne İşe Yarar? | Örnek Kullanım |
|-----|---------------|----------------|
| `LlmAgent` | Temel ajan - tek bir LLM model kullanır | Metin analizi, sorulara yanıt |
| `SequentialAgent` | Alt ajanları sırayla çalıştırır | "Önce araştır, sonra yaz" |
| `ParallelAgent` | Alt ajanları aynı anda çalıştırır | Birden fazla siteyi aynı anda tara |
| `LoopAgent` | Bir koşul sağlanana kadar tekrarlar | "Yeterli bilgi toplandı mı?" |

---

## Adım 1: Temel LlmAgent Oluşturma

İlk ajanımızı oluşturalım. Bu ajan, verilen bir metni özetleyecek.

### Dosya: `examples/01_simple_summarizer.py`

```python
"""
Basit bir özetleme ajanı
Kullanıcıdan metin alır ve özetler
"""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models import GeminiModel

# Environment variables
load_dotenv()

def create_summarizer_agent():
    """Özetleme ajanı oluşturur"""
    
    # Gemini modelini yapılandır
    model = GeminiModel(
        model_id="gemini-1.5-flash",  # Hızlı ve ucuz model
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Ajanı oluştur
    agent = LlmAgent(
        model=model,
        name="SummarizerAgent",
        instruction="""
        Sen bir metin özetleme uzmanısın.
        Kullanıcıdan aldığın metni, ana noktaları koruyarak 3-5 cümleye indir.
        Özet Türkçe olmalı, net ve anlaşılır olmalı.
        """
    )
    
    return agent

def main():
    print("=" * 70)
    print("METIN ÖZETLEME AJANI")
    print("=" * 70)
    
    # Ajanı oluştur
    agent = create_summarizer_agent()
    
    # Test metni
    test_text = """
    Yapay zeka teknolojilerindeki paradigma değişimi, basit metin tabanlı 
    etkileşimlerden (chatbotlar), karmaşık görevleri otonom olarak planlayabilen, 
    araç kullanabilen ve yürütebilen "ajan tabanlı" (agentic) iş akışlarına doğru 
    evrilmektedir. Martur gibi küresel ölçekte faaliyet gösteren sanayi ve teknoloji 
    odaklı organizasyonlar için, bu dönüşüm stratejik bir fırsat sunmaktadır. 
    Özellikle pazar araştırması, rekabet analizi ve teknik literatür taraması gibi 
    yoğun emek gerektiren süreçlerin otomasyonu, "Deep Research" adı verilen yeni 
    nesil AI ajanları ile mümkün hale gelmiştir.
    """
    
    print("\n📄 Özgün Metin:")
    print(test_text)
    
    print("\n🤖 Ajan çalışıyor...\n")
    
    # Ajanı çalıştır
    result = agent.run(f"Bu metni özetle:\n\n{test_text}")
    
    print("✅ Özet:")
    print(result.output)
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
```

### Çalıştırma

```bash
python examples/01_simple_summarizer.py
```

---

## Adım 2: Custom Tool (Araç) Ekleme

Ajanların güçlü olmasının sırrı **tool'lardadır**. Tool'lar, ajanların dış dünya ile etkileşime girmesini sağlar.

### Tool Nedir?

Tool, ajanın çağırabileceği bir Python fonksiyonudur. Örneğin:
- `search_web()` - internette arama yapar
- `scrape_url()` - bir web sayfasını okur
- `save_file()` - dosyaya yazar

### Basit Bir Tool Yazalım

### Dosya: `src/tools/web_tools.py`

```python
"""
Web ile ilgili temel araçlar
"""

import requests
from typing import List, Dict

def fetch_url_content(url: str) -> str:
    """
    Belirtilen URL'in içeriğini indirir (basit versiyon)
    
    Args:
        url: İndirilecek web sayfasının URL'i
        
    Returns:
        Sayfa içeriği (metin)
    """
    try:
        print(f"  🌐 URL indiriliyor: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Martur Research Bot)'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Basitleştirilmiş içerik (HTML tagları temizlenebilir)
        content = response.text[:5000]  # İlk 5000 karakter
        
        print(f"  ✅ İçerik indirildi ({len(content)} karakter)")
        return content
        
    except Exception as e:
        error_msg = f"❌ Hata: {str(e)}"
        print(f"  {error_msg}")
        return error_msg


def search_web(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Web'de arama yapar (basit simülasyon)
    
    Args:
        query: Arama sorgusu
        num_results: Döndürülecek sonuç sayısı
        
    Returns:
        Arama sonuçları listesi
    """
    print(f"  🔍 Arama yapılıyor: '{query}'")
    
    # Gerçek implementasyonda burası Tavily API veya Google Custom Search kullanacak
    # Şimdilik mock data dönüyoruz
    
    mock_results = [
        {
            "title": f"Sonuç 1: {query} hakkında makale",
            "url": "https://example.com/article1",
            "snippet": f"{query} ile ilgili detaylı bilgi içeren makale..."
        },
        {
            "title": f"Sonuç 2: {query} araştırması",
            "url": "https://example.com/article2",
            "snippet": f"{query} konusunda yapılan kapsamlı araştırma..."
        }
    ]
    
    print(f"  ✅ {len(mock_results)} sonuç bulundu")
    return mock_results[:num_results]
```

---

## Adım 3: Tool'u Ajana Bağlama

Tool'u oluşturduk, şimdi ajanın bunu kullanmasını sağlayalım.

### Dosya: `examples/02_agent_with_tools.py`

```python
"""
Tool kullanan ajan örneği
Web'de arama yapabilen bir araştırma ajanı
"""

import os
import sys
from dotenv import load_dotenv

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from google.adk.agents import LlmAgent
from google.adk.models import GeminiModel
from google.adk.tools import FunctionTool

from src.tools.web_tools import search_web, fetch_url_content

load_dotenv()

def create_research_agent():
    """Tool'ları kullanabilen bir araştırma ajanı oluşturur"""
    
    # Model
    model = GeminiModel(
        model_id="gemini-1.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Tool'ları ADK formatına çevir
    search_tool = FunctionTool(search_web)
    fetch_tool = FunctionTool(fetch_url_content)
    
    # Ajanı oluştur
    agent = LlmAgent(
        model=model,
        name="ResearchAgent",
        instruction="""
        Sen bir araştırma asistanısın.
        Kullanıcının sorusuna yanıt vermek için şu araçları kullanabilirsin:
        
        1. search_web: İnternette arama yapar
        2. fetch_url_content: Bir web sayfasının içeriğini okur
        
        Kullanıcının isteğini anla, gerekli araçları kullan ve bulduğun 
        bilgileri özetleyerek sun.
        """,
        tools=[search_tool, fetch_tool]
    )
    
    return agent

def main():
    print("=" * 70)
    print("ARAÇ KULLANAN ARAŞTIRMA AJANI")
    print("=" * 70)
    
    agent = create_research_agent()
    
    # Test sorgusu
    user_query = "Yapay zeka ajanları nedir? İnternette araştır."
    
    print(f"\n👤 Kullanıcı: {user_query}\n")
    print("🤖 Ajan düşünüyor ve araçları kullanıyor...\n")
    
    result = agent.run(user_query)
    
    print("\n✅ Ajanın Yanıtı:")
    print(result.output)
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
```

### Çalıştırma

```bash
python examples/02_agent_with_tools.py
```

### Ne Oldu?

1. Ajan, kullanıcının "internette araştır" dediğini anladı
2. `search_web` tool'unu çağırdı
3. Sonuçları aldı
4. Bu sonuçları sentezleyerek yanıt verdi

---

## Adım 4: Sequential Agent - Çok Aşamalı İşlem

Gerçek dünyada işler genellikle adım adım ilerler:
1. Önce plan yap
2. Sonra araştır
3. En son rapor yaz

### Dosya: `examples/03_sequential_agent.py`

```python
"""
Sequential Agent örneği
Adım adım çalışan araştırma süreci
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models import GeminiModel
from google.adk.tools import FunctionTool

from src.tools.web_tools import search_web

load_dotenv()

def create_sequential_research_workflow():
    """Sıralı çalışan bir araştırma workflow'u oluşturur"""
    
    model = GeminiModel(
        model_id="gemini-1.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Adım 1: Planlayıcı Ajan
    planner = LlmAgent(
        model=model,
        name="Planner",
        instruction="""
        Sen bir araştırma planlayıcısısın.
        Kullanıcının isteğini analiz et ve 3-5 alt başlığa böl.
        Her başlık için spesifik bir arama sorgusu öner.
        Çıktı formatı: Numaralandırılmış liste
        """
    )
    
    # Adım 2: Araştırmacı Ajan
    researcher = LlmAgent(
        model=model,
        name="Researcher",
        instruction="""
        Sen bir araştırmacısın.
        Planlayıcının verdiği başlıkları kullanarak web'de arama yap.
        Her başlık için search_web tool'unu kullan.
        Bulduğun bilgileri özetle.
        """,
        tools=[FunctionTool(search_web)]
    )
    
    # Adım 3: Rapor Yazıcı Ajan
    writer = LlmAgent(
        model=model,
        name="Writer",
        instruction="""
        Sen bir teknik rapor yazarısın.
        Araştırmacının bulduğu bilgileri kullanarak profesyonel bir rapor yaz.
        Rapor yapısı:
        1. Özet
        2. Ana Bulgular
        3. Detaylar
        4. Sonuç
        """
    )
    
    # Workflow: Sırayla çalıştır
    workflow = SequentialAgent(
        name="ResearchWorkflow",
        sub_agents=[planner, researcher, writer]
    )
    
    return workflow

def main():
    print("=" * 70)
    print("SEQUENTIAL AGENT - ÇOK AŞAMALI ARAŞTIRMA")
    print("=" * 70)
    
    workflow = create_sequential_research_workflow()
    
    user_request = "Elektrikli araçlarda kullanılan batarya teknolojilerini araştır"
    
    print(f"\n👤 İstek: {user_request}\n")
    print("🤖 Workflow başlıyor...\n")
    print("  1️⃣ Planlayıcı çalışıyor...")
    print("  2️⃣ Araştırmacı çalışıyor...")
    print("  3️⃣ Rapor yazılıyor...\n")
    
    result = workflow.run(user_request)
    
    print("=" * 70)
    print("📄 SONUÇ RAPORU")
    print("=" * 70)
    print(result.output)
    print("=" * 70)

if __name__ == "__main__":
    main()
```

---

## 🎓 Önemli Kavramlar

### 1. Agent vs Tool

- **Agent**: Karar verir, düşünür (LLM kullanır)
- **Tool**: Sadece bir işi yapar (Python fonksiyonu)

### 2. Instruction (Talimat)

Ajanın "karakteri" ve "görev tanımı". Ne kadar net olursa ajan o kadar iyi çalışır.

### 3. Sequential vs Parallel

- **Sequential**: Sırayla (A bitsin, B başlasın)
- **Parallel**: Aynı anda (A ve B birlikte)

---

## 📝 Alıştırmalar

Bu bölümü bitirmeden önce şunları dene:

1. `01_simple_summarizer.py`'yi çalıştır, kendi metninle test et
2. `02_agent_with_tools.py`'de farklı sorular sor
3. `web_tools.py`'ye yeni bir tool ekle: `count_words(text: str) -> int`

---

## 🎉 Tebrikler!

Temel ajan geliştirmeyi öğrendiniz! Artık:
- ✅ Basit ajanlar oluşturabiliyorsunuz
- ✅ Custom tool yazabiliyorsunuz
- ✅ Sequential workflow kurabiliyorsunuz

**Sıradaki Adım**: [03-web-scraping.md](./03-web-scraping.md) - Gerçek web scraping'i öğreneceğiz (Crawl4AI)
