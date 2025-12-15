# 01 - Temel Kurulum Rehberi

## 🎯 Bu Bölümde Neler Yapacağız?

1. Python ortamını hazırlayacağız
2. Google ADK'yı kuracağız
3. Gerekli API key'leri alacağız
4. İlk test ajanımızı çalıştıracağız

---

## Adım 1: Python Ortamı Hazırlama

### Sistem Gereksinimleri
- Python 3.10 veya üstü
- pip (Python paket yöneticisi)
- Git

### Kurulum

```bash
# Mevcut Python versiyonunu kontrol et
python3 --version
# Çıktı: Python 3.10.x veya üstü olmalı

# Proje dizinine git
cd /home/sirac/ai

# Sanal ortam oluştur
python3 -m venv venv

# Sanal ortamı aktifleştir
source venv/bin/activate

# pip'i güncelle
pip install --upgrade pip
```

---

## Adım 2: Google ADK Kurulumu

Google ADK, Google'ın kendi yapay zeka ajanları geliştirmek için kullandığı framework'ün açık kaynak versiyonudur.

```bash
# Google ADK'yı kur
pip install google-genai-adk

# Crawl4AI'yı kur (web scraping için)
pip install crawl4ai[all]

# Playwright'ı kur (browser automation için)
playwright install chromium

# Diğer yardımcı kütüphaneler
pip install python-dotenv requests tavily-python
```

### Kurulum Kontrolü

```bash
python -c "import google.adk; print('ADK version:', google.adk.__version__)"
python -c "import crawl4ai; print('Crawl4AI kurulumu başarılı!')"
```

---

## Adım 3: API Key'leri Alma

### 3.1 Google Gemini API Key

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine git
2. Google hesabınla giriş yap
3. "Create API Key" butonuna tıkla
4. API key'i kopyala (güvenli bir yere kaydet)

**Önemli**: Bu key'i asla GitHub'a pushlama!

### 3.2 Tavily Search API Key (Opsiyonel ama Önerilen)

Tavily, web araması için optimize edilmiş bir API. Ücretsiz tier'ı ayda 1000 sorgu sunuyor.

1. [Tavily](https://tavily.com) adresine git
2. "Get API Key" ile üye ol
3. API key'i al

### 3.3 Environment Variables Ayarlama

```bash
# .env dosyası oluştur
cat > .env << 'EOF'
# Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here

# Tavily Search API (opsiyonel)
TAVILY_API_KEY=your_tavily_api_key_here

# Genel ayarlar
LOG_LEVEL=INFO
MAX_CONCURRENT_SCRAPES=5
EOF

# .env dosyasını düzenle
nano .env
# veya
code .env
```

**API key'lerini yukarıdaki `your_..._here` kısımlarına yapıştır.**

---

## Adım 4: İlk Test - "Hello World" Ajanı

Kurulumun doğru çalıştığını test etmek için basit bir ajan oluşturalım.

### Dosya: `examples/hello_agent.py`

Bu dosyayı bir sonraki adımda oluşturacağız, ama önce ne yapacağını anlayalım:

```python
"""
İlk test ajanımız - Gemini modeli ile basit sohbet
"""

import os
from dotenv import load_dotenv
from google.genai import types

# Environment variables'ı yükle
load_dotenv()

# Basit bir test
def test_gemini_connection():
    """Gemini API'ye bağlantıyı test eder"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ HATA: GOOGLE_API_KEY bulunamadı!")
        print("Lütfen .env dosyasını kontrol edin.")
        return False
    
    print("✅ API Key bulundu")
    print("🚀 Gemini ile bağlantı test ediliyor...")
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents='Merhaba! Bu bir test mesajıdır. Kısaca kendini tanıt.'
        )
        
        print("\n✅ Bağlantı başarılı!")
        print(f"\n🤖 Gemini'nin yanıtı:\n{response.text}\n")
        return True
        
    except Exception as e:
        print(f"\n❌ HATA: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("GOOGLE GEMINI API TEST")
    print("=" * 60)
    test_gemini_connection()
```

---

## Adım 5: Kurulumu Doğrulama

Aşağıdaki komutu çalıştırarak tüm kurulumu test edin:

```bash
# Test scriptini çalıştır
python examples/hello_agent.py
```

### Beklenen Çıktı

```
============================================================
GOOGLE GEMINI API TEST
============================================================
✅ API Key bulundu
🚀 Gemini ile bağlantı test ediliyor...

✅ Bağlantı başarılı!

🤖 Gemini'nin yanıtı:
Merhaba! Ben Gemini, Google AI tarafından geliştirilen büyük bir dil modeliyim...
```

---

## Sık Karşılaşılan Sorunlar ve Çözümleri

### Sorun 1: ModuleNotFoundError: No module named 'google.adk'

**Çözüm**:
```bash
# Sanal ortamın aktif olduğundan emin ol
source venv/bin/activate

# ADK'yı tekrar kur
pip install --force-reinstall google-genai-adk
```

### Sorun 2: Playwright kurulumunda hata

**Çözüm**:
```bash
# Playwright browser'ları manuel kur
python -m playwright install chromium

# Eğer sistem kütüphaneleri eksikse
python -m playwright install-deps
```

### Sorun 3: API Key geçersiz hatası

**Çözüm**:
1. `.env` dosyasındaki key'i kontrol et (başında/sonunda boşluk olmamalı)
2. API key'in Google AI Studio'dan doğru kopyalandığından emin ol
3. Key'in aktif olduğunu Google AI Studio'dan kontrol et

---

## 📝 Kontrol Listesi

Devam etmeden önce bunların hepsini tamamladığınızdan emin olun:

- [ ] Python 3.10+ kurulu
- [ ] Sanal ortam oluşturuldu ve aktif
- [ ] Google ADK kuruldu
- [ ] Crawl4AI kuruldu
- [ ] Playwright browser'ları kuruldu
- [ ] `.env` dosyası oluşturuldu ve API key'ler eklendi
- [ ] `hello_agent.py` başarıyla çalıştı

---

## 🎉 Tebrikler!

Temel kurulumu tamamladınız! Artık Google ADK ile ajan geliştirmeye hazırsınız.

**Sıradaki Adım**: [02-basic-agent.md](./02-basic-agent.md) - İlk gerçek ajanınızı oluşturacaksınız.
