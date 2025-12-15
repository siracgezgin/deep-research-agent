"""
Source Scorer - Kaynak Güvenilirliği Skorlama
============================================

Her kaynağa güvenilirlik skoru verir (0-100).

Skorlama Kriterleri:
- Domain authority (.edu, .gov, tanınmış siteler)
- Güncellik (ne kadar yeni)
- İçerik kalitesi (uzunluk, derinlik)
- Cite edilme (kaç kez referans gösterilmiş)
"""

from datetime import datetime
from typing import Dict, List
from urllib.parse import urlparse
import re


class SourceScorer:
    """Kaynak güvenilirliği skorlama sistemi"""
    
    # Güvenilir domain'ler ve skorları
    TRUSTED_DOMAINS = {
        # Akademik
        '.edu': 95,
        '.ac.uk': 95,
        'scholar.google': 95,
        'arxiv.org': 90,
        'researchgate.net': 85,
        'sciencedirect.com': 90,
        'springer.com': 90,
        'ieee.org': 95,
        
        # Resmi
        '.gov': 95,
        '.gov.tr': 95,
        'who.int': 95,
        'un.org': 90,
        
        # Haber (güvenilir)
        'reuters.com': 85,
        'bbc.com': 85,
        'nytimes.com': 85,
        'theguardian.com': 85,
        'apnews.com': 90,
        
        # Türkiye
        'tubitak.gov.tr': 95,
        'tdk.gov.tr': 90,
        
        # Teknoloji
        'github.com': 80,
        'stackoverflow.com': 75,
        'medium.com': 60,
        
        # Genel
        'wikipedia.org': 70,
    }
    
    # Düşük güvenilirlik
    LOW_TRUST_INDICATORS = [
        'blogspot.com',
        'wordpress.com',
        'wix.com',
        'tumblr.com',
    ]
    
    def score_source(
        self,
        url: str,
        title: str = "",
        content: str = "",
        publish_date: str = None
    ) -> Dict:
        """
        Kaynağa güvenilirlik skoru ver
        
        Args:
            url: Kaynak URL
            title: Başlık
            content: İçerik
            publish_date: Yayın tarihi (YYYY-MM-DD)
        
        Returns:
            {
                'url': str,
                'score': int (0-100),
                'breakdown': {
                    'domain': int,
                    'recency': int,
                    'content_quality': int
                },
                'trust_level': str ('high', 'medium', 'low'),
                'badges': List[str]
            }
        """
        
        score = 0
        breakdown = {}
        badges = []
        
        # 1. Domain Authority (40 puan)
        domain_score = self._score_domain(url)
        breakdown['domain'] = domain_score
        score += domain_score
        
        if domain_score >= 90:
            badges.append("🎓 Akademik")
        elif domain_score >= 85:
            badges.append("✅ Güvenilir")
        
        # 2. Güncellik (20 puan)
        recency_score = self._score_recency(publish_date)
        breakdown['recency'] = recency_score
        score += recency_score
        
        if recency_score >= 18:
            badges.append("🆕 Güncel")
        
        # 3. İçerik Kalitesi (40 puan)
        quality_score = self._score_content_quality(content, title)
        breakdown['content_quality'] = quality_score
        score += quality_score
        
        if quality_score >= 35:
            badges.append("📊 Detaylı")
        
        # Güven seviyesi
        if score >= 80:
            trust_level = "high"
        elif score >= 60:
            trust_level = "medium"
        else:
            trust_level = "low"
        
        return {
            'url': url,
            'score': min(score, 100),
            'breakdown': breakdown,
            'trust_level': trust_level,
            'badges': badges
        }
    
    def _score_domain(self, url: str) -> int:
        """Domain authority skoru (0-40)"""
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Tam eşleşme kontrolü
            for trusted_domain, score in self.TRUSTED_DOMAINS.items():
                if trusted_domain in domain:
                    return int(score * 0.4)  # 40 puan üzerinden
            
            # Düşük güvenilirlik kontrolü
            for low_trust in self.LOW_TRUST_INDICATORS:
                if low_trust in domain:
                    return 10
            
            # HTTPS bonus
            base_score = 25
            if parsed.scheme == 'https':
                base_score += 5
            
            return base_score
        
        except Exception:
            return 20
    
    def _score_recency(self, publish_date: str) -> int:
        """Güncellik skoru (0-20)"""
        
        if not publish_date:
            return 10  # Bilinmiyorsa orta skor
        
        try:
            pub_date = datetime.strptime(publish_date, '%Y-%m-%d')
            now = datetime.now()
            days_old = (now - pub_date).days
            
            # Güncellik skorlaması
            if days_old <= 30:      # Son 1 ay
                return 20
            elif days_old <= 90:    # Son 3 ay
                return 18
            elif days_old <= 180:   # Son 6 ay
                return 15
            elif days_old <= 365:   # Son 1 yıl
                return 12
            elif days_old <= 730:   # Son 2 yıl
                return 8
            else:                   # 2+ yıl
                return 5
        
        except Exception:
            return 10
    
    def _score_content_quality(self, content: str, title: str) -> int:
        """İçerik kalitesi skoru (0-40)"""
        
        if not content:
            return 15
        
        score = 0
        
        # 1. Uzunluk (0-15)
        word_count = len(content.split())
        if word_count >= 2000:
            score += 15
        elif word_count >= 1000:
            score += 12
        elif word_count >= 500:
            score += 10
        elif word_count >= 200:
            score += 7
        else:
            score += 5
        
        # 2. Yapılandırılmış içerik (0-10)
        # Başlıklar, listeler, bölümler var mı?
        structure_indicators = [
            r'\n#{1,3}\s',          # Markdown başlıklar
            r'\n-\s',               # Liste
            r'\n\d+\.',             # Numaralı liste
            r'\n\*\s',              # Yıldızlı liste
        ]
        
        structure_count = sum(
            1 for pattern in structure_indicators
            if re.search(pattern, content)
        )
        score += min(structure_count * 2, 10)
        
        # 3. Akademik göstergeler (0-10)
        academic_indicators = [
            'research', 'study', 'analysis', 'data',
            'methodology', 'conclusion', 'findings',
            'abstract', 'introduction', 'references'
        ]
        
        academic_count = sum(
            1 for indicator in academic_indicators
            if indicator.lower() in content.lower()
        )
        score += min(academic_count, 10)
        
        # 4. Referans/Kaynak var mı? (0-5)
        citation_indicators = [
            'http://', 'https://', '[', ']',
            'source:', 'reference:', 'cite:'
        ]
        
        has_citations = any(
            indicator in content.lower()
            for indicator in citation_indicators
        )
        if has_citations:
            score += 5
        
        return min(score, 40)
    
    def score_multiple_sources(self, sources: List[Dict]) -> List[Dict]:
        """Birden fazla kaynağı skorla"""
        
        scored = []
        
        for source in sources:
            score_data = self.score_source(
                url=source.get('url', ''),
                title=source.get('title', ''),
                content=source.get('content', ''),
                publish_date=source.get('published_date')
            )
            
            # Orijinal source data ile birleştir
            scored_source = {**source, **score_data}
            scored.append(scored_source)
        
        # Skora göre sırala
        scored.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return scored
    
    def calculate_diversity_score(self, sources: List[Dict]) -> Dict:
        """Kaynak çeşitliliği skoru hesapla"""
        
        if not sources:
            return {'score': 0, 'analysis': {}}
        
        # Domain çeşitliliği
        domains = set()
        for source in sources:
            try:
                domain = urlparse(source['url']).netloc
                domains.add(domain)
            except:
                pass
        
        domain_diversity = min(len(domains) / len(sources), 1.0) * 100
        
        # Trust level çeşitliliği
        trust_levels = [s.get('trust_level', 'medium') for s in sources]
        high_trust = trust_levels.count('high')
        medium_trust = trust_levels.count('medium')
        low_trust = trust_levels.count('low')
        
        # Balanced distribution is good
        trust_diversity = 0
        if high_trust > 0:
            trust_diversity += 40
        if medium_trust > 0:
            trust_diversity += 30
        if high_trust >= len(sources) * 0.5:  # En az %50 high trust
            trust_diversity += 30
        
        # Genel çeşitlilik skoru
        overall_diversity = (domain_diversity * 0.6) + (trust_diversity * 0.4)
        
        return {
            'score': round(overall_diversity, 1),
            'analysis': {
                'unique_domains': len(domains),
                'total_sources': len(sources),
                'domain_diversity': round(domain_diversity, 1),
                'trust_distribution': {
                    'high': high_trust,
                    'medium': medium_trust,
                    'low': low_trust
                }
            }
        }


