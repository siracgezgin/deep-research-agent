# 📁 Proje Yapısı

```
ai/
│
├── 📄 README.md                    # Ana proje açıklaması
├── 📄 QUICKSTART.md                # Hızlı başlangıç rehberi (BURADAN BAŞLA!)
├── 📄 TODO.md                      # İlerleme takibi
│
├── 📋 requirements.txt             # Python bağımlılıkları
├── 📋 .env.example                 # Örnek environment variables
├── 📋 .env                         # Gerçek API key'ler (GIT'E ATMA!)
├── 📋 .gitignore                   # Git ignore dosyası
│
├── 📂 docs/                        # 📚 DOKÜMANTASYON
│   ├── 01-setup.md                # Kurulum rehberi
│   ├── 02-basic-agent.md          # Temel ajan örnekleri
│   ├── 03-web-scraping.md         # Web scraping rehberi
│   ├── 04-research-agent.md       # Ana proje rehberi
│   └── 05-deployment.md           # Deployment rehberi
│
├── 📂 src/                         # 💻 ANA KAYNAK KODLAR
│   ├── __init__.py
│   │
│   ├── 📂 agents/                 # Ajan tanımları
│   │   ├── __init__.py
│   │   ├── planner_agent.py      # Konuyu alt başlıklara böler
│   │   ├── researcher_agent.py   # Web'de araştırır
│   │   ├── evaluator_agent.py    # Yeterlilik kontrolü
│   │   └── writer_agent.py       # Rapor yazar
│   │
│   ├── 📂 tools/                  # Custom tool'lar
│   │   ├── __init__.py
│   │   ├── search_tools.py       # Web arama (Tavily)
│   │   ├── scraping_tools.py     # Web scraping (Crawl4AI)
│   │   └── advanced_scraper.py   # Gelişmiş scraping
│   │
│   ├── 📂 config/                 # Konfigürasyon
│   │   └── settings.py           # Ayarlar (gelecekte)
│   │
│   ├── 📂 utils/                  # Yardımcı fonksiyonlar
│   │   ├── logger.py             # Loglama (gelecekte)
│   │   ├── cache.py              # Cache sistemi (gelecekte)
│   │   └── metrics.py            # Metrik toplama (gelecekte)
│   │
│   └── martur_research_agent.py  # 🎯 ANA AGENT
│
├── 📂 examples/                    # 🧪 ÖRNEK KODLAR
│   ├── hello_agent.py             # İlk test
│   ├── 01_simple_summarizer.py   # Basit özetleyici
│   ├── 02_agent_with_tools.py    # Tool kullanan ajan
│   ├── 03_sequential_agent.py    # Sıralı workflow
│   ├── 04_basic_scraping.py      # Basit scraping
│   ├── 05_parallel_scraping.py   # Paralel scraping
│   └── 06_agent_with_scraper.py  # Scraping + Agent
│
├── 📂 tests/                       # 🧪 TEST DOSYALARI
│   └── test_basic.py              # Temel testler
│
├── 📂 logs/                        # 📊 LOG DOSYALARI
│   └── agent.log                  # (Otomatik oluşur)
│
├── 📂 cache/                       # 💾 CACHE
│   └── *.json                     # (Otomatik oluşur)
│
├── 📂 reports/                     # 📄 OLUŞTURULAN RAPORLAR
│   └── *.md                       # (Otomatik oluşur)
│
├── 📄 app.py                      # 🌐 WEB ARAYÜZÜ (Streamlit)
│
├── 🐳 Dockerfile                  # Docker image
└── 🐳 docker-compose.yml          # Docker compose

```

## 📚 Hangi Dosya Ne İçin?

### Başlamak için:
1. **QUICKSTART.md** ← Buradan başla!
2. **docs/01-setup.md** ← Detaylı kurulum

### Öğrenmek için:
- **docs/02-basic-agent.md** ← Ajan nasıl yazılır?
- **docs/03-web-scraping.md** ← Web scraping nasıl yapılır?
- **docs/04-research-agent.md** ← Ana proje nasıl yapılır?

### Kod yazmak için:
- **src/agents/** ← Ajan kodları buraya
- **src/tools/** ← Tool kodları buraya
- **examples/** ← Test örnekleri buradan bakılır

### Deploy etmek için:
- **docs/05-deployment.md** ← Production rehberi
- **app.py** ← Web arayüzü
- **Dockerfile** ← Container

## 🎯 Dosya Oluşturma Sırası

Projeyi geliştirirken dosyaları bu sırayla oluşturacaksın:

### ✅ Zaten var olanlar:
- README.md
- QUICKSTART.md
- TODO.md
- requirements.txt
- .env.example
- Tüm docs/ klasörü
- examples/hello_agent.py

### 📝 Senin oluşturacağın dosyalar (sırayla):

1. **Hafta 1 - Temeller**
   ```
   src/tools/web_tools.py          # Basit web tools
   examples/01_simple_summarizer.py
   examples/02_agent_with_tools.py
   examples/03_sequential_agent.py
   ```

2. **Hafta 1-2 - Scraping**
   ```
   src/tools/advanced_scraper.py
   src/tools/scraping_tools.py
   examples/04_basic_scraping.py
   examples/05_parallel_scraping.py
   examples/06_agent_with_scraper.py
   ```

3. **Hafta 2 - Ana Proje**
   ```
   src/tools/search_tools.py       # Tavily entegrasyonu
   src/agents/planner_agent.py
   src/agents/researcher_agent.py
   src/agents/evaluator_agent.py
   src/agents/writer_agent.py
   src/martur_research_agent.py    # ANA DOSYA!
   ```

4. **Hafta 2-3 - İyileştirmeler (Opsiyonel)**
   ```
   src/utils/logger.py
   src/utils/cache.py
   src/utils/metrics.py
   src/config/settings.py
   app.py                          # Streamlit UI
   Dockerfile
   docker-compose.yml
   ```

## 💡 İpuçları

- **Boş klasörler** (`logs/`, `cache/`, `reports/`) otomatik doldurulacak
- **`.env` dosyasını** kesinlikle Git'e atma!
- **TODO.md** dosyasını her gün güncelle
- **examples/** klasöründeki dosyalar seni yönlendirecek
- Her adımda **testlerini yap**

---

**Şimdi ne yapmalısın?**

1. ✅ Bu dosyayı okudum
2. 👉 **QUICKSTART.md** dosyasını aç ve adımları takip et!

İyi çalışmalar! 🚀
