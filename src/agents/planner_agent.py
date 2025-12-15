"""
Planner Agent - Araştırma Planlayıcısı
=====================================

Görev: Verilen konuyu analiz edip araştırma planı oluştur

Çıktı:
- Ana konu tanımı
- 3-5 alt başlık
- Her başlık için önerilen kaynak türü (web, academic, news vb)
"""

import os
import sys
import time
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai

# Proje utils'leri
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.retry_helper import retry_with_exponential_backoff
from src.utils.config_loader import get_model_name, get_config
from src.utils.logger import logger, log_agent_action

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


class PlannerAgent:
    """Araştırma planı oluşturan ajan"""
    
    def __init__(self, model_name=None):
        # Config'den model al, verilmemişse
        self.model_name = model_name or get_model_name('planner')
        logger.info(f"PlannerAgent başlatıldı (model={self.model_name})")
        
        system_instruction = """Sen bir uzman araştırma planlayıcısısın.

GÖREV:
Verilen konuyu analiz et ve kapsamlı bir araştırma planı oluştur.

PLAN YAPISI:
1. Ana konuyu net tanımla
2. Konuyu 4-6 alt başlığa böl
3. Her alt başlık için:
   - Net ve spesifik soru/hedef yaz
   - Önerilen kaynak türü (web, academic, news, forum)
   - Tahmini önem derecesi (1-5)

KURALLAR:
- Alt başlıklar birbirini tamamlamalı (overlap olmamalı)
- Her başlık araştırılabilir olmalı (çok genel veya çok spesifik olmamalı)
- Kronolojik veya mantıksal sıra önemli
- İlk başlık "genel tanım/giriş", son başlık "sonuç/gelecek"

ÇIKTI FORMATI:
{
  "topic": "Ana konu başlığı",
  "description": "Konunun kısa açıklaması",
  "subtopics": [
    {
      "title": "Alt başlık",
      "question": "Bu başlıkta yanıtlanacak soru",
      "source_type": "web/academic/news/forum",
      "priority": 1-5
    }
  ]
}

JSON formatında yanıt ver, başka açıklama ekleme.
"""
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_instruction,
            generation_config={
                "temperature": 0.7,  # Yaratıcı ama kontrollü
                "response_mime_type": "application/json"  # JSON zorla
            }
        )
    
    def create_plan(self, topic: str, context: str = None) -> Dict:
        """
        Konu için araştırma planı oluştur
        
        Args:
            topic: Ana araştırma konusu
            context: Ek bağlam (opsiyonel) - kullanıcının ek notları
        
        Returns:
            dict: {topic, description, subtopics[]}
        """
        prompt = f"Araştırma Konusu: {topic}"
        
        if context:
            prompt += f"\n\nEk Bağlam: {context}"
        
        prompt += "\n\nBu konu için detaylı araştırma planı oluştur."
        
        log_agent_action("PlannerAgent", "create_plan_start", {"topic": topic[:50]})
        
        # Retry wrapper ile API çağrısı
        @retry_with_exponential_backoff(max_retries=3)
        def _call_api():
            return self.model.generate_content(prompt)
        
        response = _call_api()
        
        # Rate limit: 5 req/min = 12 saniye arası gerekli
        time.sleep(13)
        
        # JSON parse (Gemini zaten JSON döner)
        import json
        plan = json.loads(response.text)
        
        log_agent_action("PlannerAgent", "create_plan_complete", {
            "subtopics_count": len(plan.get('subtopics', []))
        })
        
        return plan
    
    def refine_plan(self, initial_plan: Dict, feedback: str) -> Dict:
        """
        Kullanıcı geri bildirimine göre planı iyileştir
        
        Args:
            initial_plan: İlk plan
            feedback: Kullanıcı geri bildirimi
        
        Returns:
            dict: Güncellenmiş plan
        """
        import json
        
        prompt = f"""Mevcut Plan:
{json.dumps(initial_plan, indent=2, ensure_ascii=False)}

Kullanıcı Geri Bildirimi:
{feedback}

Bu geri bildirime göre planı güncelle. Aynı JSON formatında döndür.
"""
        
        response = self.model.generate_content(prompt)
        updated_plan = json.loads(response.text)
        
        return updated_plan
    
    def validate_plan(self, plan: Dict) -> Dict[str, bool]:
        """
        Planın kalitesini kontrol et
        
        Returns:
            dict: {is_valid, has_subtopics, subtopics_count, issues[]}
        """
        issues = []
        
        # Zorunlu alanlar
        if 'topic' not in plan or not plan['topic']:
            issues.append("Ana konu eksik")
        
        if 'subtopics' not in plan or not plan['subtopics']:
            issues.append("Alt başlık yok")
        
        # Alt başlık sayısı
        subtopics_count = len(plan.get('subtopics', []))
        if subtopics_count < 3:
            issues.append(f"Çok az alt başlık ({subtopics_count}), minimum 3 olmalı")
        elif subtopics_count > 8:
            issues.append(f"Çok fazla alt başlık ({subtopics_count}), maximum 8 olmalı")
        
        # Her alt başlık kontrolü
        for i, subtopic in enumerate(plan.get('subtopics', []), 1):
            if 'title' not in subtopic or not subtopic['title']:
                issues.append(f"Alt başlık {i}: Başlık eksik")
            
            if 'question' not in subtopic or not subtopic['question']:
                issues.append(f"Alt başlık {i}: Soru eksik")
        
        return {
            'is_valid': len(issues) == 0,
            'has_subtopics': subtopics_count > 0,
            'subtopics_count': subtopics_count,
            'issues': issues
        }


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 PLANNER AGENT TEST")
    print("="*70 + "\n")
    
    # Agent oluştur
    planner = PlannerAgent()
    
    # Test 1: Basit plan
    print("Test 1: Basit Plan Oluşturma\n")
    topic = "Kuantum bilgisayarların geleceği"
    
    print(f"📋 Konu: {topic}")
    print("🔄 Plan oluşturuluyor...\n")
    
    plan = planner.create_plan(topic)
    
    print("✅ Plan hazır!\n")
    print(f"📌 Ana Konu: {plan['topic']}")
    print(f"📝 Açıklama: {plan['description']}\n")
    print("📚 Alt Başlıklar:")
    
    for i, subtopic in enumerate(plan['subtopics'], 1):
        print(f"\n{i}. {subtopic['title']}")
        print(f"   ❓ {subtopic['question']}")
        print(f"   🔗 Kaynak: {subtopic['source_type']}")
        print(f"   ⭐ Öncelik: {subtopic['priority']}/5")
    
    # Test 2: Validasyon
    print("\n" + "="*70)
    print("Test 2: Plan Validasyonu\n")
    
    validation = planner.validate_plan(plan)
    
    if validation['is_valid']:
        print("✅ Plan geçerli!")
    else:
        print("❌ Plan sorunlu:")
        for issue in validation['issues']:
            print(f"   • {issue}")
    
    print(f"\n📊 İstatistikler:")
    print(f"   • Alt başlık sayısı: {validation['subtopics_count']}")
    print(f"   • Geçerli: {validation['is_valid']}")
    
    # Planı kaydet
    import json
    output_file = "examples/output_planner_plan.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Plan kaydedildi: {output_file}")
    
    print("\n" + "="*70)
    print("✅ TEST TAMAMLANDI")
    print("="*70 + "\n")
