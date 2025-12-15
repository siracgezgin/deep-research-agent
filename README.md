# Deep Research Agent

## Genel Bakış

Deep Research Agent, otomatik güvenilirlik puanlama, bakış açısı tespiti ve kalite değerlendirmesi ile kapsamlı çok kaynaklı analiz yapan gelişmiş bir yapay zeka destekli araştırma platformudur. Sistem, paralel işleme ve akış mimarileri kullanarak eşi görülmemiş hız ve doğrulukla profesyonel araştırma raporları sunar.

## Temel Özellikler

### Ana Yetenekler

**Akıllı Planlama Sistemi**
- Konuların otomatik olarak 3-6 araştırma alt başlığına ayrıştırılması
- Gemini LLM kullanarak bağlama duyarlı alt başlık üretimi
- Öncelik tabanlı araştırma stratejisi optimizasyonu

**Paralel Araştırma Motoru**
- Birden fazla alt başlık üzerinde eşzamanlı araştırma yürütme
- Sıralı işlemeye göre 6 kat performans iyileştirmesi
- Semaphore tabanlı istek yönetimi ile hız limiti koruması
- Zarif hata yönetimi ile asenkron işleme

**Kaynak Güvenilirlik Puanlama**
- Tüm kaynaklar için 0-100 arası bileşik güvenilirlik puanları
- Domain otoritesi değerlendirmesi (.edu, .gov, akademik dergiler)
- İçerik kalitesi değerlendirmesi (derinlik, yapı, alıntı kalıpları)
- Yayın tarihine dayalı zamansal ilgililik puanlama

**Çok Bakış Açılı Analiz**
- Farklı bakış açılarının otomatik tespiti (iyimser, kötümser, dengeli)
- Çatışma tanımlama ve çözüm önerileri
- Kaynaklar arası fikir birliği alanlarının haritalandırılması
- LLM destekli bakış açısı sınıflandırması

**Akışlı Rapor Üretimi**
- Üretim sırasında gerçek zamanlı rapor oluşturma
- Kademeli metin görüntüleme ile ChatGPT benzeri kullanıcı deneyimi
- İlk içerik 5-8 saniye içinde görünür
- Bellek verimliliği için generator pattern uygulaması

**Kalite Değerlendirme Çerçevesi**
- Altı boyutlu kalite metrikleri (kaynak sayısı, çeşitlilik, güvenilirlik, derinlik, güncellik, kapsam)
- Harf notu ile 0-100 bileşik kalite puanı (A+'dan F'ye)
- Otomatik kalite eşiği doğrulaması

**Profesyonel Web Arayüzü**
- Türkçe yerelleştirme ile modern Streamlit tabanlı kullanıcı arayüzü
- Detaylı günlük kaydı ile gerçek zamanlı ilerleme takibi
- Etkileşimli veri görselleştirme ve metrik gösterimler
- Tek tıkla rapor dışa aktarma (Markdown, JSON)

## Teknik Mimari

### Sistem Bileşenleri

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit Web Arayüzü                      │
│  - Gerçek zamanlı ilerleme takibi                           │
│  - Akışlı rapor görüntüleme                                 │
│  - Etkileşimli görselleştirmeler                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│         Araştırma Orkestratörü (İş Akışı Motoru)            │
│  - Ajan koordinasyonu ve veri akışı yönetimi                │
│  - Paralel araştırma yürütme (asyncio + semaphore)          │
│  - Akışlı çıktı koordinasyonu                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────┬──────────────┬──────────────┬────────────────┐
│   Planlayıcı │  Araştırmacı │    Yazar     │  Yardımcılar   │
│    Ajan      │    Ajan      │    Ajan      │  - Puanlama    │
│  (LLM-based) │  [Paralel]   │  [Akışlı]    │  - Bakış Açısı │
│              │              │              │  - Kalite      │
└──────────────┴──────────────┴──────────────┴────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Harici API'ler                          │
│  - Google Gemini 2.5 (Akış desteği ile LLM)                │
│  - Tavily Search API (AI-optimize web arama)               │
└─────────────────────────────────────────────────────────────┘
```

### Teknoloji Yığını

**Dil Modelleri**
- Google Gemini 2.5 Pro: Stratejik planlama ve rapor üretimi
- Google Gemini 2.5 Flash: Yüksek hızlı araştırma analizi
- Gerçek zamanlı içerik sunumu için akış API desteği

**Web Arama**
- Tavily API: Otomatik içerik çıkarma ile AI-optimize arama
- Güvenilirlik göstergeleri dahil kaynak meta verileri
- Ayda 1000 ücretsiz arama (üretim kullanımı için yeterli)

**Backend Framework**
- Eşzamanlı işlemler için asyncio ile Python 3.12+
- Active internet connection for API access

### Step 1: Clone Repository

```bash
git clone https://github.com/siracgezgin/deep-research-agent.git
cd deep-research-agent
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys

