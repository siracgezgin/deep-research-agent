# 🎯 BURADAN BAŞLA - Proje Rehberi

**Hoş geldin!** Bu dosya sana projeyi **baştan sona** anlatacak.

---

## 📖 Hangi Dosyayı Ne Zaman Okuyacaksın?

### 1️⃣ İLK ÖNCE BU DOSYAYI OKU (şimdi okuyorsun ✅)
**Dosya:** `00-BASLA-BURADAN.md` (bu dosya)
- Proje nedir?
- Ne için yaptık?
- Nasıl çalışıyor?
- Teknik detaylar

### 2️⃣ HEMEN ÇALIŞTIRMAK İSTİYORSAN
**Dosya:** `QUICKSTART.md`
- 5 dakikada kurulum
- Hemen test et
- Komutlar

### 3️⃣ DERİNLEMESİNE ÖĞRENMEK İSTİYORSAN
**Klasör:** `docs/` içindeki dosyalar **SIRAYLA:**
1. `docs/01-setup.md` - Kurulum detayları
2. `docs/02-basic-agent.md` - Agent nasıl yapılır?
3. `docs/03-web-scraping.md` - Web'den veri çekme
4. `docs/04-research-agent.md` - Ana sistem nasıl çalışır?
5. `docs/05-deployment.md` - Yayına alma

### 4️⃣ KOD ÖRNEKLERİNİ GÖRMEK İSTİYORSAN
**Klasör:** `examples/` içindeki dosyalar **SIRAYLA:**
1. `hello_agent.py` - En basit (API test)
2. `01_simple_summarizer.py` - Basit agent
3. `02_agent_with_tools.py` - Tool kullanan agent
4. `03_sequential_agent.py` - Çok aşamalı agent
5. `04-06_...` - Web scraping örnekleri

### 5️⃣ ANA KODU İNCELEMEK İSTİYORSAN
**Klasör:** `src/` içindeki dosyalar
- `src/agents/planner_agent.py` - Plan yapan agent
- `src/agents/researcher_agent.py` - Araştıran agent
- `src/agents/writer_agent.py` - Rapor yazan agent
- `src/workflow/orchestrator.py` - Hepsini yöneten sistem
- `src/ui/app.py` - Web arayüzü

---

## 🎯 PROJE NEDİR? NE YAPAR?

### Basit Açıklama
**"Bir konu ver, otomatik araştırıp rapor yazsın"**

Örnek:
- Sen: "Yapay zeka etiği hakkında rapor istiyorum"
- Sistem: 
  1. Konuyu alt başlıklara böler (plan yapar)
  2. Her başlığı web'de araştırır
  3. Bulduklarını analiz eder
  4. Profesyonel rapor yazar
  5. Sana Markdown dosyası verir

### Teknik Açıklama
**Multi-Agent AI Research System**
- 3 farklı AI agent (Planner, Researcher, Writer)
- Web search (Tavily API)
- Web scraping (Crawl4AI)
- LLM analysis (Google Gemini)
- Streamlit UI

---

## 🤔 NE İÇİN YAPTIK? (AMAÇ)

### Staj Projesi İhtiyacı
**Martur şirketindeki staj için:**
- Modern AI teknolojilerini öğrenmek
- Autonomous agent sistemi yapmak
- Web scraping + LLM birleştirmek
- Gerçek dünya problemi çözmek

### Problem
İnsanlar araştırma yaparken:
- ❌ Çok zaman kaybediyor
- ❌ Kaynak bulmakta zorlanıyor
- ❌ Özet çıkarmakta zorlanıyor
- ❌ Rapor yazmak yorucu

### Çözüm
AI agent sistemi:
- ✅ Otomatik araştırır
- ✅ Kaynakları bulur
- ✅ Analiz eder
- ✅ Rapor yazar
- ✅ 10 dakikada bitirir

---

## 🏗️ SİSTEM NASIL ÇALIŞIR? (WORKFLOW)

### Adım Adım Akış

