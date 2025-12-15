"""
Quality Metrics - Rapor Kalite Değerlendirme
===========================================

Araştırma raporunun kalitesini çok boyutlu olarak değerlendirir.
"""

from typing import List, Dict
from datetime import datetime
import re


class QualityMetrics:
    """Rapor kalite metrikleri hesaplayıcı"""
    
    def calculate_report_quality(
        self,
        sources: List[Dict],
        research_results: List[Dict],
        report: str,
        topic: str
    ) -> Dict:
        """
        Raporun genel kalite skorunu hesapla
        
        Args:
            sources: Kullanılan kaynaklar (scored)
            research_results: Araştırma bulguları
            report: Üretilen rapor metni
            topic: Ana konu
        
        Returns:
            {
                'overall_score': int (0-100),
                'metrics': {
                    'source_count': int,
                    'source_diversity': int,
                    'source_reliability': int,
                    'content_depth': int,
                    'recency': int,
                    'coverage': int
                },
                'grade': str ('A+', 'A', 'B', 'C', 'D', 'F'),
                'strengths': List[str],
                'improvements': List[str]
            }
        """
        
        metrics = {}
        
        # 1. Kaynak Sayısı (0-15)
        metrics['source_count'] = self._score_source_count(sources)
        
        # 2. Kaynak Çeşitliliği (0-15)
        metrics['source_diversity'] = self._score_source_diversity(sources)
        
        # 3. Kaynak Güvenilirliği (0-20)
        metrics['source_reliability'] = self._score_source_reliability(sources)
        
        # 4. İçerik Derinliği (0-20)
        metrics['content_depth'] = self._score_content_depth(report, research_results)
        
        # 5. Güncellik (0-15)
        metrics['recency'] = self._score_recency(sources)
        
        # 6. Kapsam (0-15)
        metrics['coverage'] = self._score_coverage(research_results, topic)
        
        # Toplam skor
        overall_score = sum(metrics.values())
        
        # Harf notu
        grade = self._calculate_grade(overall_score)
        
        # Güçlü yönler ve iyileştirmeler
        strengths, improvements = self._analyze_strengths_weaknesses(metrics)
        
        return {
            'overall_score': overall_score,
            'metrics': metrics,
            'grade': grade,
            'strengths': strengths,
            'improvements': improvements
        }
    
    def _score_source_count(self, sources: List[Dict]) -> int:
        """Kaynak sayısı skoru (0-15)"""
        count = len(sources)
        
        if count >= 20:
            return 15
        elif count >= 15:
            return 13
        elif count >= 10:
            return 11
        elif count >= 5:
            return 8
        else:
            return 5
    
    def _score_source_diversity(self, sources: List[Dict]) -> int:
        """Kaynak çeşitliliği skoru (0-15)"""
        
        if not sources:
            return 0
        
        # Farklı domain sayısı
        from urllib.parse import urlparse
        domains = set()
        
        for source in sources:
            try:
                domain = urlparse(source['url']).netloc
                domains.add(domain)
            except:
                pass
        
        diversity_ratio = len(domains) / len(sources)
        
        if diversity_ratio >= 0.8:
            return 15
        elif diversity_ratio >= 0.6:
            return 12
        elif diversity_ratio >= 0.4:
            return 9
        else:
            return 5
    
    def _score_source_reliability(self, sources: List[Dict]) -> int:
        """Kaynak güvenilirliği skoru (0-20)"""
        
        if not sources:
            return 0
        
        # Kaynaklardaki skorları topla
        total_score = sum(s.get('score', 50) for s in sources)
        avg_score = total_score / len(sources)
        
        # 0-100'den 0-20'ye çevir
        return int((avg_score / 100) * 20)
    
    def _score_content_depth(self, report: str, research_results: List[Dict]) -> int:
        """İçerik derinliği skoru (0-20)"""
        
        score = 0
        
        # 1. Rapor uzunluğu (0-8)
        word_count = len(report.split())
        
        if word_count >= 3000:
            score += 8
        elif word_count >= 2000:
            score += 6
        elif word_count >= 1000:
            score += 4
        else:
            score += 2
        
        # 2. Bölüm sayısı (0-6)
        section_count = len([r for r in research_results if r.get('summary')])
        
        if section_count >= 8:
            score += 6
        elif section_count >= 6:
            score += 5
        elif section_count >= 4:
            score += 4
        else:
            score += 2
        
        # 3. Detay seviyesi (0-6)
        # Bulgular, örnekler, açıklamalar
        detail_indicators = [
            'örneğin', 'specifically', 'detailed', 'analysis',
            'bulgu', 'veri', 'data', 'research shows'
        ]
        
        detail_count = sum(
            report.lower().count(indicator)
            for indicator in detail_indicators
        )
        
        if detail_count >= 20:
            score += 6
        elif detail_count >= 10:
            score += 4
        else:
            score += 2
        
        return min(score, 20)
    
    def _score_recency(self, sources: List[Dict]) -> int:
        """Güncellik skoru (0-15)"""
        
        if not sources:
            return 5
        
        # Kaynakların recency skorlarını topla
        recency_scores = [
            s.get('breakdown', {}).get('recency', 10)
            for s in sources
        ]
        
        if not recency_scores:
            return 5
        
        avg_recency = sum(recency_scores) / len(recency_scores)
        
        # 0-20'den 0-15'e çevir
        return int((avg_recency / 20) * 15)
    
    def _score_coverage(self, research_results: List[Dict], topic: str) -> int:
        """Kapsam skoru (0-15)"""
        
        if not research_results:
            return 0
        
        score = 0
        
        # 1. Subtopic sayısı (0-8)
        subtopic_count = len(research_results)
        
        if subtopic_count >= 8:
            score += 8
        elif subtopic_count >= 6:
            score += 7
        elif subtopic_count >= 4:
            score += 5
        else:
            score += 3
        
        # 2. Her subtopic'in kalitesi (0-7)
        avg_confidence = sum(
            r.get('confidence', 0)
            for r in research_results
        ) / len(research_results)
        
        score += int((avg_confidence / 5) * 7)
        
        return min(score, 15)
    
    def _calculate_grade(self, score: int) -> str:
        """Skordan harf notu hesapla"""
        
        if score >= 95:
            return 'A+'
        elif score >= 90:
            return 'A'
        elif score >= 85:
            return 'A-'
        elif score >= 80:
            return 'B+'
        elif score >= 75:
            return 'B'
        elif score >= 70:
            return 'B-'
        elif score >= 65:
            return 'C+'
        elif score >= 60:
            return 'C'
        elif score >= 55:
            return 'C-'
        elif score >= 50:
            return 'D'
        else:
            return 'F'
    
    def _analyze_strengths_weaknesses(
        self,
        metrics: Dict[str, int]
    ) -> tuple:
        """Güçlü yönler ve iyileştirme alanları"""
        
        strengths = []
        improvements = []
        
        # Kaynak sayısı
        if metrics['source_count'] >= 11:
            strengths.append("✅ Çok sayıda kaynak kullanıldı")
        elif metrics['source_count'] < 8:
            improvements.append("📈 Daha fazla kaynak eklenebilir")
        
        # Çeşitlilik
        if metrics['source_diversity'] >= 12:
            strengths.append("✅ Kaynak çeşitliliği yüksek")
        elif metrics['source_diversity'] < 9:
            improvements.append("📈 Daha farklı kaynak türleri kullanılabilir")
        
        # Güvenilirlik
        if metrics['source_reliability'] >= 16:
            strengths.append("✅ Güvenilir kaynaklar kullanıldı")
        elif metrics['source_reliability'] < 12:
            improvements.append("📈 Daha güvenilir kaynaklar tercih edilebilir")
        
        # Derinlik
        if metrics['content_depth'] >= 16:
            strengths.append("✅ Detaylı ve derin analiz")
        elif metrics['content_depth'] < 12:
            improvements.append("📈 Daha detaylı açıklamalar eklenebilir")
        
        # Güncellik
        if metrics['recency'] >= 12:
            strengths.append("✅ Güncel kaynaklar kullanıldı")
        elif metrics['recency'] < 8:
            improvements.append("📈 Daha güncel kaynaklar aranabilir")
        
        # Kapsam
        if metrics['coverage'] >= 12:
            strengths.append("✅ Kapsamlı araştırma")
        elif metrics['coverage'] < 9:
            improvements.append("📈 Daha fazla alt konu incelenebilir")
        
        return strengths, improvements


