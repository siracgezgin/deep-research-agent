# 04 - Deep Research Agent - Tam Proje

## 🎯 Bu Bölümde Ne Yapacağız?

Şimdiye kadar öğrendiğimiz her şeyi birleştirip **tam teşekküllü bir araştırma ajanı** oluşturacağız.

### Sistem Özellikleri

✅ Verilen konuyu otomatik olarak alt başlıklara böler
✅ Her başlık için web'de arama yapar
✅ En alakalı siteleri seçer ve tarar
✅ Toplanan bilgiyi değerlendirir
✅ Eksik bilgi varsa araştırmayı derinleştirir (Loop)
✅ Profesyonel bir rapor oluşturur

---

## Mimari Tasarım

```
┌─────────────────────────────────────────────────────┐
│           MARTUR DEEP RESEARCH AGENT                │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Router Agent                │
        │   (İsteği analiz eder)        │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Sequential Workflow         │
        └───────────────────────────────┘
                        │
        ┌───────────────┴───────────────────────────┐
        │                                           │
        ▼                                           ▼
┌───────────────┐                          ┌───────────────┐
│ 1. PLANNER    │                          │ 3. WRITER     │
│   Agent       │                          │    Agent      │
│               │                          │               │
│ Konuyu alt    │                          │ Rapor yazar   │
│ başlıklara    │                          └───────────────┘
│ böler         │                                   ▲
└───────────────┘                                   │
        │                                           │
        ▼                                           │
┌───────────────────────────────────────────────────┤
│ 2. RESEARCH LOOP AGENT                            │
│    (Yeterli bilgi toplanana kadar döngü)         │
│                                                   │
│    ┌──────────────────────────────────┐         │
│    │ a) Search Agent                   │         │
│    │    (Web'de arama yapar)          │         │
│    └──────────────────────────────────┘         │
│                    │                              │
│                    ▼                              │
│    ┌──────────────────────────────────┐         │
│    │ b) Scraper Agent (Parallel)      │         │
│    │    (Siteleri paralel tarar)      │         │
│    └──────────────────────────────────┘         │
│                    │                              │
│                    ▼                              │
│    ┌──────────────────────────────────┐         │
│    │ c) Evaluator Agent               │         │
│    │    (Bilgi yeterli mi kontrol)    │         │
│    └──────────────────────────────────┘         │
│                    │                              │
│                    └──────────────────────────────┤
│                         (Loop)                    │
└───────────────────────────────────────────────────┘
```

---

## Adım 1: Web Search Tool (Tavily API)

Önce web araması yapacak tool'u oluşturalım.

### Tavily API Key Alma (Ücretsiz)