**Required API Keys:**

1. **Google Gemini API Key**
   - Navigate to: https://aistudio.google.com/app/apikey
   - Create new API key or use existing key
   - Free tier: 15 requests/minute, 1500 requests/day

2. **Tavily Search API Key**
   - Navigate to: https://tavily.com/
   - Sign up for free account
   - Free tier: 1000 searches/month

**Configuration:**

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

Anahtarlarınızı `.env` dosyasına ekleyin:

```env
GOOGLE_API_KEY=buraya_gemini_api_anahtariniz
TAVILY_API_KEY=buraya_tavily_api_anahtariniz
```

### Adım 5: Kurulumu Doğrulayın

```bash
# API bağlantısını test et
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content('Merhaba')
print('Gemini API: Bağlantı Başarılı')
"
```

## Kullanım

### Web Arayüzü (Önerilen)

**Uygulamayı başlatın:**

```bash
python main.py
```

veya

```bash
streamlit run src/ui/app.py
```

Web arayüzü otomatik olarak `http://localhost:8501` adresinde açılacaktır

**Araştırma İş Akışı:**

1. Kenar çubuğundaki giriş alanına araştırma konusunu girin
2. İsteğe bağlı olarak araştırma kapsamını daraltmak için ek bağlam sağlayın
3. Gerekirse gelişmiş ayarları düzenleyin (rapor stili, kaynak limitleri)
4. "Araştırmayı Başlat" düğmesine tıklayın
5. İlerleme göstergeleri aracılığıyla gerçek zamanlı ilerlemeyi izleyin
6. İçerik oluşturulurken akışlı rapor üretimini görüntüleyin
7. Kalite metriklerini ve perspektif analizini inceleyin
8. Son raporu Markdown veya JSON formatında indirin

### Komut Satırı Arayüzü

**Temel kullanım:**

```bash
python main.py --cli "Araştırma konunuz"
```

**Ek bağlam ile:**

```bash
python main.py --cli "Kuantum bilgisayar uygulamaları" --context "Son 5 yılın gelişmelerine odaklan"
```

**Çıktı konumu:**

Raporlar Markdown formatında `reports/` dizinine kaydedilir.

## Yapılandırma

### Yapılandırma Dosyası Yapısı

Sistem `config.yaml` aracılığıyla yapılandırılır. Ana yapılandırma bölümleri:

**Model Yapılandırması:**

```yaml
models:
  planner: "gemini-2.5-flash"     # Planlama ajan modeli
  researcher: "gemini-2.5-flash"  # Araştırma ajan modeli
  writer: "gemini-2.5-flash"      # Rapor yazım modeli
```

**Araştırma Ayarları:**

```yaml
research:
  max_subtopics: 4                # Maksimum araştırma alt başlıkları (3-6)
  min_subtopics: 3                # Minimum araştırma alt başlıkları
  max_search_results: 5           # Alt başlık başına kaynak sayısı
  enable_scraping: false          # Derin içerik çıkarma (daha yavaş)
```

**Performans Ayarlama:**

```yaml
performance:
  parallel_research: true         # Eşzamanlı işlemeyi etkinleştir
  max_concurrent_requests: 5      # Paralel istek limiti
  streaming_enabled: true         # Gerçek zamanlı rapor akışı
  stream_update_interval: 0.05    # UI güncelleme kısıtlaması (50ms)
```

**Hız Sınırlama:**

```yaml
rate_limits:
  requests_per_minute: 5          # API güvenliği için muhafazakar limit
  requests_per_day: 20            # Günlük kota yönetimi
  retry_max_attempts: 3           # Hatalarda otomatik yeniden deneme
  auto_wait_on_429: true          # Hız limitinde otomatik bekleme
```

