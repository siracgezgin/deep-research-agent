# 05 - Deployment ve Production Kullanımı

## 🎯 Bu Bölümde Neler Öğreneceğiz?

1. Geliştirme ortamından production'a geçiş
2. Web arayüzü ekleme (Streamlit)
3. Docker ile containerization
4. Maliyet optimizasyonu
5. Monitoring ve loglama
6. Best practices

---

## Adım 1: Streamlit Web Arayüzü

Terminal yerine kullanıcı dostu bir arayüz ekleyelim.

### Streamlit Kurulumu

```bash
pip install streamlit
```

### Dosya: `app.py` (Proje kök dizininde)

```python
"""
Martur Research Agent - Web Arayüzü
Streamlit ile basit ve kullanıcı dostu interface
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Proje path'ini ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from martur_research_agent import MarturResearchAgent

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Martur Research Agent",
    page_icon="🔍",
    layout="wide"
)

# CSS Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .stAlert {
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Başlık
st.markdown('<h1 class="main-header">🔍 Martur Deep Research Agent</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Ayarlar
with st.sidebar:
    st.header("⚙️ Ayarlar")
    
    st.subheader("Model Seçimi")
    planner_model = st.selectbox(
        "Planlayıcı Model",
        ["gemini-1.5-pro", "gemini-1.5-flash"],
        index=0
    )
    
    researcher_model = st.selectbox(
        "Araştırmacı Model",
        ["gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )
    
    st.subheader("Araştırma Parametreleri")
    max_sources = st.slider("Maksimum Kaynak Sayısı", 5, 20, 10)
    search_depth = st.radio("Arama Derinliği", ["Hızlı", "Detaylı"], index=1)
    
    st.markdown("---")
    st.info("💡 **İpucu:** Detaylı arama daha fazla zaman alır ama daha kapsamlı sonuç verir.")

# Ana alan
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Araştırma Konusu")
    
    # Örnek konular
    example_topics = [
        "Elektrikli araçlarda kullanılan batarya teknolojileri",
        "Otomotiv koltuklarında sürdürülebilir kumaş trendleri",
        "Hafif araç şasi malzemeleri ve karbon fiber uygulamaları",
        "Otonom araç sensör teknolojileri"
    ]
    
    selected_example = st.selectbox(
        "Örnek konular (veya aşağıya kendi konunuzu yazın):",
        ["Özel konu yazacağım"] + example_topics
    )
    
    if selected_example == "Özel konu yazacağım":
        topic = st.text_area(
            "Araştırma konunuzu detaylı bir şekilde yazın:",
            height=150,
            placeholder="Örnek: Elektrikli araçlarda kullanılan lityum-iyon bataryaların geri dönüşüm süreçlerini ve çevresel etkilerini araştır..."
        )
    else:
        topic = st.text_area(
            "Araştırma konusu:",
            value=selected_example,
            height=150
        )

with col2:
    st.subheader("📊 Önceki Araştırmalar")
    
    # Session state'te geçmiş araştırmaları sakla
    if 'research_history' not in st.session_state:
        st.session_state.research_history = []
    
    if st.session_state.research_history:
        for i, hist in enumerate(st.session_state.research_history[-5:]):  # Son 5
            with st.expander(f"🕐 {hist['timestamp'][:16]}"):
                st.write(f"**Konu:** {hist['topic'][:50]}...")
                if st.button(f"Tekrar Göster", key=f"show_{i}"):
                    st.session_state.show_old_report = hist['report']
    else:
        st.info("Henüz araştırma yapılmadı.")

# Araştırma butonu
st.markdown("---")
if st.button("🚀 Araştırmayı Başlat", type="primary", use_container_width=True):
    
    if not topic or topic.strip() == "":
        st.error("⚠️ Lütfen bir araştırma konusu girin!")
    else:
        # Progress bar
        with st.spinner("🔄 Araştırma yapılıyor..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Agent'ı oluştur
                status_text.text("📋 Agent hazırlanıyor...")
                progress_bar.progress(10)
                
                agent = MarturResearchAgent()
                
                # Araştırmayı başlat
                status_text.text("🔍 Plan oluşturuluyor...")
                progress_bar.progress(30)
                
                status_text.text("🌐 Web'de araştırma yapılıyor...")
                progress_bar.progress(50)
                
                result = agent.research(topic.strip())
                
                status_text.text("📝 Rapor yazılıyor...")
                progress_bar.progress(80)
                
                if result["success"]:
                    progress_bar.progress(100)
                    status_text.text("✅ Tamamlandı!")
                    
                    # Geçmişe ekle
                    st.session_state.research_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'topic': topic[:100],
                        'report': result['report']
                    })
                    
                    # Raporu göster
                    st.success("✅ Araştırma başarıyla tamamlandı!")
                    
                    # Tabs ile rapor gösterimi
                    tab1, tab2, tab3 = st.tabs(["📄 Rapor", "📥 İndir", "📊 Metadata"])
                    
                    with tab1:
                        st.markdown(result['report'])
                    
                    with tab2:
                        # Markdown olarak indir
                        st.download_button(
                            label="📥 Markdown olarak indir",
                            data=result['report'],
                            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                        
                        # PDF export için not
                        st.info("💡 PDF export için markdown dosyasını Pandoc veya başka bir araç ile dönüştürebilirsiniz.")
                    
                    with tab3:
                        st.json(result['metadata'])
                
                else:
                    st.error(f"❌ Araştırma başarısız: {result['error']}")
            
            except Exception as e:
                st.error(f"❌ Hata oluştu: {str(e)}")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>Martur Deep Research Agent v1.0 | Powered by Google ADK & Gemini | 2024</p>
    </div>
""", unsafe_allow_html=True)
```