# Test
if __name__ == "__main__":
    print("\n" + "="*70)
    print("QUALITY METRICS TEST")
    print("="*70 + "\n")
    
    qm = QualityMetrics()
    
    # Mock data
    mock_sources = [
        {'url': 'https://arxiv.org/1', 'score': 85, 'breakdown': {'recency': 18}},
        {'url': 'https://bbc.com/2', 'score': 75, 'breakdown': {'recency': 15}},
        {'url': 'https://nature.com/3', 'score': 90, 'breakdown': {'recency': 12}},
        {'url': 'https://ieee.org/4', 'score': 88, 'breakdown': {'recency': 16}},
        {'url': 'https://medium.com/5', 'score': 60, 'breakdown': {'recency': 10}},
    ]
    
    mock_research = [
        {'topic': 'Sub 1', 'confidence': 4, 'summary': 'Good findings'},
        {'topic': 'Sub 2', 'confidence': 5, 'summary': 'Excellent findings'},
        {'topic': 'Sub 3', 'confidence': 3, 'summary': 'Decent findings'},
        {'topic': 'Sub 4', 'confidence': 4, 'summary': 'Good findings'},
        {'topic': 'Sub 5', 'confidence': 5, 'summary': 'Great findings'},
        {'topic': 'Sub 6', 'confidence': 4, 'summary': 'Solid findings'},
    ]
    
    mock_report = """
    # Yapay Zeka Etiği Raporu
    
    ## Executive Summary
    Bu rapor yapay zeka etiğini kapsamlı şekilde incelemektedir.
    
    ## Giriş
    Yapay zeka etiği günümüzün en önemli konularından biridir.
    Örneğin, facial recognition sistemleri ciddi etik sorunlar yaratmaktadır.
    
    ## Bölüm 1
    Detaylı analiz burada... (200+ kelime)
    """ * 10  # Uzun rapor simüle et
    
    result = qm.calculate_report_quality(
        sources=mock_sources,
        research_results=mock_research,
        report=mock_report,
        topic="Yapay zeka etiği"
    )
    
    print(f"📊 GENEL KALITE SKORU: {result['overall_score']}/100")
    print(f"🎓 NOT: {result['grade']}\n")
    
    print("Detaylı Metrikler:")
    for metric, score in result['metrics'].items():
        print(f"  {metric}: {score}")
    
    print(f"\n✅ Güçlü Yönler ({len(result['strengths'])}):")
    for strength in result['strengths']:
        print(f"  {strength}")
    
    print(f"\n📈 İyileştirme Alanları ({len(result['improvements'])}):")
    for improvement in result['improvements']:
        print(f"  {improvement}")