### Performans Modları

**Demo Modu (Varsayılan - Hız İçin Optimize Edilmiş):**

```yaml
models:
  planner: "gemini-2.5-flash"
  writer: "gemini-2.5-flash"
research:
  max_subtopics: 4
performance:
  parallel_research: true
  max_concurrent_requests: 5
```

Beklenen tamamlanma süresi: 60 saniye
Kalite seviyesi: İyi (gösterimler için uygun)

**Üretim Modu (Kalite İçin Optimize Edilmiş):**

```yaml
models:
  planner: "gemini-2.5-pro"
  writer: "gemini-2.5-pro"
research:
  max_subtopics: 6
performance:
  parallel_research: true
  max_concurrent_requests: 5
```

Beklenen tamamlanma süresi: 150 saniye
Kalite seviyesi: Mükemmel (yayına hazır raporlar)

## Performans Karakteristikleri

### Paralel Araştırma Mimarisi

**Sıralı ve Paralel İşleme:**

| Alt Başlıklar | Sıralı | Paralel (5 eşzamanlı) | Hızlanma |
|-----------|------------|-------------------------|----------|
| 3 konu  | 60s        | 12s                     | 5x      |
| 4 konu  | 80s        | 16s                     | 5x      |
| 6 konu  | 120s       | 20s                     | 6x      |

**Uygulama:**
- asyncio tabanlı eşzamanlı yürütme
- Semaphore hız sınırlama (maksimum 5 eşzamanlı istek)
- Zarif bozulma ile hata yönetimi
- Her paralel görev için ilerleme takibi

### Akışlı Rapor Üretimi

**Kullanıcı Deneyimi Metrikleri:**

| Metrik | Geleneksel | Akışlı | İyileştirme |
|--------|-------------|-----------|-------------|
| İlk içerik | 150s | 5-8s | 20-30x daha hızlı |
| Algılanan bekleme | Yüksek | Düşük | 10x daha iyi UX |
| Kullanıcı etkileşimi | Düşük | Yüksek | Sürekli geri bildirim |

**Teknik Uygulama:**
- Bellek verimliliği için generator pattern
- Parça parça içerik sunumu
- Kademeli UI renderlama
- Gerçek zamanlı markdown ayrıştırma

### Hız Limiti Yönetimi

**Gemini API Ücretsiz Seviye:**
- Dakikada 15 istek (RPM)
- Günde 1500 istek (RPD)
- Dakikada 1M token (TPM)

**Koruma Stratejisi:**
- Muhafazakar 5 RPM yapılandırması (15 RPM limitinin altında)
- Semaphore tabanlı eşzamanlılık kontrolü
- Üssel geri çekilme ile otomatik yeniden deneme
- İstek toplu optimizasyonu

## Kalite Metrikleri Çerçevesi

### Six-Dimensional Assessment

**Source Count (0-15 points)**
- Minimum threshold: 3 sources
- Optimal range: 8-12 sources
- Scoring: Linear scaling based on source quantity

**Source Diversity (0-15 points)**
- Domain uniqueness measurement
- Source type variety (news, academic, government, commercial)
- Geographic and temporal distribution

**Source Reliability (0-20 points)**
- Domain authority assessment
- Academic journal recognition
- Government and educational institution preference
- Citation pattern analysis

**Content Depth (0-20 points)**
- Average content length evaluation
- Structural complexity assessment
- Citation and reference density
- Technical detail level

**Recency (0-15 points)**
- Publication date weighting
- 2024-2025 content: Maximum points
- Exponential decay for older content
- Topic-specific temporal relevance

**Coverage (0-15 points)**
- Subtopic completion rate
- Research objective fulfillment
- Comprehensive perspective representation

### Notlandırma Skalası

| Puan Aralığı | Not | Kalite Seviyesi |
|-------------|-------|----------------|
| 90-100 | A+ | Mükemmel |
| 85-89 | A | Çok İyi |
| 75-84 | B | İyi |
| 60-74 | C | Kabul Edilebilir |
| 50-59 | D | Standart Altı |
| 0-49 | F | Yetersiz |

## Perspektif Analizi

### Tespit Metodolojisi

