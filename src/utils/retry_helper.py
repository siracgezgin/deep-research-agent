"""
Retry Helper - API Çağrıları İçin Tekrar Deneme
=============================================

429 (Rate Limit) ve diğer geçici hatalar için otomatik retry.
"""

import time
import functools
from typing import Callable, Any
from loguru import logger


def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retry_on_exceptions: tuple = (Exception,)
):
    """
    Exponential backoff ile retry decorator
    
    Args:
        max_retries: Maksimum deneme sayısı
        initial_delay: İlk bekleme süresi (saniye)
        exponential_base: Her denemede çarpan
        jitter: Rastgele gecikme ekle (aynı anda birçok istek varsa)
        retry_on_exceptions: Hangi hatalarda retry yapılacak
    
    Kullanım:
        @retry_with_exponential_backoff(max_retries=3)
        def api_call():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                
                except retry_on_exceptions as e:
                    # 429 Rate Limit hatası - API'den gelen retry süresi varsa kullan
                    if "429" in str(e) and "retry" in str(e).lower():
                        # API'den önerilen süreyi çıkar
                        import re
                        match = re.search(r'retry.*?(\d+)', str(e), re.IGNORECASE)
                        if match:
                            api_suggested_delay = int(match.group(1))
                            delay = api_suggested_delay
                            logger.warning(
                                f"Rate limit! API {api_suggested_delay}s beklememi öneriyor."
                            )
                    
                    # Son deneme ise hatayı fırlat
                    if attempt == max_retries - 1:
                        logger.error(
                            f"{func.__name__} başarısız oldu ({max_retries} deneme sonrası): {e}"
                        )
                        raise
                    
                    # Bekle ve tekrar dene
                    wait_time = delay
                    if jitter:
                        import random
                        wait_time = delay * (0.5 + random.random())
                    
                    logger.info(
                        f"{func.__name__} başarısız (deneme {attempt + 1}/{max_retries}). "
                        f"{wait_time:.1f}s bekleniyor... Hata: {str(e)[:100]}"
                    )
                    
                    time.sleep(wait_time)
                    delay *= exponential_base
        
        return wrapper
    return decorator


def smart_rate_limiter(calls_per_minute: int = 5):
    """
    Akıllı rate limiter - dakikada N çağrı sınırı
    
    Args:
        calls_per_minute: Dakikada maksimum çağrı sayısı
    
    Kullanım:
        @smart_rate_limiter(calls_per_minute=5)
        def api_call():
            ...
    """
    def decorator(func: Callable) -> Callable:
        calls = []  # (timestamp, ) listesi
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            nonlocal calls
            
            now = time.time()
            
            # 1 dakikadan eski çağrıları temizle
            calls = [t for t in calls if now - t < 60]
            
            # Limit aşıldıysa bekle
            if len(calls) >= calls_per_minute:
                oldest_call = min(calls)
                wait_time = 60 - (now - oldest_call)
                
                if wait_time > 0:
                    logger.warning(
                        f"Rate limit: {calls_per_minute}/dakika doldu. "
                        f"{wait_time:.1f}s bekleniyor..."
                    )
                    time.sleep(wait_time)
            
            # Çağrıyı kaydet
            calls.append(time.time())
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Test
if __name__ == "__main__":
    @retry_with_exponential_backoff(max_retries=3, initial_delay=1.0)
    def flaky_api_call(fail_count: int = 2):
        """Bazen başarısız olan mock API"""
        import random
        
        if random.random() < 0.7:  # %70 hata şansı
            raise Exception("API geçici olarak kullanılamıyor")
        
        return "Başarılı!"
    
    print("Test ediliyor...")
    result = flaky_api_call()
    print(f"Sonuç: {result}")