# Test
if __name__ == "__main__":
    scorer = SourceScorer()
    
    # Test sources
    test_sources = [
        {
            'url': 'https://arxiv.org/abs/2024.12345',
            'title': 'Deep Learning Research',
            'content': 'A comprehensive study on neural networks... ' * 100,
            'published_date': '2024-11-01'
        },
        {
            'url': 'https://medium.com/@someone/ai-article',
            'title': 'AI is Cool',
            'content': 'Short blog post about AI.',
            'published_date': '2023-01-15'
        },
        {
            'url': 'https://bbc.com/news/technology-12345',
            'title': 'Tech News',
            'content': 'Breaking news about technology... ' * 50,
            'published_date': '2024-12-01'
        }
    ]
    
    print("="*70)
    print("SOURCE SCORING TEST")
    print("="*70 + "\n")
    
    scored = scorer.score_multiple_sources(test_sources)
    
    for source in scored:
        print(f"URL: {source['url']}")
        print(f"Score: {source['score']}/100 ({source['trust_level']})")
        print(f"Breakdown: {source['breakdown']}")
        print(f"Badges: {' '.join(source['badges'])}")
        print()
    
    # Diversity
    diversity = scorer.calculate_diversity_score(scored)
    print(f"Diversity Score: {diversity['score']}/100")
    print(f"Analysis: {diversity['analysis']}")