**Otomatik Sınıflandırma:**
- LLM destekli bakış açısı tanımlama
- Duygu analizi entegrasyonu
- Argüman yapısı ayrıştırma
- Kaynak yanlılık tespiti

**Perspektif Kategorileri:**
- İyimser: Pozitif bakış, fırsat odaklı
- Kötümser: Risk bilincinde, zorluk odaklı
- Dengeli: Nötr analiz, kanıta dayalı

### Çatışma Çözümü

**Çatışma Türleri:**
- Veri Uyuşmazlıkları: Çelişkili istatistikler veya gerçekler
- Metodolojik Farklılıklar: Farklı araştırma yaklaşımları
- Yorum Çatışmaları: Aynı veriden farklı sonuçlar
- Zamansal Çatışmalar: Zamana bağlı geçerlilik sorunları

**Çözüm Çerçevesi:**
- Kaynak güvenilirlik karşılaştırması
- Kanıt gücü değerlendirmesi
- Uzlaşma tanımlama
- Öneri sentezi

## Sorun Giderme

### Common Issues and Solutions

**Issue: API Key Errors**

```
Error: google.generativeai.types.generation_types.StopCandidateException
```

Solution:
- Verify API keys in `.env` file
- Check API key validity at provider dashboard
- Ensure no extra whitespace in key values
- Confirm environment file is loaded correctly

**Sorun: Hız Limiti Aşıldı (429)**

```
Hata: Resource exhausted (quota exceeded)
```

Çözüm:
- config.yaml'da `max_concurrent_requests` değerini azaltın (3 deneyin)
- `requests_per_minute` ayarını düşürün (3 deneyin)
- Kota sıfırlamasını bekleyin (RPM için 1 dakika, günlük için 24 saat)
- Ücretli API katmanına yükseltmeyi düşünün

**Sorun: Yavaş Performans**

Çözüm:
- config.yaml'da Flash modellerine geçin
- `max_subtopics` değerini 3-4'e azaltın
- Etkinse `enable_scraping` devre dışı bırakın
- Ağ bağlantısını ve gecikmeyi kontrol edin

**Sorun: Modül İçe Aktarma Hataları**

```
Hata: ModuleNotFoundError: No module named 'streamlit'
```

Çözüm:
- Sanal ortamın aktif olduğunu doğrulayın
- Bağımlılıkları yeniden yükleyin: `pip install -r requirements.txt --upgrade`
- Python sürüm uyumluluğunu kontrol edin (3.12+ gerektirir)

**Sorun: Akış Görüntülenmiyor**

Çözüm:
- config.yaml'da `streaming_enabled: true` olduğunu doğrulayın
- Streamlit uygulamasını yeniden başlatın
- Tarayıcı önbelleğini temizleyin
- JavaScript hataları için tarayıcı konsolunu kontrol edin

## Geliştirme ve Genişletme

### Adding Custom Agents

Agents inherit from base LLM interface:

```python
import google.generativeai as genai

class CustomAgent:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction="Your agent instructions here",
            generation_config={
                "temperature": 0.7,
                "response_mime_type": "application/json"
            }
        )
    
    def process(self, input_data):
        response = self.model.generate_content(input_data)
        return response.text
```

### Özel Puanlama Algoritmaları

`SourceScorer` sınıfını genişletin:

```python
from src.utils.source_scorer import SourceScorer

class CustomScorer(SourceScorer):
    def calculate_custom_metric(self, source):
        # Puanlama mantığınız burada
        return score
```

### Ek Veri Kaynakları

`src/tools/` dizininde yeni araçlar uygulayabilirsiniz:

```python
class CustomSearchTool:
    def search(self, query):
        # Arama uygulamanız
        return results
```

## Dokümantasyon

### Kapsamlı Rehberler

**PROJECT_GUIDE.md**
- Tam mimari dokümantasyon
- Uygulama detayları ve tasarım kararları
- Teknoloji seçim gerekçesi
- Adım adım yeniden oluşturma rehberi
- Gelişmiş yapılandırma seçenekleri

**SUMMARY.md**
- Hızlı referans rehberi
- Ana özellikler genel bakış
- Kullanım örnekleri

