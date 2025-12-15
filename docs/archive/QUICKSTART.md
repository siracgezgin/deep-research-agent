# 🚀 HIZLI BAŞLANGIÇ REHBERİ

Martur Deep Research Agent projesine hoş geldiniz! Bu rehber size ilk 30 dakikada sistemi çalıştırmanız için adım adım yol gösterecek.

---

## ⚡ Hızlı Kurulum (10 dakika)

### 1. Python Ortamı

```bash
# Sanal ortam oluştur
cd /home/sirac/ai
python3 -m venv venv

# Aktifleştir
source venv/bin/activate

# Bağımlılıkları kur
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. API Key'leri Al

#### Google Gemini (Zorunlu)
1. Git: https://makersuite.google.com/app/apikey
2. "Create API Key" tıkla
3. Key'i kopyala

#### Tavily Search (Zorunlu)
1. Git: https://tavily.com
2. Üye ol (ücretsiz)
3. Dashboard'dan API key al

### 3. Environment Dosyası

```bash
# .env.example'dan kopyala
cp .env.example .env

# Düzenle ve key'leri ekle
nano .env
```

`.env` dosyasında sadece bu iki satırı doldur:
```
GOOGLE_API_KEY=buraya_gemini_key_yapıştır
TAVILY_API_KEY=buraya_tavily_key_yapıştır
```

### 4. Playwright Browser Kur

```bash
playwright install chromium
```

### 5. İlk Test

```bash
python examples/hello_agent.py
```

✅ Eğer "Bağlantı başarılı!" görüyorsan, kurulum tamam!

---

## 📚 Dokümantasyon Sırası

Projeyi anlamak için dokümantasyonu bu sırayla oku:

### Gün 1: Temeller
1. ✅ `docs/01-setup.md` - Detaylı kurulum
2. ✅ `docs/02-basic-agent.md` - İlk ajanını yaz
3. 🧪 `examples/01_simple_summarizer.py` - Basit özetleyici

### Gün 2: Web Scraping
4. ✅ `docs/03-web-scraping.md` - Crawl4AI kullanımı
5. 🧪 `examples/04_basic_scraping.py` - İlk scraping
6. 🧪 `examples/05_parallel_scraping.py` - Paralel tarama

### Gün 3-4: Ana Proje
7. ✅ `docs/04-research-agent.md` - Deep Research Agent
8. 💻 `src/martur_research_agent.py` - Ana kodu yaz
9. 🧪 Test et ve geliştir

### Gün 5: Production
10. ✅ `docs/05-deployment.md` - Deployment rehberi
11. 💻 `app.py` - Streamlit arayüzü ekle

---

## 🎯 İlk Hafta Hedefleri

### Minimum Viable Product (MVP)
- [ ] Basit bir konu verebilme
- [ ] 5-10 site tarayabilme
- [ ] Markdown rapor üretebilme

### Ekstra Özellikler (Zaman varsa)
- [ ] Streamlit arayüzü
- [ ] Paralel scraping optimizasyonu
- [ ] PDF export
- [ ] Sonuç cache'leme

---

## 💡 Sık Sorulan Sorular

### "ModuleNotFoundError: No module named 'google.adk'"

Google ADK henüz PyPI'da olmayabilir. İki seçenek:

**Seçenek 1**: LangGraph kullan (daha stabil)
```bash
pip install langgraph langchain-google-genai
```

**Seçenek 2**: ADK'yı GitHub'dan kur
```bash
pip install git+https://github.com/google/genai-agent-development-kit.git
```

### "Playwright browser açılmıyor"

```bash
# Browser'ları tekrar kur
playwright install chromium

# Sistem kütüphaneleri (Linux)
playwright install-deps
```

### "API quota exceeded"

Gemini'nin ücretsiz tier'ı sınırlıdır:
- Flash: 15 request/dakika
- Pro: 2 request/dakika

Çözüm: İstekler arası `time.sleep(2)` ekle

---

## 🔧 Hızlı Test Komutları

```bash
# API bağlantısı
python examples/hello_agent.py

# Web scraping
python examples/04_basic_scraping.py

# Tavily arama
python src/tools/search_tools.py

# Ana agent (olması gereken)
python src/martur_research_agent.py

# Web arayüzü
streamlit run app.py
```

---

## 📞 Yardım

Takıldığın yerde:

1. **Dokümantasyonu tekrar oku**: `docs/` klasöründe her şey detaylı
2. **Error mesajını oku**: Çoğu hata mesajı çözümü söyler
3. **Logları kontrol et**: `logs/agent.log` dosyasına bak
4. **Mentor ile paylaş**: Hatayı ve ne yaptığını açıkla

---

## ✅ Kurulum Checklist

Başlamadan önce bunların hepsini işaretle:

- [ ] Python 3.10+ kurulu (`python3 --version`)
- [ ] Sanal ortam oluşturuldu (`venv` klasörü var)
- [ ] `requirements.txt` kuruldu (hata yok)
- [ ] Playwright browser kurulu
- [ ] `.env` dosyası var ve key'ler eklendi
- [ ] `hello_agent.py` çalıştı
- [ ] İlk dokümantasyon okundu

**Hepsi ✅ ise → `docs/01-setup.md` ile başla!**

---

## 🎉 Başarılar!

Kolay gelsin, güzel bir proje olacak! 🚀

*Son güncelleme: 12 Aralık 2024*