```
1. KULLANICI
   ↓
   "Kuantum bilgisayarlar hakkında araştırma yap"
   ↓

2. ORCHESTRATOR (Koordinatör)
   ↓
   "Tamam, işe başlıyorum"
   ↓

3. PLANNER AGENT
   ↓
   Konuyu analiz eder
   ↓
   Alt başlıklara böler:
   - Kuantum bilgisayar nedir?
   - Kullanım alanları
   - Zorluklar
   - Gelecek perspektifi
   ↓

4. RESEARCHER AGENT (Her başlık için)
   ↓
   a) Web'de ara (Tavily)
      → "Kuantum bilgisayar nedir" arar
      → 5 kaynak bulur
   ↓
   b) İçerikleri çek (Crawl4AI)
      → Her URL'yi ziyaret eder
      → HTML → Markdown'a çevirir
   ↓
   c) LLM ile analiz (Gemini)
      → İçerikleri okur
      → Önemli noktaları çıkarır
      → Özet yapar
   ↓

5. WRITER AGENT
   ↓
   Tüm bulguları alır
   ↓
   Profesyonel rapor yazar:
   - Başlık
   - Executive summary
   - Giriş
   - Ana bölümler
   - Sonuç
   - Kaynakça
   ↓

6. ORCHESTRATOR
   ↓
   Raporu kaydet:
   - report.md (Markdown)
   - research.json (Ham veri)
   ↓

7. KULLANICI
   ↓
   İndir ve oku!
```

---

## 🔧 KULLANILAN TEKNOLOJİLER

### 1. Google Gemini 2.5 Flash (LLM)
**Ne için?** Yapay zeka beyni
**Ne yapar?**
- Metinleri okur ve anlar
- Plan yapar
- Özet çıkarır
- Rapor yazar
- Soruları yanıtlar

**Neden Gemini?**
- ✅ Ücretsiz (20 req/gün)
- ✅ Hızlı
- ✅ Türkçe destekli
- ✅ Function calling (tool kullanır)

**Kod örneği:**
```python
import google.generativeai as genai
genai.configure(api_key="AIza...")

model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content("Özet çıkar: ...")
print(response.text)
```

---

### 2. Tavily API (Web Search)
**Ne için?** Google benzeri arama
**Ne yapar?**
- Konuyu web'de arar
- İlgili sayfaları bulur
- Snippet (özet) verir

**Neden Tavily?**
- ✅ AI için optimize
- ✅ Ücretsiz 1000 arama/ay
- ✅ Kaliteli sonuçlar
- ✅ Kolay API

**Alternatif:** Google Search API, Bing API

**Kod örneği:**
```python
from tavily import TavilyClient
client = TavilyClient(api_key="tvly-...")

results = client.search("AI etiği")
# → [{'title': '...', 'url': '...', 'content': '...'}]
```

**Not:** Tavily key yoksa mock data kullanıyoruz (test için)

---

### 3. Crawl4AI (Web Scraping)
**Ne için?** Web sayfalarından içerik çekme
**Ne yapar?**
- URL'yi ziyaret eder
- HTML'i okur
- Temiz text/markdown çıkarır
- JavaScript sayfaları render eder

**Neden Crawl4AI?**
- ✅ AI için optimize
- ✅ Async (hızlı)
- ✅ JavaScript desteği
- ✅ Kolay kullanım

**Alternatif:** BeautifulSoup, Scrapy, Selenium

**Kod örneği:**
```python
from crawl4ai import AsyncWebCrawler

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://example.com")
    print(result.markdown)  # Temiz text
```

---

### 4. Streamlit (Web UI)
**Ne için?** Kullanıcı arayüzü
**Ne yapar?**
- Web sayfası oluşturur
- Form gösterir (konu girişi)
- Progress bar
- Raporu gösterir
- İndirme butonu

**Neden Streamlit?**
- ✅ Python ile web app
- ✅ Çok hızlı geliştirme
- ✅ Modern görünüm
- ✅ Ücretsiz deployment

**Alternatif:** Flask, FastAPI, Gradio

**Kod örneği:**
```python
import streamlit as st

st.title("AI Research Agent")
topic = st.text_input("Konu:")
if st.button("Başlat"):
    st.write("Araştırılıyor...")
```

---

## 🧠 AGENT KAVRAMI

### Agent Nedir?
**Basit:** Kendisi karar veren, araç kullanan AI

**Fark:**
- **Normal LLM:** Sadece text üretir
- **Agent:** Araçlar kullanır (web ara, kod çalıştır, dosya oku)

**Örnek:**
```
KULLANICI: "Hava durumu nasıl?"

Normal LLM:
  → "Bilmiyorum, ben sadece textim"

Agent:
  → 1. Hava durumu API'sine bak
  → 2. Sonucu oku
  → 3. Kullanıcıya söyle
  → "İstanbul'da 15°C, yağmurlu"
```

---

### Bizim 3 Agent'ımız

#### 1️⃣ Planner Agent
**Görevi:** Konuyu alt başlıklara böl
**Input:** "Yapay zeka etiği"
**Output:** 
```json
{
  "subtopics": [
    "AI etiği nedir?",
    "Güncel sorunlar",
    "Çözüm önerileri"
  ]
}
```