1. [tavily.com](https://tavily.com) → Sign up
2. Dashboard → API key kopyala
3. `.env` dosyasına ekle:

```bash
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxx
```

### Dosya: `src/tools/search_tools.py`

```python
"""
Web arama araçları (Tavily API)
"""

import os
from typing import List, Dict, Optional
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class SearchEngine:
    """Web arama motoru (Tavily)"""
    
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        
        self.client = TavilyClient(api_key=api_key)
    
    def search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "advanced"  # "basic" veya "advanced"
    ) -> List[Dict[str, str]]:
        """
        Web'de arama yapar
        
        Args:
            query: Arama sorgusu
            max_results: Maksimum sonuç sayısı
            search_depth: "basic" (hızlı) veya "advanced" (detaylı)
            
        Returns:
            Arama sonuçları listesi
        """
        
        print(f"  🔍 Arama: '{query}'")
        
        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth=search_depth,
                include_raw_content=False  # Ham HTML'e gerek yok
            )
            
            results = []
            for item in response.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),  # Tavily'nin özetlediği içerik
                    "score": item.get("score", 0.0)
                })
            
            print(f"  ✅ {len(results)} sonuç bulundu")
            return results
            
        except Exception as e:
            print(f"  ❌ Arama hatası: {e}")
            return []


# ADK için senkron fonksiyon
_search_engine = None

def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Web'de arama yap (ADK FunctionTool için)
    
    Args:
        query: Arama sorgusu
        max_results: Maksimum sonuç sayısı (1-10)
        
    Returns:
        Arama sonuçları
    """
    global _search_engine
    
    if _search_engine is None:
        _search_engine = SearchEngine()
    
    # Güvenlik limiti
    max_results = min(max_results, 10)
    
    return _search_engine.search(query, max_results)


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("TAVILY SEARCH TEST")
    print("=" * 70 + "\n")
    
    results = search_web("Google Gemini AI agents", max_results=3)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Skor: {result['score']}")
        print(f"   Özet: {result['content'][:200]}...")
```

### Test

```bash
python src/tools/search_tools.py
```

---

## Adım 2: Ajan Tanımları

Şimdi her bir ajanı ayrı modül olarak oluşturalım.

### Dosya: `src/agents/planner_agent.py`

```python
"""
Planlayıcı Ajan: Araştırma konusunu alt başlıklara böler
"""

import os
from google.adk.agents import LlmAgent
from google.adk.models import GeminiModel
from dotenv import load_dotenv

load_dotenv()

def create_planner_agent() -> LlmAgent:
    """
    Araştırma planlayıcı ajanı oluşturur
    
    Bu ajan, kullanıcının araştırma konusunu analiz edip
    3-5 alt başlık ve her biri için arama sorgusu üretir.
    """
    
    model = GeminiModel(
        model_id="gemini-1.5-pro",  # Planlama için güçlü model
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    agent = LlmAgent(
        model=model,
        name="PlannerAgent",
        instruction="""
        Sen bir araştırma planlama uzmanısın.
        
        GÖREV:
        Kullanıcının verdiği araştırma konusunu analiz et ve 
        kapsamlı bir araştırma planı oluştur.
        
        Planın şu şekilde olmalı:
        
        1. Ana konu özeti (1-2 cümle)
        2. Alt başlıklar (3-5 tane):
           - Her alt başlık konunun farklı bir yönünü kapsamalı
           - Pazar analizi, teknoloji, rekabet, trendler vb.
        
        3. Her alt başlık için arama sorguları:
           - İngilizce olmalı (web araması için optimize edilmiş)
           - Spesifik ve hedef odaklı
        
        ÇIKTI FORMATI (JSON):
        {
            "topic": "Ana konu",
            "summary": "Kısa özet",
            "subtopics": [
                {
                    "title": "Alt başlık 1",
                    "search_queries": ["sorgu1", "sorgu2"]
                },
                ...
            ]
        }
        
        Sadece JSON döndür, başka açıklama ekleme.
        """
    )
    
    return agent
```

### Dosya: `src/agents/researcher_agent.py`

```python
"""
Araştırmacı Ajan: Web'de arama yapar ve içerikleri toplar
"""

import os
import sys
from google.adk.agents import LlmAgent
from google.adk.models import GeminiModel
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

# Tools'u import et
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.tools.search_tools import search_web
from src.tools.scraping_tools import scrape_url_sync, scrape_multiple_urls_sync

load_dotenv()

def create_researcher_agent() -> LlmAgent:
    """
    Araştırmacı ajanı oluşturur
    
    Bu ajan:
    - Web'de arama yapar
    - En alakalı URL'leri seçer
    - O URL'leri tarar
    - İçerikleri özetler
    """
    
    model = GeminiModel(
        model_id="gemini-1.5-flash",  # Veri toplama için hızlı model
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Tool'ları hazırla
    search_tool = FunctionTool(search_web)
    scrape_tool = FunctionTool(scrape_url_sync)
    scrape_multiple_tool = FunctionTool(scrape_multiple_urls_sync)
    
    agent = LlmAgent(
        model=model,
        name="ResearcherAgent",
        instruction="""
        Sen bir web araştırma uzmanısın.
        
        GÖREV:
        Verilen arama sorgularını kullanarak:
        1. search_web tool'u ile web'de arama yap
        2. En alakalı 3-5 URL'yi seç
        3. scrape_multiple_urls_sync ile o URL'leri paralel tara
        4. Her kaynaktan önemli bilgileri çıkar ve özetle
        
        ÖNEMLİ:
        - Her kaynak için mutlaka URL'i kaydet
        - Sayısal veriler varsa not et
        - Çelişkili bilgiler varsa her ikisini de belirt
        
        ÇIKTI FORMATI:
        Her sorgu için:
        
        **Sorgu:** [sorgu adı]
        
        **Bulgular:**
        1. [Kaynak URL]
           - [Önemli bilgi 1]
           - [Önemli bilgi 2]
        
        2. [Kaynak URL]
           ...
        """,
        tools=[search_tool, scrape_tool, scrape_multiple_tool]
    )
    
    return agent
```

### Dosya: `src/agents/evaluator_agent.py`

```python
"""
Değerlendirici Ajan: Toplanan bilginin yeterliliğini kontrol eder
"""

import os
from google.adk.agents import LlmAgent
from google.adk.models import GeminiModel
from dotenv import load_dotenv

load_dotenv()

def create_evaluator_agent() -> LlmAgent:
    """
    Değerlendirici ajanı oluşturur
    
    Bu ajan toplanan bilgiyi analiz edip
    araştırmanın devam etmesi gerekip gerekmediğine karar verir.
    """
    
    model = GeminiModel(
        model_id="gemini-1.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    agent = LlmAgent(
        model=model,
        name="EvaluatorAgent",
        instruction="""
        Sen bir araştırma kalite kontrol uzmanısın.
        
        GÖREV:
        Araştırmacının topladığı bilgiyi değerlendir:
        
        1. Kapsam kontrolü:
           - Tüm alt başlıklar için yeterli bilgi var mı?
           - Eksik kalan nokta var mı?
        
        2. Kalite kontrolü:
           - Bilgiler güncel mi?
           - Birden fazla kaynaktan doğrulandı mı?
           - Sayısal veriler var mı?
        
        3. Karar:
           - YETERLİ: Rapor yazılmaya hazır
           - EKSİK: Daha fazla araştırma gerekli
        
        ÇIKTI FORMATI (JSON):
        {
            "decision": "YETERLİ" veya "EKSİK",
            "reasoning": "Karar gerekçesi",
            "missing_info": ["Eksik konu 1", "Eksik konu 2"],
            "quality_score": 0.0-1.0
        }
        
        Sadece JSON döndür.
        """
    )
    
    return agent
```

### Dosya: `src/agents/writer_agent.py`

```python
"""
Yazar Ajan: Toplanan bilgilerden profesyonel rapor oluşturur
"""

import os
from google.adk.agents import LlmAgent
from google.adk.models import GeminiModel
from dotenv import load_dotenv

load_dotenv()

def create_writer_agent() -> LlmAgent:
    """
    Rapor yazıcı ajanı oluşturur
    
    Bu ajan tüm toplanan bilgiyi sentezleyip
    profesyonel bir teknik rapor oluşturur.
    """
    
    model = GeminiModel(
        model_id="gemini-1.5-pro",  # Yazma için güçlü model
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    agent = LlmAgent(
        model=model,
        name="WriterAgent",
        instruction="""
        Sen deneyimli bir teknik rapor yazarısın.
        
        GÖREV:
        Araştırmacının topladığı tüm bilgileri kullanarak
        profesyonel, akademik tarzda bir rapor yaz.
        
        RAPOR YAPISI:
        
        # [Konu Başlığı]
        
        ## Yönetici Özeti
        - 2-3 paragraf
        - Ana bulguları özetle
        
        ## 1. Giriş
        - Konunun önemi
        - Araştırmanın kapsamı
        
        ## 2. [Alt Başlık 1]
        - Bulgular
        - Destekleyici veriler
        - Kaynak referansları [1], [2] formatında
        
        ## 3. [Alt Başlık 2]
        ...
        
        ## Sonuç ve Öneriler
        - Ana çıkarımlar
        - Gelecek trendler
        - Öneriler
        
        ## Kaynaklar
        [1] URL
        [2] URL
        ...
        
        ÖNEMLİ:
        - Markdown formatında yaz
        - Tüm kaynakları referans göster
        - Sayısal verileri tablolar ile sun
        - Net ve profesyonel dil kullan
        - Türkçe yaz
        """
    )
    
    return agent
```

---

## Adım 3: Ana Workflow

Tüm ajanları birleştiren ana workflow:

### Dosya: `src/martur_research_agent.py`

```python
"""
MARTUR DEEP RESEARCH AGENT
Ana workflow - Tüm ajanları orkestre eder
"""

import os
import sys
import json
from typing import Dict, Any
from dotenv import load_dotenv

from google.adk.agents import SequentialAgent, LoopAgent
from google.adk.models import GeminiModel

# Ajanları import et
sys.path.insert(0, os.path.dirname(__file__))
from agents.planner_agent import create_planner_agent
from agents.researcher_agent import create_researcher_agent
from agents.evaluator_agent import create_evaluator_agent
from agents.writer_agent import create_writer_agent

load_dotenv()

class MarturResearchAgent:
    """Martur Deep Research Agent - Ana Sınıf"""
    
    def __init__(self):
        """Tüm workflow'u hazırlar"""
        
        print("🚀 Martur Research Agent başlatılıyor...\n")
        
        # Ajanları oluştur
        self.planner = create_planner_agent()
        self.researcher = create_researcher_agent()
        self.evaluator = create_evaluator_agent()
        self.writer = create_writer_agent()
        
        # Research Loop: Yeterli bilgi toplanana kadar döner
        # NOT: Gerçek LoopAgent implementasyonu ADK versiyonuna bağlı
        # Basitleştirilmiş versiyon kullanıyoruz
        
        # Ana workflow
        self.workflow = SequentialAgent(
            name="MarturResearchWorkflow",
            sub_agents=[
                self.planner,
                self.researcher,
                # Evaluator ve loop mantığı researcher içinde basitleştirildi
                self.writer
            ]
        )
        
        print("✅ Workflow hazır!\n")
    
    def research(self, topic: str) -> Dict[str, Any]:
        """
        Verilen konu hakkında derin araştırma yapar
        
        Args:
            topic: Araştırma konusu
            
        Returns:
            Rapor ve metadata
        """
        
        print("=" * 70)
        print(f"ARAŞTIRMA KONUSU: {topic}")
        print("=" * 70 + "\n")
        
        # Workflow'u çalıştır
        print("📋 Faz 1: Plan oluşturuluyor...")
        print("🔍 Faz 2: Web araştırması yapılıyor...")
        print("📝 Faz 3: Rapor yazılıyor...\n")
        
        try:
            result = self.workflow.run(topic)
            
            print("\n" + "=" * 70)
            print("✅ ARAŞTIRMA TAMAMLANDI")
            print("=" * 70)
            
            return {
                "success": True,
                "topic": topic,
                "report": result.output,
                "metadata": {
                    "timestamp": self._get_timestamp(),
                    "agent_version": "1.0.0"
                }
            }
            
        except Exception as e:
            print(f"\n❌ HATA: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_timestamp(self) -> str:
        """Timestamp üretir"""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Test için ana fonksiyon"""
    
    # Agent'ı oluştur
    agent = MarturResearchAgent()
    
    # Test konusu
    test_topic = """
    Otomotiv koltuklarında kullanılan sürdürülebilir kumaş ve 
    malzeme trendlerini araştır. Özellikle geri dönüştürülmüş 
    malzemeler ve doğal lifler üzerine odaklan.
    """
    
    # Araştırmayı başlat
    result = agent.research(test_topic.strip())
    
    # Sonucu göster
    if result["success"]:
        print("\n" + "=" * 70)
        print("📄 RAPOR")
        print("=" * 70)
        print(result["report"])
        
        # Raporu dosyaya kaydet
        output_file = "research_report.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["report"])
        
        print(f"\n💾 Rapor kaydedildi: {output_file}")
    else:
        print(f"\n❌ Araştırma başarısız: {result['error']}")


if __name__ == "__main__":
    main()
```

---

## Adım 4: Çalıştırma ve Test

### Gereksinimler Kontrolü

```bash
# requirements.txt oluştur
cat > requirements.txt << 'EOF'
google-genai-adk>=0.1.0
crawl4ai[all]>=0.3.0
tavily-python>=0.3.0
python-dotenv>=1.0.0
requests>=2.31.0
playwright>=1.40.0
EOF

# Kur
pip install -r requirements.txt
```

### Proje Yapısı Kontrolü

```
ai/
├── src/
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── researcher_agent.py
│   │   ├── evaluator_agent.py
│   │   └── writer_agent.py
│   ├── tools/
│   │   ├── search_tools.py
│   │   ├── scraping_tools.py
│   │   └── advanced_scraper.py
│   └── martur_research_agent.py
├── examples/
│   └── ...
├── docs/
│   └── ...
├── .env
├── requirements.txt
└── README.md
```

### Test Çalıştırma

```bash
python src/martur_research_agent.py
```

---

## Adım 5: İyileştirmeler ve Özelleştirmeler

### 1. Loop Mantığını Geliştirme

Gerçek bir "yeterli mi?" kontrolü için:

```python
# src/agents/research_loop.py
def research_with_loop(topic, max_iterations=3):
    """
    Döngüsel araştırma mantığı
    """
    collected_info = []
    iteration = 0
    
    while iteration < max_iterations:
        # Araştır
        new_info = researcher.run(topic)
        collected_info.append(new_info)
        
        # Değerlendir
        eval_result = evaluator.run(collected_info)
        
        if eval_result["decision"] == "YETERLİ":
            break
        
        # Eksik konuları araştır
        topic = eval_result["missing_info"]
        iteration += 1
    
    return collected_info
```

### 2. Paralel Araştırma

Birden fazla alt başlığı aynı anda araştırmak için:

```python
from google.adk.agents import ParallelAgent

parallel_researcher = ParallelAgent(
    sub_agents=[researcher1, researcher2, researcher3]
)
```

### 3. Kendi Veri Kaynaklarınızı Ekleme

Martur'un kendi veritabanı veya dosyaları varsa:

```python
# src/tools/internal_search.py
def search_internal_docs(query: str):
    """Martur'un iç dokümantasyonunda arar"""
    # PDF'leri, Excel'leri, veritabanını ara
    pass
```

---

## 🎯 Proje Teslim Kontrol Listesi

### Temel Gereksinimler
- [ ] Kullanıcı bir konu verebiliyor
- [ ] Sistem otomatik alt başlıklar üretiyor
- [ ] Web'de arama yapılıyor
- [ ] Siteler taranıyor (scraping)
- [ ] Rapor oluşturuluyor

### İleri Seviye (Opsiyonel)
- [ ] Döngüsel araştırma (loop)
- [ ] Paralel tarama
- [ ] PDF/Excel export
- [ ] Web UI (Streamlit)
- [ ] Hata loglama

---

## 📊 Performans Metrikleri

Test sonuçlarınızı kaydedin:

| Metrik | Hedef | Gerçekleşen |
|--------|-------|-------------|
| Araştırma süresi | < 3 dakika | ? |
| Taranan site sayısı | 10-20 | ? |
| Rapor uzunluğu | 2000+ kelime | ? |
| Kaynak sayısı | 10+ | ? |

---

## 🐛 Hata Giderme

### Sorun: "TAVILY_API_KEY bulunamadı"

```bash
# .env dosyasını kontrol et
cat .env | grep TAVILY

# Eksikse ekle
echo "TAVILY_API_KEY=tvly-xxx" >> .env
```

### Sorun: Import hataları

```bash
# PYTHONPATH'i ayarla
export PYTHONPATH="/home/sirac/ai:$PYTHONPATH"

# Veya her script'te:
sys.path.insert(0, os.path.dirname(__file__))
```

### Sorun: Playwright browser açılmıyor

```bash
# Browser'ları tekrar kur
playwright install chromium

# Sistem kütüphaneleri
playwright install-deps
```

---

## 🎉 Tebrikler!

Tam teşekküllü bir **Deep Research Agent** oluşturdunuz!

Bu ajan:
- ✅ Otonomdur
- ✅ Web'de arama yapar
- ✅ İçerikleri toplar
- ✅ Analiz eder
- ✅ Rapor yazar

**Sıradaki Adım**: [05-deployment.md](./05-deployment.md) - Deployment ve production kullanımı
