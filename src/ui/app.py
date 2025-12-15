"""
Streamlit Web UI - Deep Research Agent
======================================

Kullanıcı dostu arayüz:
- Konu girişi
- Real-time progress tracking
- Sonuçları görüntüleme
- Rapor indirme
"""

import streamlit as st
import asyncio
import sys
import os
from datetime import datetime

# Proje root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.workflow.orchestrator import ResearchOrchestrator


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="AI Deep Research Agent | Martur Staj Projesi",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# AI Deep Research Agent\nYapay zeka destekli kapsamlı araştırma platformu.\n\n**Özellikler:**\n- Kaynak güvenilirlik skorlama\n- Perspektif analizi\n- Kalite değerlendirmesi"
    }
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

/* Global Styles */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Main Title */
.big-title {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #d4af37 0%, #7f8c3a 50%, #556b2f 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
    text-align: center;
}

/* Subtitle */
.subtitle {
    font-size: 1.3rem;
    color: #64748b;
    margin-bottom: 2rem;
    text-align: center;
    font-weight: 400;
}

/* Feature Badge */
.feature-badge {
    display: inline-block;
    background: linear-gradient(135deg, #d4af3715 0%, #7f8c3a15 100%);
    border: 1px solid #d4af3730;
    border-radius: 20px;
    padding: 6px 16px;
    margin: 4px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #7f8c3a;
}

/* Quality Score Card */
.quality-card {
    background: linear-gradient(135deg, #d4af37 0%, #7f8c3a 100%);
    border-radius: 16px;
    padding: 24px;
    color: white;
    text-align: center;
    box-shadow: 0 10px 40px rgba(212, 175, 55, 0.3);
}

.quality-score {
    font-size: 3.5rem;
    font-weight: 900;
    margin: 0;
}

.quality-label {
    font-size: 1rem;
    opacity: 0.9;
    margin-top: 8px;
    font-weight: 600;
}

/* Metric Cards */
.metric-card {
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: #d4af37;
    box-shadow: 0 8px 24px rgba(212, 175, 55, 0.15);
    transform: translateY(-3px);
}

/* Source Badge */
.source-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f1f5f9;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 4px;
}

.source-badge.high {
    background: #dcfce7;
    color: #166534;
    border: 1px solid #86efac;
}

.source-badge.medium {
    background: #fef3c7;
    color: #854d0e;
    border: 1px solid #fde047;
}

.source-badge.low {
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #fca5a5;
}

/* Stage Badges */
.stage-badge {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 12px;
    font-weight: bold;
    font-size: 0.9rem;
}

.stage-planning { background: #4F46E5; color: white; }
.stage-researching { background: #0891B2; color: white; }
.stage-writing { background: #059669; color: white; }
.stage-done { background: #16A34A; color: white; }

/* Streamlit Overrides */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: #f8fafc;
    border-radius: 8px 8px 0 0;
    padding: 0 24px;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #d4af3715 0%, #7f8c3a15 100%);
    border-bottom: 3px solid #d4af37;
}

.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3);
}

/* Text Area Enhancements */
.stTextArea textarea {
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    resize: vertical !important;
    min-height: 120px !important;
}

.stTextArea [data-baseweb="textarea"] {
    min-height: 120px !important;
}

/* Sidebar Width */
[data-testid="stSidebar"] {
    min-width: 350px !important;
    max-width: 400px !important;
}

[data-testid="stSidebar"] .block-container {
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
# =============================================================================

if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = ResearchOrchestrator()

if 'results' not in st.session_state:
    st.session_state.results = None

if 'running' not in st.session_state:
    st.session_state.running = False

# Config'i session_state'e yükle
if 'config' not in st.session_state:
    from src.utils.config_loader import config as config_loader
    st.session_state.config = config_loader.get_all()


# =============================================================================
# MAIN UI
# =============================================================================

def main():
    # Header - Professional
    st.markdown('<div class="big-title">AI Deep Research Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Yapay zeka destekli, kaynak doğrulamalı, çok perspektifli araştırma platformu</div>', unsafe_allow_html=True)
    
    # Feature badges
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <span class="feature-badge">Kaynak Güvenilirlik Skorlama</span>
        <span class="feature-badge">Perspektif Analizi</span>
        <span class="feature-badge">Kalite Değerlendirmesi</span>
        <span class="feature-badge">Derin Araştırma</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Sidebar - Input
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0; margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #1e293b; letter-spacing: -0.01em;">Araştırma Ayarları</div>
        </div>
        """, unsafe_allow_html=True)
        
        topic = st.text_area(
            "Araştırma Konusu",
            placeholder="Örnek: Kuantum bilgisayarların geleceği ve yapay zeka uygulamaları",
            height=120,
            help="Araştırmak istediğiniz konuyu detaylı yazın",
            key="topic_input"
        )
        
        context = st.text_area(
            "Ek Bağlam (Opsiyonel)",
            placeholder="Örnek: Son 5 yılın gelişmelerine odaklan, pratik uygulamalar dahil",
            height=100,
            help="Araştırmaya yön vermek için ek bilgiler",
            key="context_input"
        )
        
        st.markdown("---")
        
        # Options
        with st.expander("Gelişmiş Ayarlar", expanded=False):
            style = st.selectbox(
                "Rapor Stili",
                ["professional", "academic", "casual"],
                help="Raporun yazım tarzı"
            )
            
            max_sources = st.slider(
                "Maksimum Kaynak",
                min_value=3,
                max_value=10,
                value=5,
                help="Her alt başlık için kaç kaynak taranacak"
            )
            
            scrape_content = st.checkbox(
                "İçerik Scraping",
                value=False,
                help="URL içeriklerini detaylı scrape et (yavaş ama kapsamlı)"
            )
        
        st.markdown("---")
        
        # Start button - Hero style
        start_button = st.button(
            "Araştırmayı Başlat",
            type="primary",
            disabled=st.session_state.running or not topic,
            use_container_width=True
        )
        
        if start_button:
            st.session_state.running = True
            st.session_state.results = None
            st.rerun()
    
    # Main content area
    if st.session_state.running:
        show_research_progress(topic, context)
    elif st.session_state.results:
        show_results(st.session_state.results)
    else:
        show_welcome()


def show_welcome():
    """İlk ekran"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. Planlama")
        st.write("Konunuzu alt başlıklara böler ve araştırma planı oluşturur.")
    
    with col2:
        st.markdown("### 2. Araştırma")
        st.write("Her alt başlık için web'de arama yapar, kaynakları analiz eder.")
    
    with col3:
        st.markdown("### 3. Yazım")
        st.write("Tüm bulguları derleyerek profesyonel rapor üretir.")
    
    st.divider()
    
    st.info("Sol menüden konunuzu girin ve araştırmayı başlatın!")
    
    # Example topics
    st.markdown("### Örnek Konular")
    
    examples = [
        "Yapay zeka etiği ve toplumsal etkileri",
        "Gen düzenleme teknolojilerinin geleceği",
        "İklim değişikliği ve yenilenebilir enerji çözümleri",
        "mRNA aşı teknolojisi ve yeni uygulamalar",
        "Otonom araçların yasal ve etik boyutları"
    ]
    
    cols = st.columns(2)
    for i, example in enumerate(examples):
        with cols[i % 2]:
            st.markdown(f"- {example}")


def show_research_progress(topic, context):
    """Araştırma progress ekranı"""
    
    st.markdown("### Araştırma Devam Ediyor...")
    
    # Progress placeholder
    progress_bar = st.progress(0)
    status_text = st.empty()
    stage_container = st.empty()
    
    # Log area
    log_expander = st.expander("Detaylı Log", expanded=False)
    log_text = log_expander.empty()
    
    # Config'den streaming ayarını al
    config = st.session_state.get('config', {})
    use_streaming = config.get('performance', {}).get('streaming_enabled', True)
    
    # Rapor container (her zaman tanımlı)
    st.markdown("---")
    
    # Streaming durumunu göster
    if use_streaming:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-left: 4px solid #3b82f6; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
            <div style="font-weight: 600; color: #1e40af; font-size: 0.95rem;">
                Gerçek Zamanlı Rapor Üretimi Aktif
            </div>
            <div style="color: #3730a3; font-size: 0.85rem; margin-top: 4px;">
                Rapor içeriği oluşturulurken ekranda görüntülenecektir
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Araştırma Raporu")
    report_container = st.empty()
    
    # İlk mesaj - Professional
    report_container.markdown("""
    <div style="background: linear-gradient(135deg, #fafaf9 0%, #f5f5f4 100%); border: 2px solid #e7e5e4; border-radius: 12px; padding: 32px; text-align: center;">
        <div style="font-size: 1.1rem; font-weight: 600; color: #57534e; margin-bottom: 8px;">
            Rapor Üretimi Bekleniyor
        </div>
        <div style="color: #78716c; font-size: 0.9rem; line-height: 1.6;">
            Araştırma aşaması devam etmektedir. Veri toplama ve analiz tamamlandıktan sonra rapor yazımına başlanacaktır.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Run research
    async def run_async():
        logs = []
        
        def progress_callback(stage, progress):
            progress_bar.progress(progress / 100)
            
            # Stage badge
            stage_badges = {
                'planning': '<span class="stage-badge stage-planning">PLANLAMA</span>',
                'researching': '<span class="stage-badge stage-researching">ARAŞTIRMA</span>',
                'writing': '<span class="stage-badge stage-writing">RAPOR YAZIMI</span>',
                'done': '<span class="stage-badge stage-done">TAMAMLANDI</span>'
            }
            
            stage_container.markdown(stage_badges.get(stage, ''), unsafe_allow_html=True)
            status_text.text(f"{progress}% tamamlandı")
            
            logs.append(f"[{stage.upper()}] {progress}%")
            log_text.code("\n".join(logs[-20:]))  # Son 20 log
        
        # Streaming veya normal mode
        if use_streaming:
            # STREAMING MODE
            full_report = ""
            final_results = None
            
            # Stage badges
            stage_badges = {
                'planning': '<span class="stage-badge stage-planning">PLANLAMA</span>',
                'researching': '<span class="stage-badge stage-researching">ARAŞTIRMA</span>',
                'writing': '<span class="stage-badge stage-writing">RAPOR YAZIMI</span>',
                'done': '<span class="stage-badge stage-done">TAMAMLANDI</span>'
            }
            
            async for update in st.session_state.orchestrator.run_research_streaming(
                topic=topic,
                context=context,
                progress_callback=progress_callback
            ):
                stage = update.get('stage')
                update_type = update.get('type')
                data = update.get('data', {})
                
                # Update stage badge
                if stage in stage_badges:
                    stage_container.markdown(stage_badges[stage], unsafe_allow_html=True)
                
                # Progress updates
                if update_type == 'status':
                    message = data.get('message', '')
                    logs.append(message)
                    log_text.code("\n".join(logs[-20:]))
                    
                    if 'progress' in data:
                        progress_bar.progress(data['progress'] / 100)
                        status_text.text(f"{data['progress']}% tamamlandı")
                
                # Plan ready
                elif update_type == 'plan':
                    logs.append(data.get('message', ''))
                    log_text.code("\n".join(logs[-20:]))
                
                # Research complete
                elif update_type == 'research':
                    logs.append(data.get('message', ''))
                    log_text.code("\n".join(logs[-20:]))
                    # Araştırma tamamlandı, yazım başlıyor
                    report_container.markdown("""
                    <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border: 2px solid #6ee7b7; border-radius: 12px; padding: 32px; text-align: center;">
                        <div style="font-size: 1.2rem; font-weight: 700; color: #065f46; margin-bottom: 8px;">
                            Araştırma Aşaması Tamamlandı
                        </div>
                        <div style="color: #047857; font-size: 0.95rem; line-height: 1.6;">
                            Veri analizi sonuçlandı. Kapsamlı rapor oluşturuluyor...
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Report chunks (STREAMING!)
                elif update_type == 'report_chunk':
                    chunk = data
                    
                    # Metin chunk'ları - REAL-TIME RENDER
                    if chunk['type'] in ['metadata', 'intro', 'section', 'conclusion']:
                        full_report += chunk['content']
                        # Update UI in real-time
                        report_container.markdown(full_report)
                    
                    # Status updates from writer
                    elif chunk['type'] == 'status':
                        logs.append(chunk['content'])
                        log_text.code("\n".join(logs[-20:]))
                
                # Final result
                elif update_type == 'final':
                    final_results = data
                    logs.append(data.get('message', '✅ Tamamlandı!'))
                    log_text.code("\n".join(logs[-20:]))
                
                # Error
                elif update_type == 'error':
                    raise Exception(data.get('error', 'Unknown error'))
            
            return final_results
        
        else:
            # NORMAL MODE (non-streaming)
            results = await st.session_state.orchestrator.run_research(
                topic=topic,
                context=context,
                progress_callback=progress_callback
            )
            
            return results
    
    # Asyncio event loop
    try:
        results = asyncio.run(run_async())
        
        st.session_state.results = results
        st.session_state.running = False
        
        st.success("Araştırma tamamlandı!")
        
        # Auto rerun to show results
        st.rerun()
        
    except Exception as e:
        st.error(f"Hata: {e}")
        st.session_state.running = False


def show_results(results):
    """Sonuçları göster (kalite metrikleri + perspektifler dahil) - PROFESSIONAL"""
    
    if not results.get('success'):
        st.error(f"Araştırma başarısız: {results.get('error')}")
        return
    
    # Header
    st.success("Araştırma başarıyla tamamlandı!")
    
    # =========================================================================
    # KALITE METRİKLERİ - PROFESSIONAL CARD DESIGN
    # =========================================================================
    if results.get('quality_metrics'):
        qm = results['quality_metrics']
        
        st.markdown("### Rapor Kalite Değerlendirmesi")
        st.markdown("---")
        
        # Main quality card (hero)
        col_hero, col_metrics = st.columns([1, 2])
        
        with col_hero:
            score = qm['overall_score']
            grade = qm['grade']
            
            # Gradient color based on score
            if score >= 90:
                gradient = "linear-gradient(135deg, #10b981 0%, #059669 100%)"
            elif score >= 75:
                gradient = "linear-gradient(135deg, #d4af37 0%, #7f8c3a 100%)"
            elif score >= 60:
                gradient = "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"
            else:
                gradient = "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
            
            st.markdown(f"""
            <div style="background: {gradient}; border-radius: 20px; padding: 32px; text-align: center; box-shadow: 0 10px 40px rgba(212, 175, 55, 0.3);">
                <div style="font-size: 1.2rem; font-weight: 700; color: white; opacity: 0.9; margin-bottom: 16px;">KALİTE SKORU</div>
                <div style="font-size: 4rem; font-weight: 900; color: white; margin: 16px 0;">{score}</div>
                <div style="font-size: 1.5rem; font-weight: 600; color: white; opacity: 0.95;">/ 100</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: white; margin-top: 16px; padding: 8px 24px; background: rgba(255,255,255,0.2); border-radius: 12px; display: inline-block;">{grade}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metrics:
            st.markdown("#### Detaylı Metrikler")
            
            # Metric breakdown - Modern cards
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            metrics_data = [
                ("Kaynak Sayısı", qm['metrics']['source_count'], 15, "#d4af37"),
                ("Çeşitlilik", qm['metrics']['source_diversity'], 15, "#7f8c3a"),
                ("Güvenilirlik", qm['metrics']['source_reliability'], 20, "#10b981"),
                ("İçerik Derinliği", qm['metrics']['content_depth'], 20, "#f59e0b"),
                ("Güncellik", qm['metrics']['recency'], 15, "#0ea5e9"),
                ("Kapsam", qm['metrics']['coverage'], 15, "#556b2f"),
            ]
            
            for i, (label, value, max_val, color) in enumerate(metrics_data):
                col = [metric_col1, metric_col2, metric_col3][i % 3]
                with col:
                    percentage = (value / max_val) * 100
                    st.markdown(f"""
                    <div style="background: white; border: 2px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 12px; transition: all 0.3s ease;">
                        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">{label}</div>
                        <div style="font-size: 1.8rem; font-weight: 700; color: {color};">{value}<span style="font-size: 1rem; color: #94a3b8;">/{max_val}</span></div>
                        <div style="background: #e2e8f0; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;">
                            <div style="background: {color}; height: 100%; width: {percentage}%; border-radius: 3px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # =========================================================================
    # PERSPEKTİF ANALİZİ - PROFESSIONAL DESIGN
    # =========================================================================
    if results.get('perspectives') and results['perspectives'].get('has_conflict'):
        persp = results['perspectives']
        
        st.markdown("### Çoklu Perspektif Analizi")
        
        # Info card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-left: 4px solid #7f8c3a; border-radius: 12px; padding: 20px; margin: 20px 0;">
            <div style="font-size: 1.1rem; font-weight: 600; color: #365314;">
                Bu konuda <strong>{len(persp['perspectives'])} farklı bakış açısı</strong> ve <strong>{len(persp.get('conflicts', []))} çelişki</strong> tespit edildi.
            </div>
            <div style="font-size: 0.95rem; color: #4d7c0f; margin-top: 8px;">
                Dengeli bir analiz için tüm perspektifleri inceleyiniz.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Perspective cards - Modern tabs
        st.markdown("#### Perspektifler")
        perspective_tabs = st.tabs([f"{p['label'].title()}" for p in persp['perspectives']])
        
        for i, p in enumerate(persp['perspectives']):
            with perspective_tabs[i]:
                # Icon based on label
                icon_map = {
                    'iyimser': '+',
                    'karamsar': '-',
                    'dengeli': '=',
                    'optimistic': '+',
                    'pessimistic': '-',
                    'balanced': '=',
                }
                icon = icon_map.get(p['label'].lower(), '·')
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 16px; padding: 24px; margin: 16px 0;">
                    <div style="font-size: 2rem; font-weight: 900; color: #7f8c3a; margin-bottom: 12px;">{icon}</div>
                    <h3 style="color: #1e293b; margin-bottom: 16px;">{p['label'].upper()} BAKIŞ AÇISI</h3>
                    <p style="font-size: 1.05rem; color: #475569; line-height: 1.7; margin-bottom: 20px;">{p['summary']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("##### Ana Argümanlar")
                for idx, point in enumerate(p['key_points'], 1):
                    st.markdown(f"""
                    <div style="background: white; border-left: 3px solid #d4af37; padding: 12px 16px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        <strong>{idx}.</strong> {point}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("##### Kaynaklar")
                
                # Get actual source URLs from perspective sources list
                source_urls = []
                if isinstance(p.get('sources'), list):
                    for src in p['sources'][:6]:  # İlk 6 kaynak
                        # If source is a full URL, use it; otherwise try to find it in research results
                        if isinstance(src, str) and (src.startswith('http') or src.startswith('www')):
                            source_urls.append(src)
                        else:
                            # Try to find the URL from research results based on title/reference
                            for res in results.get('research_results', []):
                                if res.get('scored_sources'):
                                    for scored_src in res['scored_sources']:
                                        if src.lower() in scored_src.get('title', '').lower() or src.lower() in scored_src.get('url', '').lower():
                                            source_urls.append(scored_src['url'])
                                            break
                                if len(source_urls) >= 6:
                                    break
                
                # If no URLs found, get some from research results
                if not source_urls and results.get('research_results'):
                    for res in results.get('research_results', []):
                        if res.get('scored_sources'):
                            for scored_src in res['scored_sources'][:2]:
                                source_urls.append(scored_src['url'])
                        if len(source_urls) >= 6:
                            break
                
                cols = st.columns(2)
                for idx, source_url in enumerate(source_urls[:6]):
                    with cols[idx % 2]:
                        display_url = source_url if len(source_url) < 80 else source_url[:77] + '...'
                        st.markdown(f"""
                        <div style="background: #f8fafc; padding: 10px; border-radius: 8px; font-size: 0.8rem; margin: 4px 0; border-left: 3px solid #d4af37; word-break: break-all; font-family: monospace;">
                            <a href="{source_url}" target="_blank" style="color: #7f8c3a; text-decoration: none;">{display_url}</a>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Çelişkiler - Professional conflict cards
        if persp.get('conflicts'):
            st.markdown("#### Tespit Edilen Çelişkiler")
            
            for idx, conflict in enumerate(persp['conflicts'], 1):
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 16px; padding: 24px; margin: 20px 0; border-left: 5px solid #f59e0b;">
                    <div style="font-size: 1.3rem; font-weight: 700; color: #92400e; margin-bottom: 12px;">
                        {idx}. {conflict['conflict_type'].replace('_', ' ').title()}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get actual URLs for sources_a
                    sources_a_urls = []
                    for src_ref in conflict.get('sources_a', [])[:2]:
                        if src_ref.startswith('http'):
                            sources_a_urls.append(src_ref)
                        else:
                            # Try to find URL from research results
                            for res in results.get('research_results', []):
                                if res.get('scored_sources'):
                                    for scored in res['scored_sources']:
                                        if src_ref.lower() in scored.get('title', '').lower() or src_ref in str(scored.get('url', '')):
                                            sources_a_urls.append(scored['url'])
                                            break
                                if sources_a_urls:
                                    break
                    
                    sources_a_html = '<br>'.join([f'<a href="{url}" target="_blank" style="color: #991b1b; font-size: 0.75rem; word-break: break-all;">{url[:60]}...</a>' for url in sources_a_urls]) if sources_a_urls else 'Kaynak bilgisi bulunamadı'
                    
                    st.markdown(f"""
                    <div style="background: #fee2e2; border: 2px solid #fca5a5; border-radius: 12px; padding: 18px; height: 100%;">
                        <div style="font-weight: 700; color: #991b1b; margin-bottom: 10px; font-size: 1.1rem;">İddia A</div>
                        <div style="color: #7f1d1d; line-height: 1.6;">{conflict['claim_a']}</div>
                        <div style="margin-top: 12px; font-size: 0.85rem; color: #991b1b;">
                            <strong>Kaynaklar:</strong><br>{sources_a_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Get actual URLs for sources_b
                    sources_b_urls = []
                    for src_ref in conflict.get('sources_b', [])[:2]:
                        if src_ref.startswith('http'):
                            sources_b_urls.append(src_ref)
                        else:
                            # Try to find URL from research results
                            for res in results.get('research_results', []):
                                if res.get('scored_sources'):
                                    for scored in res['scored_sources']:
                                        if src_ref.lower() in scored.get('title', '').lower() or src_ref in str(scored.get('url', '')):
                                            sources_b_urls.append(scored['url'])
                                            break
                                if sources_b_urls:
                                    break
                    
                    sources_b_html = '<br>'.join([f'<a href="{url}" target="_blank" style="color: #166534; font-size: 0.75rem; word-break: break-all;">{url[:60]}...</a>' for url in sources_b_urls]) if sources_b_urls else 'Kaynak bilgisi bulunamadı'
                    
                    st.markdown(f"""
                    <div style="background: #dcfce7; border: 2px solid #86efac; border-radius: 12px; padding: 18px; height: 100%;">
                        <div style="font-weight: 700; color: #166534; margin-bottom: 10px; font-size: 1.1rem;">İddia B</div>
                        <div style="color: #14532d; line-height: 1.6;">{conflict['claim_b']}</div>
                        <div style="margin-top: 12px; font-size: 0.85rem; color: #166534;">
                            <strong>Kaynaklar:</strong><br>{sources_b_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-radius: 12px; padding: 18px; margin-top: 12px; border-left: 4px solid #0ea5e9;">
                    <div style="font-weight: 700; color: #075985; margin-bottom: 8px;">Çözüm Önerisi</div>
                    <div style="color: #0c4a6e; line-height: 1.6;">{conflict['resolution']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
        
        # Uzlaşma alanları - Success cards
        if persp.get('consensus_areas'):
            st.markdown("#### Ortak Uzlaşı Alanları")
            
            cols = st.columns(2)
            for idx, consensus in enumerate(persp['consensus_areas']):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border: 2px solid #6ee7b7; border-radius: 12px; padding: 16px; margin: 8px 0;">
                        <div style="color: #064e3b; font-weight: 600; line-height: 1.5;">{consensus}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # =========================================================================
    # METADATA - MODERN STATS CARDS
    # =========================================================================
    st.markdown("### Araştırma İstatistikleri")
    
    # Subtopic titles list
    subtopic_titles = [st['title'] for st in results.get('plan', {}).get('subtopics', [])]
    subtopics_display = f"{len(subtopic_titles)} başlık" if subtopic_titles else results['metadata']['subtopics_count']
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats_data = [
        ("Alt Başlık", subtopics_display, "#d4af37"),
        ("Süre", f"{results['metadata']['duration_seconds']:.1f}s", "#7f8c3a"),
        ("Rapor", f"{len(results['report']):,} char", "#10b981"),
        ("Kaynaklar", results['metadata'].get('sources_analyzed', 'N/A'), "#556b2f"),
    ]
    
    for (label, value, color), col in zip(stats_data, [col1, col2, col3, col4]):
        with col:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}15 0%, {color}25 100%); border: 2px solid {color}40; border-radius: 14px; padding: 20px; text-align: center;">
                <div style="font-size: 0.9rem; color: #64748b; font-weight: 600; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.05em;">{label}</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: {color};">{value}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Show subtopic list if available
    if subtopic_titles:
        st.markdown("#### Alt Başlıklar")
        cols = st.columns(2)
        for idx, title in enumerate(subtopic_titles):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fafaf9 0%, #f5f5f4 100%); border-left: 3px solid #d4af37; padding: 12px 16px; margin: 6px 0; border-radius: 8px; font-weight: 500; color: #292524;">
                    {idx + 1}. {title}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # =========================================================================
    # TABS
    # =========================================================================
    tab1, tab2, tab3, tab4 = st.tabs(["Rapor", "Plan", "Araştırma Detayları", "İndir"])
    
    with tab1:
        st.markdown("### Final Rapor")
        st.markdown(results['report'])
    
    with tab2:
        st.markdown("### Araştırma Planı")
        
        plan = results['plan']
        st.markdown(f"**Konu:** {plan['topic']}")
        st.markdown(f"**Açıklama:** {plan['description']}")
        
        st.markdown("#### Alt Başlıklar")
        for i, subtopic in enumerate(plan['subtopics'], 1):
            with st.expander(f"{i}. {subtopic['title']}"):
                st.write(f"**Soru:** {subtopic['question']}")
                st.write(f"**Kaynak Türü:** {subtopic['source_type']}")
                st.write(f"**Öncelik:** {subtopic['priority']}/5")
    
    with tab3:
        st.markdown("### Detaylı Kaynak Analizi")
        
        for i, result in enumerate(results['research_results'], 1):
            with st.expander(f"{i}. {result.get('subtopic_title', 'N/A')}", expanded=(i==1)):
                # Header
                confidence = result.get('confidence', 0)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                    <div style="font-weight: 700; font-size: 1.1rem; color: #1e293b; margin-bottom: 8px;">{result['topic']}</div>
                    <div style="color: #64748b;">Güven Seviyesi: {confidence}/5</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Kaynak skorları - Modern badges
                if result.get('scored_sources'):
                    st.markdown("#### Kaynaklar ve Güvenilirlik Skorları")
                    
                    for idx, source in enumerate(result['scored_sources'][:8], 1):  # İlk 8 kaynak
                        score = source['score']
                        trust = source['trust_level']
                        badges = ' '.join(source.get('badges', []))
                        
                        # Trust level styling
                        if trust == 'high':
                            badge_color = "#10b981"
                            badge_bg = "#d1fae5"
                            trust_icon = "HIGH"
                        elif trust == 'medium':
                            badge_color = "#f59e0b"
                            badge_bg = "#fef3c7"
                            trust_icon = "MED"
                        else:
                            badge_color = "#ef4444"
                            badge_bg = "#fee2e2"
                            trust_icon = "LOW"
                        
                        st.markdown(f"""
                        <div style="background: white; border: 2px solid {badge_color}30; border-radius: 10px; padding: 14px; margin: 10px 0;">
                            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                                <div style="background: {badge_bg}; color: {badge_color}; border: 2px solid {badge_color}; border-radius: 8px; padding: 4px 12px; font-weight: 700; font-size: 0.95rem;">
                                    {trust_icon} {score}/100
                                </div>
                                <div style="font-size: 0.85rem; color: #64748b;">
                                    {badges}
                                </div>
                            </div>
                            <div style="font-size: 0.85rem; color: #1e293b; word-break: break-all; font-family: monospace; margin-top: 8px;">
                                <a href="{source['url']}" target="_blank" style="color: #0ea5e9; text-decoration: none;">{source['url']}</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Key findings
                if 'key_findings' in result:
                    st.markdown("#### Ana Bulgular")
                    for finding in result['key_findings']:
                        st.markdown(f"""
                        <div style="background: #f0f9ff; border-left: 3px solid #0ea5e9; padding: 12px 16px; margin: 8px 0; border-radius: 8px;">
                            {finding}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Summary
                if 'summary' in result:
                    st.markdown("#### Özet")
                    st.markdown(f"""
                    <div style="background: #fafaf9; border: 2px solid #e7e5e4; border-radius: 12px; padding: 18px; line-height: 1.7; color: #292524;">
                        {result['summary']}
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### Araştırma Sonuçlarını İndir")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <div style="font-size: 1.1rem; font-weight: 600; color: #075985; margin-bottom: 8px;">
                Araştırma sonuçlarınızı farklı formatlarda indirebilirsiniz
            </div>
            <div style="font-size: 0.95rem; color: #0c4a6e;">
                Tüm kalite metrikleri, perspektif analizleri ve kaynak bilgileri dahildir.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Download options in cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: white; border: 2px solid #d4af37; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 16px;">
                <div style="font-weight: 700; color: #7f8c3a; font-size: 1.1rem; margin-bottom: 8px;">Markdown Rapor</div>
                <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 16px;">İnsan okunabilir format</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.download_button(
                label="MD İndir",
                data=results['report'],
                file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            st.markdown("""
            <div style="background: white; border: 2px solid #7f8c3a; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 16px;">
                <div style="font-weight: 700; color: #556b2f; font-size: 1.1rem; margin-bottom: 8px;">Tüm Veriler</div>
                <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 16px;">Yapılandırılmış JSON</div>
            </div>
            """, unsafe_allow_html=True)
            
            import json
            json_data = json.dumps(results, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="JSON İndir",
                data=json_data,
                file_name=f"research_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            st.markdown("""
            <div style="background: white; border: 2px solid #10b981; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 16px;">
                <div style="font-weight: 700; color: #065f46; font-size: 1.1rem; margin-bottom: 8px;">Araştırma Planı</div>
                <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 16px;">Plan + Alt başlıklar</div>
            </div>
            """, unsafe_allow_html=True)
            
            plan_json = json.dumps(results.get('plan', {}), indent=2, ensure_ascii=False)
            
            st.download_button(
                label="Plan İndir",
                data=plan_json,
                file_name=f"research_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Quality and Perspectives (if available)
        if results.get('quality_metrics') or results.get('perspectives'):
            st.markdown("---")
            st.markdown("#### Gelişmiş Analizler")
            
            adv_col1, adv_col2 = st.columns(2)
            
            if results.get('quality_metrics'):
                with adv_col1:
                    quality_json = json.dumps(results['quality_metrics'], indent=2, ensure_ascii=False)
                    st.download_button(
                        label="Kalite Metrikleri (JSON)",
                        data=quality_json,
                        file_name=f"quality_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
            
            if results.get('perspectives'):
                with adv_col2:
                    persp_json = json.dumps(results['perspectives'], indent=2, ensure_ascii=False)
                    st.download_button(
                        label="Perspektif Analizi (JSON)",
                        data=persp_json,
                        file_name=f"perspectives_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
    
    # Yeni araştırma butonu - Styled
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("Yeni Araştırma Başlat", type="primary", use_container_width=True):
            st.session_state.results = None
            st.rerun()


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    main()