**Dosya:** `src/agents/planner_agent.py`

---

#### 2️⃣ Researcher Agent
**Görevi:** Her başlığı araştır
**Input:** "AI etiği nedir?"
**Process:**
1. Tavily'de ara → 5 kaynak bul
2. Her kaynağı scrape et → İçerikleri al
3. Gemini ile analiz et → Özet çıkar

**Output:**
```json
{
  "topic": "AI etiği nedir?",
  "key_findings": [
    "Bulgu 1...",
    "Bulgu 2..."
  ],
  "summary": "AI etiği şu demektir..."
}
```

**Dosya:** `src/agents/researcher_agent.py`

---

#### 3️⃣ Writer Agent
**Görevi:** Rapor yaz
**Input:** Tüm araştırma sonuçları
**Output:** Markdown raporu

```markdown
# Yapay Zeka Etiği

## Executive Summary
...

## Giriş
...

## 1. AI Etiği Nedir?
...
```

**Dosya:** `src/agents/writer_agent.py`

---

### Orchestrator (Koordinatör)
**Görevi:** 3 agent'ı sırayla çalıştır

**Kod mantığı:**
```python
# 1. Plan yap
plan = planner.create_plan(topic)

# 2. Her başlığı araştır
results = []
for subtopic in plan['subtopics']:
    result = researcher.research(subtopic)
    results.append(result)

# 3. Rapor yaz
report = writer.write_report(plan, results)

# 4. Kaydet
save(report)
```

**Dosya:** `src/workflow/orchestrator.py`

---

## 📂 PROJE YAPISINI ANLAMA

```
ai/                              # Ana klasör
│
├── 00-BASLA-BURADAN.md         # ← Şu an buradasın
├── README.md                    # Proje özeti
├── QUICKSTART.md                # Hızlı başlangıç
├── FINAL_REPORT.md              # Detaylı rapor
│
├── main.py                      # ⭐ ANA ÇALIŞTIRICI
│   ├── UI mode    → python main.py
│   ├── CLI mode   → python main.py --cli "konu"
│   └── Test mode  → python main.py --test
│
├── requirements.txt             # Bağımlılıklar
├── .env                         # API anahtarları (gizli)
├── .env.example                 # Şablon
│
├── docs/                        # 📚 Rehberler (SIRAYLA OKU)
│   ├── 01-setup.md             # Kurulum
│   ├── 02-basic-agent.md       # Agent yapımı
│   ├── 03-web-scraping.md      # Scraping
│   ├── 04-research-agent.md    # Ana sistem
│   └── 05-deployment.md        # Deployment
│
├── examples/                    # 🎓 Öğrenme örnekleri (SIRAYLA)
│   ├── hello_agent.py          # 1. En basit
│   ├── 01_simple_summarizer.py # 2. Basit agent
│   ├── 02_agent_with_tools.py  # 3. Tool kullanan
│   ├── 03_sequential_agent.py  # 4. Multi-step
│   ├── 04_crawl4ai_basic.py    # 5. Scraping
│   ├── 05_crawl4ai_advanced.py # 6. Advanced
│   └── 06_llm_scraping_combo.py# 7. LLM+Scraping
│
├── src/                         # ⚙️ ANA KOD
│   │
│   ├── agents/                  # 3 ana agent
│   │   ├── planner_agent.py    # Planlayıcı
│   │   ├── researcher_agent.py # Araştırmacı
│   │   └── writer_agent.py     # Yazar
│   │
│   ├── tools/                   # Araçlar
│   │   └── web_tools.py        # Tavily + mock
│   │
│   ├── workflow/                # Workflow yönetimi
│   │   └── orchestrator.py     # Koordinatör
│   │
│   └── ui/                      # Web arayüzü
│       └── app.py              # Streamlit app
│
├── tests/                       # Test dosyaları
│   └── test_basic.py
│
├── output/                      # Üretilen raporlar
│   └── research_*.md
│
└── venv/                        # Python sanal ortamı
```

---

## 🔍 HER DOSYANIN AMACI

### Kök Klasördeki MD Dosyaları

| Dosya | Ne İçerir? | Ne Zaman Oku? |
|-------|-----------|---------------|
| `00-BASLA-BURADAN.md` | Bu dosya, her şey | İLK |
| `README.md` | Proje özeti, kurulum | İkinci |
| `QUICKSTART.md` | Hızlı başlangıç komutları | Hemen çalıştıracaksan |
| `TODO.md` | İlerleme takibi | Geliştirme yaparsan |
| `PROJECT_STRUCTURE.md` | Klasör yapısı | Klasörleri anlamak için |
| `PROJECT_COMPLETED.md` | Tamamlanma özeti | Proje bittiğinde |
| `FINAL_REPORT.md` | Detaylı rapor | Sunum için |