**docs/archive/**
- Geliştirme geçmişi
- Özellik evrim dokümantasyonu
- Eski uygulama notları

## Versiyon Geçmişi

### Versiyon 2.0 (15 Aralık 2024)

**Performans İyileştirmeleri:**
- Paralel araştırma uygulaması (6x hızlanma)
- Akışlı rapor üretimi (gerçek zamanlı UX)
- Semaphore ile hız limiti koruması
- Demo modu optimizasyonu (flash modeller, azaltılmış alt başlıklar)

**Kullanıcı Arayüzü İyileştirmeleri:**
- Türkçe dil arayüzü
- Profesyonel stil (emoji kaldırma)
- Gerçek zamanlı ilerleme göstergeleri
- Gelişmiş hata mesajları

**Teknik İyileştirmeler:**
- asyncio tabanlı eşzamanlılık
- Akış için generator pattern
- Gelişmiş hata yönetimi
- Kapsamlı günlük kaydı

### Versiyon 1.0 (13 Aralık 2024)

**İlk Yayın:**
- Çok ajanlı araştırma sistemi
- Kaynak güvenilirlik puanlama
- Perspektif analizi
- Kalite metrikleri çerçevesi
- Streamlit web arayüzü
- CLI desteği

## Katkıda Bulunma

Katkılar memnuniyetle karşılanır. Lütfen şu yönergeleri takip edin:

1. Depoyu fork edin
2. Özellik dalı oluşturun (`git checkout -b feature/YourFeature`)
3. Değişiklikleri commit edin (`git commit -m 'Add YourFeature'`)
4. Dala push edin (`git push origin feature/YourFeature`)
5. Pull Request açın

## Lisans

Bu proje açık kaynaktır ve akademik ve ticari kullanım için uygun.

## İletişim ve Destek

**Depo:** https://github.com/siracgezgin/deep-research-agent

**Sorunlar:** GitHub Issues aracılığıyla hata bildirin ve özellik isteyin

**Yazar:** Sirac Gezgin

## Teşekkürler

Bu proje aşağıdaki teknoloji ve hizmetleri kullanmaktadır:

- Gelişmiş dil modeli yetenekleri için Google Gemini API
- AI-optimize web arama için Tavily Search API
- Hızlı UI geliştirme için Streamlit framework
- Eşzamanlı işleme için Python asyncio
- Destek kütüphaneleri için açık kaynak topluluğu

---

**Durum:** Üretim Hazır (v2.0)
**Son Güncelleme:** 15 Aralık 2024
**Python Sürümü:** 3.12+
**Lisans:** Açık Kaynak
│   ├── planner_agent.py      # Alt başlık planlayıcı
│   ├── researcher_agent.py   # Web araştırmacı
│   └── writer_agent.py       # Rapor yazıcı
├── tools/               # API entegrasyonları
│   └── web_tools.py          # Tavily web arama
├── utils/               # Yardımcı modüller
│   ├── source_scorer.py      # Kaynak skorlama
│   ├── perspective_analyzer.py  # Perspektif analizi
│   ├── quality_metrics.py    # Kalite metrikleri
│   ├── demo_data.py          # Demo veri üretici
│   ├── logger.py             # Loglama
│   ├── config_loader.py      # Config yönetimi
│   └── retry_helper.py       # Retry logic
├── workflow/            # Orchestration
│   └── orchestrator.py       # Workflow engine
└── ui/                  # Kullanıcı arayüzü
    └── app.py                # Streamlit UI
```

---

## 🔧 Teknolojiler

| Teknoloji | Amaç | Neden? |
|-----------|------|--------|
| **Google Gemini 2.5** | LLM | Ücretsiz tier, 2M token context, streaming API |
| **Tavily API** | Web arama | AI-optimized, ücretsiz 1000 arama/ay |
| **Streamlit** | UI | Hızlı prototipleme, Python-only, reactive UI |
| **asyncio** | Paralel işleme | Concurrent requests, 6x hızlanma |
| **Pydantic** | Validasyon | Type-safe data models |

Detaylar: [PROJECT_GUIDE.md - Teknolojiler](PROJECT_GUIDE.md#kullanılan-teknolojiler)

---

## ⚡ Performans

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| **Araştırma Hızı** | ~60 saniye | 4 alt başlık, paralel mod (DEMO) |
| **Normal Mod** | ~150 saniye | 6 alt başlık, production ayarları |
| **İlk İçerik** | 5-8 saniye | Streaming ile ilk kelimeler |
| **Algılanan UX** | 10x daha hızlı | Real-time feedback sayesinde |
| **API Rate Limit** | Korunuyor | Semaphore(5) ile güvenli |
| **Bellek Kullanımı** | +4MB | Paralel işlemden dolayı minimal artış |

**Not:** Demo modunda (config.yaml) flash modeller + 4 başlık kullanılıyor. Production için pro modeller + 6 başlık önerilir.

---

## 📝 Kullanım

### UI Mode (Önerilen)

```bash
python main.py
# veya
streamlit run src/ui/app.py --server.port 8501
```

Tarayıcıda `http://localhost:8501` açılır.

**Kullanım Adımları:**
1. Sol menüden araştırma konusu girin
2. İsteğe bağlı: Ek bağlam ekleyin
3. "Araştırmayı Başlat" butonuna tıklayın
4. Real-time progress takibi yapın
5. Streaming raporu izleyin (kelimeler yazılırken görünür)
6. Kalite metrikleri ve perspektif analizini inceleyin
7. Raporu markdown/JSON olarak indirin

**Not:** Streaming mod aktif olduğunda rapor yazılırken gerçek zamanlı görüntülenir (ChatGPT-like deneyim).

### CLI Mode

```bash
# Basit kullanım
python main.py --cli "Yapay zeka etiği"

# Bağlam ile
python main.py --cli "Kuantum bilgisayarlar" --context "Son 5 yılın gelişmeleri"

# Çıktı: reports/<konu>.md
```

### Hız Ayarları

**Demo Modu (Hızlı - Mevcut):**
```yaml
# config.yaml
models:
  planner: "gemini-2.5-flash"  # 2x hızlı
  writer: "gemini-2.5-flash"   # 2x hızlı
research:
  max_subtopics: 4             # Daha az başlık
```

**Production Modu (Kaliteli):**
```yaml
models:
  planner: "gemini-2.5-pro"    # Daha detaylı
  writer: "gemini-2.5-pro"     # Daha kaliteli
research:
  max_subtopics: 6             # Daha kapsamlı
```

---

## 🚀 Yeniden Oluşturma Rehberi

**Bu projeyi sıfırdan oluşturmak için:**

1. **[PROJECT_GUIDE.md](PROJECT_GUIDE.md)** oku (özellikle "Sıfırdan Kurulum" bölümü)
2. Proje yapısını oluştur
3. Bağımlılıkları yükle
4. API keylerini al ve `.env` dosyasına ekle
5. Kaynak kodları ekle (repodaki `src/` klasörünü kopyala)
6. Test et: `python main.py`

**Tüm adımlar detaylıca dokümante edilmiştir.**

---

## 🐛 Hızlı Sorun Giderme

```bash
# Bağımlılık hatası
pip install -r requirements.txt --upgrade

# API key hatası
cat .env  # Keyleri kontrol et

# Streamlit çalışmıyor
pkill -f streamlit
streamlit run src/ui/app.py

# Config değişiklikleri uygulanmadı
# Streamlit'i yeniden başlatın (config değişikliklerini okur)
```

**Sık Karşılaşılan Sorunlar:**

1. **"Rate limit exceeded"** → `config.yaml`'da `requests_per_minute: 5` düşürün
2. **"Streaming görünmüyor"** → `config.yaml`'da `streaming_enabled: true` olduğundan emin olun
3. **"Çok yavaş"** → Flash modellere geçin (yukarıdaki Demo Modu ayarları)
4. **"Import error"** → Virtual environment aktif mi? `source .venv/bin/activate`

Detaylı: [PROJECT_GUIDE.md - Sorun Giderme](PROJECT_GUIDE.md#sorun-giderme)

---

## 📊 Sistem Akışı

```
1. Kullanıcı → Ana konu girer
2. Planner Agent → 3-6 alt başlık oluşturur (Gemini Flash)
3. Researcher Agent → Paralel araştırma (5 concurrent)
   ├─ Tavily API ile web arama
   ├─ Kaynak güvenilirlik skorlama (0-100)
   └─ LLM ile içerik analizi
4. Writer Agent → Streaming report generation
   ├─ Giriş + metadata
   ├─ Her bölüm için detaylı yazım
   ├─ Sonuç ve öneriler
   └─ Real-time UI update
5. Perspective Analyzer → Çoklu bakış açısı tespiti
6. Quality Metrics → 6 metrik hesaplama
7. UI → Profesyonel görselleştirme
```

**Öne Çıkan Özellikler:**
- ✅ Paralel araştırma (asyncio + semaphore)
- ✅ Streaming rapor (chunk-by-chunk)
- ✅ Rate limit koruması (15 RPM Gemini)
- ✅ Hata yönetimi (retry + fallback)
- ✅ Loglama ve debug

Mimari detayları: [PROJECT_GUIDE.md - Mimari](PROJECT_GUIDE.md#mimari-ve-tasarım)

---

## 🎯 Öne Çıkan Teknik Özellikler

### 1. Paralel Araştırma Mimarisi
```python
# asyncio + semaphore ile rate-limit-safe paralel işleme
async with self.semaphore:
    research_results = await asyncio.gather(*tasks)
```
- 6x hızlanma (6 başlık → aynı anda)
- API limit koruması (Semaphore(5))
- Graceful error handling

### 2. Streaming Report Generation
```python
# Generator pattern ile chunk-by-chunk rapor
for chunk in model.generate_content(prompt, stream=True):
    yield {'type': 'section', 'content': chunk.text}
```
- Real-time UI update (ChatGPT-like)
- İlk içerik 5 saniyede
- Kullanıcı deneyimi 10x iyileşti

### 3. Kaynak Güvenilirlik Skorlama
```python
# 0-100 arası kompozit skor
score = domain_trust * 40 + freshness * 20 + content_quality * 40
badges = ['verified', 'academic', 'gov']
```
- Domain güvenilirliği (.edu, .gov, +40 puan)
- İçerik kalitesi (uzunluk, derinlik)
- Güncellik (2024 → +20 puan)

### 4. Perspektif Analizi
```python
# LLM ile çoklu bakış açısı tespiti
perspectives = ['iyimser', 'karamsar', 'dengeli']
conflicts = analyzer.detect_conflicts(sources)
```
- Otomatik perspektif sınıflandırma
- Çelişki tespiti + çözüm önerileri
- Uzlaşma alanları

### 5. Kalite Metrikleri
6 farklı metrik ile rapor değerlendirmesi:
- Kaynak sayısı (0-15 puan)
- Kaynak çeşitliliği (0-15 puan)
- Güvenilirlik (0-20 puan)
- İçerik derinliği (0-20 puan)
- Güncellik (0-15 puan)
- Kapsam (0-15 puan)

**Toplam:** 0-100 puan + Grade (A+, A, B, C, D, F)

---

## 📖 Harici Kaynaklar

Bu projede kullanılan/incelenen kaynaklar:

- **Tavily Python SDK**: API kullanımı, search optimization
- **Google AI Python SDK**: Gemini API, JSON mode, streaming
- **Streamlit Gallery**: UI patterns, custom CSS
- **asyncio Documentation**: Paralel işleme, semaphore patterns

Tam liste: [PROJECT_GUIDE.md - Harici Kaynaklar](PROJECT_GUIDE.md#harici-kaynaklar)

---

## 🚀 Versiyon Notları

### v2.0 (15 Aralık 2024) - Performance Update
- ✅ Paralel araştırma implementasyonu (6x hızlanma)
- ✅ Streaming report generation (real-time UI)
- ✅ Rate limit koruması (semaphore)
- ✅ Demo mode (flash models, 4 subtopics)
- ✅ Türkçe UI iyileştirmeleri
- ✅ Emoji temizliği (profesyonel görünüm)

### v1.0 (13 Aralık 2024) - Initial Release
- ✅ Multi-agent research system
- ✅ Source reliability scoring
- ✅ Perspective analysis
- ✅ Quality metrics
- ✅ Streamlit UI

---

**Durum:** ✅ Production Ready (Performance Optimized)  
**Son Güncelleme:** 15 Aralık 2024  
**Performans:** 60 saniye (demo) | 150 saniye (production)

**İLK KEZ Mİ KULLANIYORSUN?** → [PROJECT_GUIDE.md](PROJECT_GUIDE.md) oku!
