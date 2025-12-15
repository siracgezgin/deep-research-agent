"""
Demo/Mock Data Generator
Tam sistemi API kotası olmadan test etmek için
"""

from datetime import datetime, timedelta
import json


def generate_demo_results():
    """
    Gerçekçi demo sonuçları üret (tüm yeni özellikleri içerir)
    """
    
    demo_results = {
        "success": True,
        "topic": "Yapay Zeka Etiği ve Toplumsal Etkileri",
        
        # =====================================================================
        # PLAN
        # =====================================================================
        "plan": {
            "topic": "Yapay Zeka Etiği ve Toplumsal Etkileri",
            "description": "Yapay zekanın etik boyutları, toplumsal sonuçları ve düzenleme gereksinimleri hakkında kapsamlı araştırma",
            "subtopics": [
                {
                    "title": "Algoritmik Önyargı ve Adalet",
                    "question": "YZ sistemlerinde önyargı nasıl oluşur ve nasıl önlenir?",
                    "source_type": "academic",
                    "priority": 5
                },
                {
                    "title": "İş Gücü Piyasasına Etkileri",
                    "question": "Otomasyon hangi sektörleri nasıl etkileyecek?",
                    "source_type": "mixed",
                    "priority": 4
                },
                {
                    "title": "Mahremiyet ve Veri Güvenliği",
                    "question": "YZ çağında kişisel verilerin korunması nasıl sağlanır?",
                    "source_type": "technical",
                    "priority": 5
                },
                {
                    "title": "Otonom Sistemlerde Sorumluluk",
                    "question": "Otonom araçlarda kaza durumunda yasal sorumluluk kime aittir?",
                    "source_type": "legal",
                    "priority": 4
                },
                {
                    "title": "Düzenleyici Çerçeveler",
                    "question": "AB AI Act ve benzeri düzenlemeler neleri içeriyor?",
                    "source_type": "regulatory",
                    "priority": 3
                }
            ]
        },
        
        # =====================================================================
        # RESEARCH RESULTS
        # =====================================================================
        "research_results": [
            {
                "topic": "Algoritmik Önyargı ve Adalet",
                "subtopic_title": "Algoritmik Önyargı ve Adalet",
                "confidence": 5,
                "scored_sources": [
                    {
                        "url": "https://arxiv.org/abs/1908.09635",
                        "title": "Fairness and Abstraction in Sociotechnical Systems",
                        "score": 92,
                        "trust_level": "high",
                        "badges": ["🎓 Akademik", "✅ Güvenilir", "📊 Detaylı"],
                        "domain": "arxiv.org",
                        "date": "2023-03-15"
                    },
                    {
                        "url": "https://www.nature.com/articles/s41586-023-05860-0",
                        "title": "Algorithmic bias in AI systems",
                        "score": 95,
                        "trust_level": "high",
                        "badges": ["🎓 Akademik", "✅ Güvenilir", "🆕 Güncel"],
                        "domain": "nature.com",
                        "date": "2023-11-20"
                    },
                    {
                        "url": "https://www.acm.org/code-of-ethics",
                        "title": "ACM Code of Ethics - AI Guidelines",
                        "score": 88,
                        "trust_level": "high",
                        "badges": ["🏛️ Kurum", "✅ Güvenilir"],
                        "domain": "acm.org",
                        "date": "2023-06-01"
                    }
                ],
                "key_findings": [
                    "Eğitim verilerindeki tarihi önyargılar YZ modellerine yansıyor",
                    "Cinsiyet ve ırk bazlı ayrımcılık risk değerlendirme sistemlerinde yaygın",
                    "Adil YZ için 'fairness metrics' geliştirilmiş (demographic parity, equal opportunity)",
                    "Açıklanabilir yapay zeka (XAI) önyargı tespitinde kritik rol oynuyor"
                ],
                "summary": "Algoritmik önyargı, YZ sistemlerinin eğitim verilerindeki toplumsal önyargıları öğrenmesi ve pekiştirmesiyle oluşur. Çözüm için çeşitli teknik (veri dengeleme, adalet metrikleri) ve organizasyonel (çeşitli ekipler, etik denetim) önlemler önerilmektedir."
            },
            {
                "topic": "İş Gücü Piyasasına Etkileri",
                "subtopic_title": "İş Gücü Piyasasına Etkileri",
                "confidence": 4,
                "scored_sources": [
                    {
                        "url": "https://www.mckinsey.com/featured-insights/future-of-work/ai-automation-and-the-future-of-work",
                        "title": "AI, Automation, and the Future of Work",
                        "score": 78,
                        "trust_level": "medium",
                        "badges": ["📊 Detaylı", "🆕 Güncel"],
                        "domain": "mckinsey.com",
                        "date": "2024-01-10"
                    },
                    {
                        "url": "https://www.imf.org/en/Publications/Staff-Discussion-Notes/Issues/2024/01/14/AI-and-Employment",
                        "title": "AI, Technological Unemployment, and Income Distribution",
                        "score": 85,
                        "trust_level": "high",
                        "badges": ["🏛️ Kurum", "✅ Güvenilir", "🆕 Güncel"],
                        "domain": "imf.org",
                        "date": "2024-01-14"
                    },
                    {
                        "url": "https://medium.com/@techlead/will-ai-take-your-job-d2b3c5f6a7e8",
                        "title": "Will AI Take Your Job? A Developer's Perspective",
                        "score": 52,
                        "trust_level": "low",
                        "badges": ["📝 Blog"],
                        "domain": "medium.com",
                        "date": "2024-02-05"
                    }
                ],
                "key_findings": [
                    "2030'a kadar 400-800 milyon iş otomasyondan etkilenebilir (McKinsey tahmini)",
                    "Rutinsel ve tekrarlı işler yüksek risk altında (üretim, veri girişi, muhasebe)",
                    "Yaratıcılık, empati ve karmaşık problem çözme gerektiren işler daha az risk altında",
                    "Yeni iş kategorileri ortaya çıkacak (YZ eğiticileri, etik denetçileri)",
                    "İşsizlik değil, 'job displacement' bekleniyor - yeniden eğitim kritik"
                ],
                "summary": "YZ ve otomasyon iş gücü piyasasını köklü şekilde dönüştürecek. Rutinsel işlerin otomasyonu hızlanırken, insan merkezli becerilere talep artacak. Toplumsal uyum için yeniden eğitim programları ve sosyal güvenlik ağlarının güçlendirilmesi gerekiyor."
            },
            {
                "topic": "Mahremiyet ve Veri Güvenliği",
                "subtopic_title": "Mahremiyet ve Veri Güvenliği",
                "confidence": 5,
                "scored_sources": [
                    {
                        "url": "https://www.eff.org/issues/artificial-intelligence",
                        "title": "Artificial Intelligence and Privacy",
                        "score": 82,
                        "trust_level": "high",
                        "badges": ["🏛️ Kurum", "✅ Güvenilir"],
                        "domain": "eff.org",
                        "date": "2023-09-12"
                    },
                    {
                        "url": "https://gdpr.eu/artificial-intelligence/",
                        "title": "GDPR and AI: Data Protection in the Age of Machine Learning",
                        "score": 86,
                        "trust_level": "high",
                        "badges": ["⚖️ Hukuki", "✅ Güvenilir", "📊 Detaylı"],
                        "domain": "gdpr.eu",
                        "date": "2023-10-05"
                    }
                ],
                "key_findings": [
                    "YZ sistemleri büyük ölçekli kişisel veri işliyor - mahremiyet riski yüksek",
                    "Differential privacy ve federated learning gibi teknikler geliştirilmiş",
                    "GDPR'ın 'açıklama hakkı' YZ kararlarını da kapsıyor",
                    "Yüz tanıma ve biyometrik veri kullanımı tartışmalı",
                    "Veri minimizasyonu ve purpose limitation ilkeleri kritik"
                ],
                "summary": "YZ çağında veri mahremiyeti karmaşık bir sorundur. Teknik çözümler (differential privacy, federated learning) ve yasal düzenlemeler (GDPR) birlikte uygulanmalıdır. Şeffaflık, veri minimizasyonu ve kullanıcı kontrolü temel ilkelerdir."
            }
        ],
        
        # =====================================================================
        # FINAL REPORT
        # =====================================================================
        "report": """# Yapay Zeka Etiği ve Toplumsal Etkileri: Kapsamlı Analiz

## Giriş

Yapay zeka (YZ) teknolojisinin hızla gelişmesi, toplumu ekonomik, sosyal ve etik açılardan derinden etkilemektedir. Bu rapor, YZ'nin etik boyutlarını, toplumsal sonuçlarını ve düzenleyici ihtiyaçları kapsamlı bir şekilde ele almaktadır.

## 1. Algoritmik Önyargı ve Adalet

### Sorun
Yapay zeka sistemlerinde algoritmik önyargı, eğitim verilerindeki tarihi önyargıların modellere yansımasıyla ortaya çıkar. Cinsiyet ve ırk bazlı ayrımcılık özellikle risk değerlendirme, işe alım ve kredi skorlama sistemlerinde yaygındır.

### Çözümler
- **Teknik Önlemler**: Veri dengeleme, fairness metrics (demographic parity, equal opportunity), açıklanabilir yapay zeka (XAI)
- **Organizasyonel Önlemler**: Çeşitli ekipler, bağımsız etik denetimler, sürekli izleme

### Akademik Perspektif
Nature dergisinde yayınlanan araştırmalar, önyargı azaltma tekniklerinin etkinliğini göstermektedir. Ancak, "adalet" kavramının çoklu tanımları arasında trade-off'lar bulunmaktadır.

## 2. İş Gücü Piyasasına Etkileri

### İki Farklı Perspektif

**🔴 Karamsar Görüş** (IMF, bazı ekonomistler):
- 2030'a kadar 400-800 milyon iş otomasyon nedeniyle kaybolabilir
- Rutinsel işler yüksek risk altında (üretim, veri girişi, muhasebe)
- Gelir eşitsizliği artabilir (skilled vs unskilled worker gap)

**🟢 İyimser Görüş** (McKinsey, teknoloji liderleri):
- YZ yeni iş kategorileri yaratacak (YZ eğiticileri, etik denetçileri, prompt mühendisleri)
- İşsizlik değil, "job displacement" - insanlar yeni rollere geçecek
- Üretkenlik artışı ekonomik büyüme sağlayacak

### Uzlaşma Alanı
Her iki grup da yeniden eğitim programlarının kritik önemini vurgulamaktadır. Yaratıcılık, empati ve karmaşık problem çözme gibi insan merkezli becerilere yatırım yapılması gereklidir.

## 3. Mahremiyet ve Veri Güvenliği

### Riskler
- Büyük ölçekli kişisel veri işleme
- Yüz tanıma ve biyometrik veri kullanımı
- Profilleme ve mikro hedefleme
- Veri sızıntıları ve kötüye kullanım

### Koruma Mekanizmaları
**Teknik Çözümler**:
- Differential Privacy: Bireysel verileri gizlerken toplu analiz yapma
- Federated Learning: Verileri merkezi sunucuya göndermeden model eğitme
- Homomorphic Encryption: Şifreli verilerle hesaplama

**Yasal Düzenlemeler**:
- GDPR: Açıklama hakkı, unutulma hakkı, veri taşınabilirliği
- Veri minimizasyonu ilkesi
- Purpose limitation (amaç sınırlaması)

## 4. Otonom Sistemlerde Sorumluluk

Otonom araçlarda kaza durumunda yasal sorumluluk belirsizdir:
- Sürücü mü?
- Üretici mi?
- Yazılım geliştiricisi mi?
- YZ sistemi kendisi mi? (tartışmalı)

Çoğu hukuk sistemi henüz bu sorulara net yanıt veremiyor. AB AI Act gibi düzenlemeler yüksek riskli YZ sistemleri için sorumluluk çerçevesi oluşturmaya çalışıyor.

## 5. Düzenleyici Çerçeveler

### AB AI Act
- Risk bazlı sınıflandırma (unacceptable, high, limited, minimal risk)
- Yüksek riskli sistemler için zorunlu denetimler
- Yasaklar: sosyal skorlama, bilinçaltı manipülasyon

### Diğer İnisiyatifler
- OECD AI Principles
- IEEE Ethically Aligned Design
- Partnership on AI

## Sonuç ve Öneriler

1. **Çok Paydaşlı Yaklaşım**: Hükümetler, şirketler, akademi ve sivil toplum işbirliği yapmalı
2. **Proaktif Düzenleme**: Teknoloji ilerlemeden önce etik çerçeveler kurulmalı
3. **Eğitim ve Farkındalık**: Toplumun tüm kesimleri YZ okuryazarlığı kazanmalı
4. **Sürekli İzleme**: YZ sistemlerinin toplumsal etkileri düzenli değerlendirilmeli
5. **İnsan Merkezli Tasarım**: YZ insanlığın refahını artırma amacıyla geliştirilmeli

## Kaynaklar

1. Nature - Algorithmic bias in AI systems (2023)
2. McKinsey - AI, Automation, and the Future of Work (2024)
3. IMF - AI and Employment (2024)
4. GDPR.eu - GDPR and AI: Data Protection (2023)
5. ArXiv - Fairness and Abstraction in Sociotechnical Systems (2023)

---
*Bu rapor 5 akademik kaynak, 3 kurum raporu ve 2 sektör analizi kullanılarak hazırlanmıştır. Toplam 10 farklı kaynak incelenmiştir.*
""",
        
        # =====================================================================
        # QUALITY METRICS (YENİ)
        # =====================================================================
        "quality_metrics": {
            "overall_score": 84,
            "grade": "B+",
            "metrics": {
                "source_count": 13,      # 10 kaynak = 13/15
                "source_diversity": 14,  # 8 farklı domain = 14/15
                "source_reliability": 18, # Çoğu high trust = 18/20
                "content_depth": 17,     # Detaylı analiz = 17/20
                "recency": 13,           # Ortalama 6 ay = 13/15
                "coverage": 9            # 3/5 subtopic = 9/15
            },
            "strengths": [
                "✅ Akademik kaynaklar ağırlıklı (Nature, ArXiv, ACM)",
                "✅ Kaynak çeşitliliği yüksek (8 farklı domain)",
                "✅ Detaylı ve yapılandırılmış analiz",
                "✅ Çoğu kaynak güncel (son 12 ay)"
            ],
            "improvements": [
                "📈 Tüm alt başlıklar araştırılmadı (3/5)",
                "📈 Daha fazla güncel kaynak eklenebilir",
                "📈 Hukuki perspektif güçlendirilebilir"
            ]
        },
        
        # =====================================================================
        # PERSPECTIVES (YENİ)
        # =====================================================================
        "perspectives": {
            "has_conflict": True,
            "perspectives": [
                {
                    "label": "iyimser",
                    "summary": "YZ'nin toplumsal faydalarına ve uyum sürecinin başarılı olacağına inananlar",
                    "key_points": [
                        "YZ yeni iş alanları ve fırsatlar yaratacak",
                        "Üretkenlik artışı ekonomik refaha dönüşecek",
                        "Teknolojik ilerleme tarihin her döneminde yaşandı ve adaptasyon sağlandı",
                        "YZ sağlık, eğitim ve bilimde devrim yapacak"
                    ],
                    "sources": [
                        "McKinsey - Future of Work report",
                        "ACM - AI Guidelines",
                        "Medium - Developer's Perspective"
                    ]
                },
                {
                    "label": "karamsar",
                    "summary": "YZ'nin olumsuz etkilerine ve yetersiz hazırlığa dikkat çekenler",
                    "key_points": [
                        "400-800 milyon iş kaybolabilir (IMF tahmini)",
                        "Gelir eşitsizliği dramatik artacak",
                        "Önyargı ve ayrımcılık sistemleşecek",
                        "Mahremiyet sonu gelecek (surveillance capitalism)",
                        "Düzenlemeler teknolojinin gerisinde kalıyor"
                    ],
                    "sources": [
                        "IMF - AI and Employment report",
                        "EFF - Privacy concerns",
                        "Nature - Algorithmic bias studies"
                    ]
                },
                {
                    "label": "dengeli",
                    "summary": "Hem riskleri hem fırsatları kabul eden, proaktif politika çağrısı yapanlar",
                    "key_points": [
                        "YZ kaçınılmaz - risk yönetimi şart",
                        "Yeniden eğitim programları kritik",
                        "Etik çerçeveler şimdiden kurulmalı",
                        "Çok paydaşlı yaklaşım gerekli",
                        "İnsan merkezli tasarım ilkesi temel alınmalı"
                    ],
                    "sources": [
                        "GDPR - AI regulations",
                        "OECD - AI Principles",
                        "ArXiv - Fairness studies"
                    ]
                }
            ],
            "conflicts": [
                {
                    "conflict_type": "economic_impact",
                    "claim_a": "YZ 400-800 milyon işi yok edecek ve gelir eşitsizliğini artıracak",
                    "claim_b": "YZ yeni iş kategorileri yaratacak ve üretkenlik artışı ekonomik büyüme sağlayacak",
                    "sources_a": ["IMF report", "Bazı ekonomistler"],
                    "sources_b": ["McKinsey report", "Teknoloji liderleri"],
                    "resolution": "Her iki grup da yeniden eğitim programlarının kritik önemini kabul ediyor. Fark beklenti ve zaman çizelgesinde - kısa vadede job displacement kaçınılmaz, uzun vadede yeni denge kurulabilir."
                },
                {
                    "conflict_type": "regulatory_approach",
                    "claim_a": "Katı düzenlemeler şimdi gerekli - teknoloji çok hızlı ilerliyor",
                    "claim_b": "Aşırı düzenleme inovasyonu öldürür - sektör kendi kendini düzenlemeli",
                    "sources_a": ["EFF", "Privacy advocates", "EU regulators"],
                    "sources_b": ["Big Tech", "Libertarian think tanks"],
                    "resolution": "AB AI Act gibi risk bazlı yaklaşımlar orta yol sunuyor: yüksek riskli sistemler sıkı denetim, düşük riskli sistemler serbest."
                }
            ],
            "consensus_areas": [
                "Eğitim ve farkındalık artırılmalı",
                "Algoritmik önyargı ciddi bir sorun",
                "Mahremiyet korumaları güçlendirilmeli",
                "Açıklanabilir YZ önemli",
                "Etik denetimler olmalı"
            ]
        },
        
        # =====================================================================
        # METADATA
        # =====================================================================
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "subtopics_count": 5,
            "sources_analyzed": 10,
            "duration_seconds": 127.3,
            "errors_count": 0,
            "model": "gemini-2.0-flash-exp",
            "version": "1.0.0"
        }
    }
    
    return demo_results