---

## 🎓 ÖĞRENME YOLU

### Seviye 1: Temel (1-2 saat)
1. ✅ Bu dosyayı oku (`00-BASLA-BURADAN.md`)
2. ✅ `QUICKSTART.md` ile çalıştır
3. ✅ `examples/hello_agent.py` dosyasını oku ve çalıştır
4. ✅ `examples/01_simple_summarizer.py` oku

**Hedef:** Basit agent nasıl çalışır anla

---

### Seviye 2: Orta (3-4 saat)
5. ✅ `docs/01-setup.md` oku
6. ✅ `docs/02-basic-agent.md` oku
7. ✅ `examples/02_agent_with_tools.py` oku ve çalıştır
8. ✅ `examples/03_sequential_agent.py` oku

**Hedef:** Tool kullanımı, workflow'lar

---

### Seviye 3: İleri (5-8 saat)
9. ✅ `docs/03-web-scraping.md` oku
10. ✅ `examples/04-06` scraping örneklerini oku
11. ✅ `docs/04-research-agent.md` oku
12. ✅ `src/agents/` klasöründeki 3 agent'ı incele
13. ✅ `src/workflow/orchestrator.py` incele

**Hedef:** Ana sistemi tam anla

---

### Seviye 4: Expert (10+ saat)
14. ✅ `src/ui/app.py` incele (Streamlit)
15. ✅ Kendi agent'ını yaz
16. ✅ Sisteme yeni özellik ekle
17. ✅ Deploy et

**Hedef:** Sistemi özelleştir

---

## 💡 TEMEL KAVRAMLAR

### 1. LLM (Large Language Model)
**Ne?** Büyük dil modeli (ChatGPT gibi)
**Bizde:** Google Gemini 2.5 Flash
**Görevi:** Text anlama, üretme, analiz

### 2. Agent
**Ne?** Araç kullanan AI
**Bizde:** 3 tane (Planner, Researcher, Writer)
**Görevi:** Bağımsız karar verme, araç kullanma

### 3. Tool/Function Calling
**Ne?** Agent'ın Python fonksiyonu çağırması
**Örnek:** `search_web("AI etiği")` çağırır
**Bizde:** Tavily search, Crawl4AI scraping

### 4. Orchestration
**Ne?** Birden fazla agent'ı koordine etme
**Bizde:** Orchestrator sınıfı
**Görevi:** Planner → Researcher → Writer sıralaması

### 5. Web Scraping
**Ne?** Web sitesinden veri çekme
**Bizde:** Crawl4AI kütüphanesi
**Görevi:** HTML → Markdown dönüşümü

### 6. RAG (Retrieval Augmented Generation)
**Ne?** LLM'e dış bilgi verme
**Bizde:** Web'den çekilen içerikler
**Görevi:** LLM'in güncel bilgiye erişimi

---

## 🚀 NASIL ÇALIŞTIRILIR?

### Yöntem 1: UI Mode (Tavsiye)
```bash
# Terminal'de
cd /home/sirac/ai
source venv/bin/activate
python main.py
```
→ Tarayıcıda http://localhost:8501 açılır
→ Konu gir, araştırma başlat

---

### Yöntem 2: CLI Mode
```bash
python main.py --cli "Kuantum bilgisayarların geleceği"
```
→ Terminal'de çalışır
→ Sonuçlar `output/` klasörüne kaydedilir

---

### Yöntem 3: Test Mode
```bash
python main.py --test
```
→ Hazır bir konu ile test eder
→ Tüm workflow'u çalıştırır

---

### Yöntem 4: Örnekleri Tek Tek Çalıştır
```bash
python examples/hello_agent.py
python examples/01_simple_summarizer.py
python examples/02b_agent_single_test.py
```

---

## ⚙️ SİSTEM GEREKSİNİMLERİ

### Yazılım
- ✅ Python 3.12+
- ✅ pip (paket yöneticisi)
- ✅ Virtual environment
- ✅ Playwright Chromium browser

### API Keys
- ✅ **ZORUNLU:** Google Gemini API key
  - Al: https://ai.google.dev/
  - Ücretsiz: 20 request/gün
  
- ⚪ **OPSİYONEL:** Tavily API key
  - Al: https://tavily.com/
  - Ücretsiz: 1000 request/ay
  - Yoksa mock data kullanılır

### Disk
- Kod: ~50 MB
- Python packages: ~315 MB
- Chromium browser: ~165 MB
- **Toplam:** ~530 MB

