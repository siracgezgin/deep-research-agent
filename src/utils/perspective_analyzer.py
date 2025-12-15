"""
Perspective Analyzer - Çelişkili Görüş Tespiti
=============================================

Araştırma bulgularındaki farklı perspektifleri, çelişkileri ve 
karşıt görüşleri otomatik tespit eder.
"""

import os
import sys
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.retry_helper import retry_with_exponential_backoff
from src.utils.logger import logger

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


class PerspectiveAnalyzer:
    """Farklı perspektifleri ve çelişkileri analiz eder"""
    
    def __init__(self, model_name='gemini-2.5-flash'):
        self.model_name = model_name
        
        system_instruction = """Sen bir analist uzmanısın.

GÖREV:
Araştırma bulgularındaki farklı görüşleri, çelişkileri ve perspektifleri tespit et.

YETENEKLERİN:
1. Çelişkili iddiaları bulma
2. Farklı perspektifleri kategorize etme
3. Uzlaşma noktalarını belirleme
4. Her görüşün destekleyici kaynaklarını listeleme

ÖNEMLİ:
- Objektif ol
- Her perspektifi adil şekilde temsil et
- Çelişkileri açıkça belirt
- Hangi görüş daha yaygın/güçlü ise belirt
"""
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_instruction,
            generation_config={
                "temperature": 0.3,  # Objektiflik için düşük
                "response_mime_type": "application/json"
            }
        )
    
    @retry_with_exponential_backoff(max_retries=3)
    def analyze_perspectives(
        self,
        topic: str,
        findings: List[Dict]
    ) -> Dict:
        """
        Bulgulardaki farklı perspektifleri analiz et
        
        Args:
            topic: Ana konu
            findings: Araştırma bulguları (her biri source data içermeli)
        
        Returns:
            {
                'topic': str,
                'has_conflict': bool,
                'perspectives': [
                    {
                        'label': str ('supportive', 'critical', 'neutral'),
                        'summary': str,
                        'key_points': List[str],
                        'sources': List[str]
                    }
                ],
                'conflicts': [
                    {
                        'claim_a': str,
                        'claim_b': str,
                        'conflict_type': str,
                        'resolution': str
                    }
                ],
                'consensus_areas': List[str]
            }
        """
        
        logger.info(f"Perspektif analizi başlatılıyor: {topic}")
        
        # Bulguları prompt'a dönüştür
        prompt = f"""Konu: {topic}

Araştırma Bulguları:

"""
        
        for i, finding in enumerate(findings, 1):
            prompt += f"\n[Bulgu {i}]\n"
            prompt += f"Kaynak: {finding.get('url', 'Bilinmiyor')}\n"
            prompt += f"Özet: {finding.get('summary', '')[:500]}\n"
            
            if 'key_findings' in finding:
                prompt += "Ana noktalar:\n"
                for point in finding['key_findings'][:5]:
                    prompt += f"- {point}\n"
            
            prompt += "\n"
        
        prompt += """

Bu bulguları analiz et ve şu JSON formatında döndür:

{
  "has_conflict": true/false,
  "perspectives": [
    {
      "label": "supportive" | "critical" | "neutral" | "skeptical",
      "summary": "Bu perspektifin özeti",
      "key_points": ["Nokta 1", "Nokta 2"],
      "sources": ["url1", "url2"]
    }
  ],
  "conflicts": [
    {
      "claim_a": "İddia A",
      "claim_b": "İddia B (çelişkili)",
      "conflict_type": "data" | "interpretation" | "methodology",
      "resolution": "Nasıl çözülebilir veya hangisi daha güçlü"
    }
  ],
  "consensus_areas": ["Üzerinde anlaşma olan nokta 1", "..."]
}

Eğer çelişki yoksa conflicts boş array dön.
"""
        
        response = self.model.generate_content(prompt)
        
        import json
        import time
        time.sleep(13)  # Rate limit
        
        analysis = json.loads(response.text)
        analysis['topic'] = topic
        
        logger.info(f"Perspektif analizi tamamlandı: {len(analysis.get('perspectives', []))} perspektif bulundu")
        
        return analysis
    
    def detect_bias(self, text: str) -> Dict:
        """
        Metindeki önyargıyı tespit et
        
        Args:
            text: Analiz edilecek metin
        
        Returns:
            {
                'has_bias': bool,
                'bias_type': str | None,
                'indicators': List[str],
                'balance_score': int (0-100)
            }
        """
        
        prompt = f"""Bu metni önyargı açısından analiz et:

{text[:2000]}

Şu JSON formatında döndür:

{{
  "has_bias": true/false,
  "bias_type": null | "political" | "commercial" | "ideological" | "cultural",
  "indicators": ["Gösterge 1", "Gösterge 2"],
  "balance_score": 0-100 (100 = tamamen dengeli),
  "explanation": "Kısa açıklama"
}}
"""
        
        response = self.model.generate_content(prompt)
        
        import json
        import time
        time.sleep(13)
        
        return json.loads(response.text)
    
    def compare_sources(self, source_a: Dict, source_b: Dict) -> Dict:
        """İki kaynağı karşılaştır"""
        
        prompt = f"""İki kaynağı karşılaştır:

Kaynak A:
URL: {source_a.get('url')}
İçerik: {source_a.get('summary', '')[:500]}

Kaynak B:
URL: {source_b.get('url')}
İçerik: {source_b.get('summary', '')[:500]}

JSON döndür:

{{
  "agreement_level": "high" | "medium" | "low",
  "common_points": ["Ortak nokta 1", ...],
  "differences": ["Fark 1", ...],
  "conflicts": ["Çelişki 1", ...] (varsa)
}}
"""
        
        response = self.model.generate_content(prompt)
        
        import json
        import time
        time.sleep(13)
        
        return json.loads(response.text)