def save_demo_results(output_dir: str = "demo_output"):
    """Demo sonuçlarını dosyalara kaydet"""
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    
    results = generate_demo_results()
    
    # 1. Report
    with open(f"{output_dir}/report.md", "w", encoding="utf-8") as f:
        f.write(results['report'])
    
    # 2. Plan
    with open(f"{output_dir}/plan.json", "w", encoding="utf-8") as f:
        json.dump(results['plan'], f, indent=2, ensure_ascii=False)
    
    # 3. Research
    with open(f"{output_dir}/research.json", "w", encoding="utf-8") as f:
        json.dump(results['research_results'], f, indent=2, ensure_ascii=False)
    
    # 4. Quality Metrics
    with open(f"{output_dir}/quality.json", "w", encoding="utf-8") as f:
        json.dump(results['quality_metrics'], f, indent=2, ensure_ascii=False)
    
    # 5. Perspectives
    with open(f"{output_dir}/perspectives.json", "w", encoding="utf-8") as f:
        json.dump(results['perspectives'], f, indent=2, ensure_ascii=False)
    
    # 6. Metadata
    with open(f"{output_dir}/metadata.json", "w", encoding="utf-8") as f:
        json.dump(results['metadata'], f, indent=2, ensure_ascii=False)
    
    print(f"✅ Demo sonuçları '{output_dir}/' dizinine kaydedildi")
    print(f"📄 report.md, plan.json, research.json, quality.json, perspectives.json, metadata.json")
    
    return results


if __name__ == "__main__":
    results = save_demo_results()
    
    print("\n" + "="*70)
    print("📊 DEMO SONUÇLARI ÖZETİ")
    print("="*70)
    print(f"Konu: {results['topic']}")
    print(f"Alt Başlıklar: {results['metadata']['subtopics_count']}")
    print(f"Kaynaklar: {results['metadata']['sources_analyzed']}")
    print(f"Kalite Skoru: {results['quality_metrics']['overall_score']}/100 ({results['quality_metrics']['grade']})")
    print(f"Perspektifler: {len(results['perspectives']['perspectives'])}")
    print(f"Çelişkiler: {len(results['perspectives']['conflicts'])}")
    print("="*70)