### RAM
- Minimum: 2 GB
- Önerilen: 4 GB

---

## 🐛 SORUN GİDERME

### "Rate limit" Hatası
**Sorun:** 429 quota exceeded
**Sebep:** Günlük 20 request limiti doldu
**Çözüm:** 
- Yarın tekrar dene (gece yarısı reset)
- Veya paid plan al ($0.15/1M token)

### "Module not found" Hatası
**Sorun:** `ModuleNotFoundError: No module named 'tavily'`
**Sebep:** Paket kurulmamış
**Çözüm:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "API key invalid" Hatası
**Sorun:** `Invalid API key`
**Sebep:** `.env` dosyasında yanlış key
**Çözüm:**
1. https://ai.google.dev/ → API key al
2. `.env` dosyasını aç
3. `GOOGLE_API_KEY=yeni_key` yaz

### Streamlit Açılmıyor
**Sorun:** `python main.py` çalışmıyor
**Sebep:** Streamlit kurulu değil
**Çözüm:**
```bash
pip install streamlit
python main.py
```

---

## 📊 PROJE METRİKLERİ

### Kod İstatistikleri
- Python dosyası: 21
- Toplam satır: ~3000+
- Fonksiyon: ~50+
- Sınıf: 4 (3 agent + orchestrator)

### Test Durumu
- ✅ Temel testler: Yapıldı
- ✅ Planner agent: Çalışıyor
- ✅ Tool usage: Çalışıyor
- ⏳ Full e2e: Yarın (quota)

### Özellikler
- ✅ Multi-agent sistem
- ✅ Web search
- ✅ Web scraping
- ✅ LLM analizi
- ✅ Report generation
- ✅ Streamlit UI
- ✅ CLI interface
- ✅ Progress tracking
- ✅ Error handling

---

## 🎯 SONRAKI ADIMLAR

### Kısa Vadeli (1 gün)
1. ✅ Tavily API key al (2 dakika)
2. ✅ `.env` dosyasına ekle
3. ✅ `python main.py --test` çalıştır
4. ✅ UI'da gerçek araştırma yap

### Orta Vadeli (1 hafta)
1. Kendi agent'ını yaz
2. Yeni tool ekle (örnek: Twitter search)
3. Farklı rapor formatları (PDF, HTML)
4. Daha fazla özelleştirme

### Uzun Vadeli (1 ay)
1. Docker ile deployment
2. Database entegrasyonu
3. Multi-user support
4. Advanced analytics

---

## 📚 EK KAYNAKLAR

### Kullandığımız Teknolojiler
- **Google Gemini:** https://ai.google.dev/
- **Tavily:** https://docs.tavily.com/
- **Crawl4AI:** https://docs.crawl4ai.com/
- **Streamlit:** https://docs.streamlit.io/

### Öğrenme Kaynakları
- **LangChain Tutorial:** Agent patterns
- **Google Colab:** Gemini examples
- **Streamlit Gallery:** UI örnekleri

### Bizim Dökümanlar
1. `docs/01-setup.md` - Kurulum
2. `docs/02-basic-agent.md` - Agent dev
3. `docs/03-web-scraping.md` - Scraping
4. `docs/04-research-agent.md` - Main system
5. `docs/05-deployment.md` - Deploy

---

## ✅ ÖZET CHECKLIST

Proje tam olarak anlamak için:

- [ ] Bu dosyayı baştan sona oku
- [ ] `QUICKSTART.md` ile sistemi çalıştır
- [ ] `examples/hello_agent.py` çalıştır ve kodunu incele
- [ ] `docs/02-basic-agent.md` oku
- [ ] `src/agents/planner_agent.py` kodunu oku
- [ ] `examples/02_agent_with_tools.py` oku
- [ ] `src/workflow/orchestrator.py` oku
- [ ] `python main.py` ile UI'ı başlat
- [ ] Tavily API key ekle
- [ ] Gerçek bir araştırma yap
- [ ] Üretilen raporu incele

---

## 🎉 TEBRIKLER!

Bu dosyayı okuduğunda:
- ✅ Proje nedir biliyorsun
- ✅ Ne için yapıldığını biliyorsun
- ✅ Nasıl çalıştığını biliyorsun
- ✅ Hangi teknolojileri kullandığımızı biliyorsun
- ✅ Nereden başlayacağını biliyorsun

**Şimdi ne yapmalısın?**
→ `QUICKSTART.md` aç ve sistemi çalıştır!

Başarılar! 🚀

---

**Hazırlayan:** AI Assistant + Sen  
**Tarih:** 12 Aralık 2024  
**Proje:** AI Deep Research Agent