### Çalıştırma

```bash
streamlit run app.py
```

Browser'da otomatik olarak açılacak: `http://localhost:8501`

---

## Adım 2: Docker ile Containerization

Production'da çalıştırmak için Docker container oluşturalım.

### Dosya: `Dockerfile`

```dockerfile
# Python base image
FROM python:3.10-slim

# Sistem bağımlılıkları (Playwright için)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Python bağımlılıklarını kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright browser'ı kur
RUN playwright install chromium

# Proje dosyalarını kopyala
COPY . .

# Port açıkla (Streamlit için)
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Streamlit'i başlat
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Dosya: `docker-compose.yml`

```yaml
version: '3.8'

services:
  martur-research-agent:
    build: .
    container_name: martur_research_agent
    ports:
      - "8501:8501"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs  # Log dosyaları için
      - ./reports:/app/reports  # Rapor çıktıları için
    restart: unless-stopped
    mem_limit: 2g  # Bellek limiti
    cpus: 2  # CPU limiti
```

### Docker ile Çalıştırma

```bash
# Image'i build et
docker-compose build

# Container'ı başlat
docker-compose up -d

# Logları izle
docker-compose logs -f

# Durdur
docker-compose down
```

---

## Adım 3: Maliyet Optimizasyonu

### LLM API Maliyetlerini Düşürme

| Strateji | Tasarruf | Uygulama |
|----------|----------|----------|
| Flash model kullan | %90 | Özetleme ve basit görevler için |
| Token sınırla | %50 | Scraping sonuçlarını kısalt (10k karakter) |
| Cache kullan | %80 | Aynı URL'i tekrar taramaktan kaçın |
| Batch işlem | %30 | Paralel scraping ile toplam süreyi düşür |

### Örnek: Caching Sistemi

```python
# src/utils/cache.py
import json
import hashlib
from datetime import datetime, timedelta

class SimpleCache:
    """Basit dosya tabanlı cache"""
    
    def __init__(self, cache_dir="./cache", ttl_hours=24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)
    
    def get(self, key: str):
        """Cache'den al"""
        cache_file = self._get_cache_file(key)
        
        if not os.path.exists(cache_file):
            return None
        
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        # TTL kontrolü
        cached_time = datetime.fromisoformat(data['timestamp'])
        if datetime.now() - cached_time > self.ttl:
            os.remove(cache_file)
            return None
        
        return data['value']
    
    def set(self, key: str, value: any):
        """Cache'e yaz"""
        cache_file = self._get_cache_file(key)
        
        with open(cache_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'value': value
            }, f)
    
    def _get_cache_file(self, key: str) -> str:
        """Key'den dosya adı oluştur"""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hash_key}.json")
```

---

## Adım 4: Monitoring ve Loglama

### Structured Logging

```python
# src/utils/logger.py
import logging
from datetime import datetime
import json