# Test
if __name__ == "__main__":
    print("\n" + "="*70)
    print("PERSPECTIVE ANALYZER TEST")
    print("="*70 + "\n")
    
    analyzer = PerspectiveAnalyzer()
    
    # Mock findings
    mock_findings = [
        {
            'url': 'https://example.com/source1',
            'summary': 'Yapay zeka çok faydalıdır ve topluma büyük katkı sağlar. İş verimliliğini artırır.',
            'key_findings': [
                'İş gücü verimliliği %40 arttı',
                'Maliyet tasarrufu sağlıyor',
                'Yeni iş alanları yaratıyor'
            ]
        },
        {
            'url': 'https://example.com/source2',
            'summary': 'Yapay zeka ciddi riskler taşıyor. İş kayıplarına ve eşitsizliğe yol açabilir.',
            'key_findings': [
                '300 milyon iş kaybolacak',
                'Etik sorunlar var',
                'Kontrol edilemez hale gelebilir'
            ]
        },
        {
            'url': 'https://example.com/source3',
            'summary': 'Yapay zeka hem fırsatlar hem riskler sunuyor. Dengeli yaklaşım gerekli.',
            'key_findings': [
                'Düzenleme gerekli',
                'Eğitim önemli',
                'Adaptasyon süreci zaman alacak'
            ]
        }
    ]
    
    print("⏳ Analiz ediliyor...\n")
    
    try:
        result = analyzer.analyze_perspectives(
            topic="Yapay zeka etiği",
            findings=mock_findings
        )
        
        print(f"✅ Analiz tamamlandı!\n")
        print(f"Çelişki var mı: {result['has_conflict']}")
        print(f"Perspektif sayısı: {len(result.get('perspectives', []))}")
        print(f"Çelişki sayısı: {len(result.get('conflicts', []))}")
        print(f"Uzlaşma noktası sayısı: {len(result.get('consensus_areas', []))}")
        
        print("\nPerspektifler:")
        for p in result.get('perspectives', []):
            print(f"  - {p['label']}: {p['summary'][:80]}...")
        
        if result.get('conflicts'):
            print("\nÇelişkiler:")
            for c in result['conflicts']:
                print(f"  - {c['claim_a']} VS {c['claim_b']}")
    
    except Exception as e:
        print(f"❌ Hata (muhtemelen quota): {e}")
        print("Bu normal - yarın test edebilirsin")
