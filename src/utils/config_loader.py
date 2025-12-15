"""
Config Loader - YAML Konfigürasyon Yönetimi
==========================================

config.yaml dosyasını okur ve environment variables ile merge eder.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv

# .env yükle
load_dotenv()

# Config dosyası yolu
CONFIG_FILE = Path(__file__).parent.parent.parent / "config.yaml"


class Config:
    """Singleton config manager"""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """YAML dosyasını yükle ve env vars ile merge et"""
        
        # YAML oku
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
        else:
            self._config = {}
            print(f"⚠️  Config dosyası bulunamadı: {CONFIG_FILE}")
        
        # Environment variables ile değiştir
        self._replace_env_vars(self._config)
    
    def _replace_env_vars(self, config: Any) -> Any:
        """${VAR_NAME} formatındaki environment variable'ları değiştir"""
        
        if isinstance(config, dict):
            for key, value in config.items():
                config[key] = self._replace_env_vars(value)
        
        elif isinstance(config, list):
            return [self._replace_env_vars(item) for item in config]
        
        elif isinstance(config, str) and config.startswith('${') and config.endswith('}'):
            # ${VAR_NAME} → os.getenv('VAR_NAME')
            var_name = config[2:-1]
            return os.getenv(var_name, config)
        
        return config
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Nested key'leri al (örnek: 'models.planner')
        
        Args:
            key_path: Nokta ile ayrılmış key yolu
            default: Varsayılan değer
        
        Returns:
            Config değeri veya default
        """
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """Tüm config'i döndür"""
        return self._config.copy()
    
    def reload(self):
        """Config'i yeniden yükle"""
        self._load_config()


# Singleton instance
config = Config()


# Kolaylık fonksiyonları
def get_config(key_path: str, default: Any = None) -> Any:
    """Config değeri al"""
    return config.get(key_path, default)


def get_model_name(agent_type: str) -> str:
    """Agent için model adı al"""
    return config.get(f'models.{agent_type}', 'gemini-2.5-flash')


def get_rate_limit() -> int:
    """Dakikadaki maksimum request sayısı"""
    return config.get('rate_limits.requests_per_minute', 5)


def should_enable_scraping() -> bool:
    """Web scraping açık mı?"""
    return config.get('research.enable_scraping', False)


# Test
if __name__ == "__main__":
    print("\n" + "="*70)
    print("CONFIG TEST")
    print("="*70 + "\n")
    
    print("Planner model:", get_model_name('planner'))
    print("Rate limit:", get_rate_limit(), "req/min")
    print("Max subtopics:", get_config('research.max_subtopics'))
    print("Scraping enabled:", should_enable_scraping())
    print("Log level:", get_config('logging.level'))
    
    print("\nTüm config:")
    import json
    print(json.dumps(config.get_all(), indent=2, ensure_ascii=False))