class StructuredLogger:
    """JSON formatında log tutan logger"""
    
    def __init__(self, name: str, log_file: str = "logs/agent.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Dosya handler
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
    
    def log(self, event: str, **kwargs):
        """Yapılandırılmış log kaydı"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            **kwargs
        }
        self.logger.info(json.dumps(log_entry))

# Kullanım
logger = StructuredLogger("MarturAgent")
logger.log("research_started", topic="Electric vehicles", user="sirac")
logger.log("scraping_completed", url="example.com", duration_ms=1234)
```

### Metrik Toplama

```python
# src/utils/metrics.py
from dataclasses import dataclass
from typing import List
import time

@dataclass
class ResearchMetrics:
    """Araştırma metrikleri"""
    topic: str
    start_time: float
    end_time: float
    total_urls_scraped: int
    total_searches: int
    report_word_count: int
    
    @property
    def duration_seconds(self) -> float:
        return self.end_time - self.start_time
    
    def to_dict(self):
        return {
            'topic': self.topic,
            'duration_seconds': self.duration_seconds,
            'urls_scraped': self.total_urls_scraped,
            'searches': self.total_searches,
            'report_words': self.report_word_count
        }

# Kullanım
start = time.time()
# ... araştırma ...
end = time.time()

metrics = ResearchMetrics(
    topic=topic,
    start_time=start,
    end_time=end,
    total_urls_scraped=15,
    total_searches=5,
    report_word_count=2500
)

print(f"Araştırma {metrics.duration_seconds:.1f} saniye sürdü")
```

---

## Adım 5: Production Best Practices

### 1. Hata Yönetimi

```python
# src/utils/error_handler.py
class ResearchError(Exception):
    """Özel hata sınıfı"""
    pass

def handle_research_error(func):
    """Decorator: Hataları yakala ve logla"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.log("error", function=func.__name__, error=str(e))
            # Kullanıcıya friendly mesaj
            return {
                'success': False,
                'error': 'Araştırma sırasında bir hata oluştu. Lütfen tekrar deneyin.'
            }
    return wrapper
```

### 2. Rate Limiting

```python
# src/utils/rate_limiter.py
import time
from collections import deque

class RateLimiter:
    """API rate limiti kontrol eder"""
    
    def __init__(self, max_calls: int, period_seconds: int):
        self.max_calls = max_calls
        self.period = period_seconds
        self.calls = deque()
    
    def wait_if_needed(self):
        """Gerekirse bekle"""
        now = time.time()
        
        # Eski çağrıları temizle
        while self.calls and self.calls[0] < now - self.period:
            self.calls.popleft()
        
        # Limit aşıldıysa bekle
        if len(self.calls) >= self.max_calls:
            sleep_time = self.period - (now - self.calls[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.calls.append(time.time())

# Kullanım
limiter = RateLimiter(max_calls=10, period_seconds=60)  # Dakikada 10 çağrı

for url in urls:
    limiter.wait_if_needed()
    scrape_url(url)
```

### 3. Konfigürasyon Yönetimi

```python
# src/config/settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Uygulama ayarları"""
    
    # API Keys
    google_api_key: str
    tavily_api_key: str
    
    # Model ayarları
    planner_model: str = "gemini-1.5-pro"
    researcher_model: str = "gemini-1.5-flash"
    writer_model: str = "gemini-1.5-pro"
    
    # Scraping ayarları
    max_concurrent_scrapes: int = 5
    scrape_timeout_seconds: int = 30
    
    # Araştırma ayarları
    max_search_results: int = 10
    max_research_iterations: int = 3
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Adım 6: CI/CD Pipeline (GitHub Actions)

### Dosya: `.github/workflows/deploy.yml`

```yaml
name: Deploy Martur Research Agent

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
      
      - name: Run tests
        run: |
          pytest tests/
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t martur-research-agent .
      
      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push martur-research-agent
```

---

## 🎯 Production Checklist

Canlıya almadan önce kontrol edin:

### Güvenlik
- [ ] API key'ler `.env` dosyasında ve `.gitignore`'da
- [ ] Docker secrets kullanılıyor
- [ ] Rate limiting aktif
- [ ] Input validation (XSS, injection vb.)

### Performance
- [ ] Caching sistemi çalışıyor
- [ ] Paralel scraping optimize edildi
- [ ] Token limitleri ayarlandı
- [ ] Timeout'lar ayarlandı

### Monitoring
- [ ] Structured logging aktif
- [ ] Metrik toplama çalışıyor
- [ ] Error tracking (Sentry vb.)
- [ ] Uptime monitoring

### Dokümantasyon
- [ ] README güncel
- [ ] API dokümantasyonu
- [ ] Deployment rehberi
- [ ] Troubleshooting guide

---

## 📊 Örnek Production Metrikleri

İlk hafta sonuçları (örnek):

| Metrik | Değer |
|--------|-------|
| Toplam araştırma | 127 |
| Ortalama süre | 2.3 dk |
| Başarı oranı | %94.5 |
| Ortalama kaynak | 12 site |
| Toplam maliyet | $8.40 |

---

## 🎉 Tebrikler!

Production'a hazır bir **Deep Research Agent** sistemini tamamladınız!

### Başardıklarınız

- ✅ Google ADK ile ajan mimarisi
- ✅ Web scraping altyapısı (Crawl4AI)
- ✅ Web arama entegrasyonu (Tavily)
- ✅ Streamlit web arayüzü
- ✅ Docker containerization
- ✅ Monitoring ve logging
- ✅ Production best practices

### Sonraki Adımlar

1. **Kendi verilerinizi ekleyin**: Martur'un iç dokümantasyonu, PDF'ler
2. **Multimodal yapın**: Görselleri, videoları da analiz edin
3. **Fine-tuning**: Spesifik domain için model fine-tune edin
4. **Chatbot entegrasyonu**: Slack/Teams bot'u yapın

---

## 📚 Ek Kaynaklar

- [Google ADK Docs](https://github.com/google/genai-agent-development-kit)
- [LangGraph Tutorial](https://langchain-ai.github.io/langgraph/)
- [Crawl4AI Examples](https://docs.crawl4ai.com/examples)
- [Streamlit Gallery](https://streamlit.io/gallery)

---

**İyi çalışmalar! 🚀**

*Sorularınız için: GitHub Issues veya internal Slack channel*
