"""
Logger Setup - Structured Logging
=================================

Loguru ile merkezi logging sistemi.
"""

import sys
from pathlib import Path
from loguru import logger

# Log klasörü
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_logger(
    log_level: str = "INFO",
    console: bool = True,
    file_output: bool = True,
    log_format: str = "detailed"
):
    """
    Logger'ı yapılandır
    
    Args:
        log_level: DEBUG, INFO, WARNING, ERROR
        console: Console'a log yaz
        file_output: Dosyaya log yaz
        log_format: simple, detailed, json
    """
    
    # Mevcut handler'ları temizle
    logger.remove()
    
    # Format seç
    if log_format == "simple":
        format_string = "<level>{level: <8}</level> | {message}"
    
    elif log_format == "json":
        format_string = "{message}"  # JSON serialize edilmiş
    
    else:  # detailed
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Console handler
    if console:
        logger.add(
            sys.stderr,
            format=format_string,
            level=log_level,
            colorize=True
        )
    
    # File handlers
    if file_output:
        # Ana log dosyası (tüm loglar)
        logger.add(
            LOG_DIR / "app.log",
            format=format_string,
            level=log_level,
            rotation="10 MB",      # 10 MB'da yeni dosya
            retention="7 days",    # 7 gün tut
            compression="zip",     # Sıkıştır
            enqueue=True          # Thread-safe
        )
        
        # Error log dosyası (sadece hatalar)
        logger.add(
            LOG_DIR / "errors.log",
            format=format_string,
            level="ERROR",
            rotation="5 MB",
            retention="30 days",
            compression="zip",
            enqueue=True
        )
    
    logger.info(f"Logger başlatıldı (level={log_level}, format={log_format})")


def log_agent_action(agent_name: str, action: str, details: dict = None):
    """Agent aksiyonlarını yapılandırılmış şekilde logla"""
    
    log_msg = f"[{agent_name}] {action}"
    
    if details:
        import json
        log_msg += f" | {json.dumps(details, ensure_ascii=False)}"
    
    logger.info(log_msg)


def log_api_call(endpoint: str, status: str, duration_ms: float = None, error: str = None):
    """API çağrılarını logla"""
    
    details = {
        "endpoint": endpoint,
        "status": status,
        "duration_ms": duration_ms
    }
    
    if error:
        details["error"] = error
        logger.error(f"API call failed | {details}")
    else:
        logger.info(f"API call | {details}")


# Default setup (import sırasında)
try:
    from src.utils.config_loader import get_config
    
    log_level = get_config('logging.level', 'INFO')
    log_format = get_config('logging.format', 'detailed')
    console_output = get_config('logging.console_output', True)
    file_output = get_config('logging.file_output', True)
    
    setup_logger(
        log_level=log_level,
        console=console_output,
        file_output=file_output,
        log_format=log_format
    )

except Exception as e:
    # Config yüklenemezse default ayarlarla başlat
    setup_logger(log_level="INFO", console=True, file_output=True, log_format="detailed")
    logger.warning(f"Config yüklenemedi, default logging ayarları kullanılıyor: {e}")


# Test
if __name__ == "__main__":
    logger.debug("Bu bir debug mesajı")
    logger.info("Bu bir info mesajı")
    logger.warning("Bu bir warning mesajı")
    logger.error("Bu bir error mesajı")
    
    log_agent_action("PlannerAgent", "create_plan", {"topic": "AI etiği", "subtopics": 6})
    log_api_call("gemini-2.5-flash", "success", 1234.5)
    log_api_call("gemini-2.5-flash", "error", 567.8, "429 Rate limit exceeded")
