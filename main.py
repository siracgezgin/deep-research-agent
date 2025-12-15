"""
Ana Çalıştırıcı - CLI veya UI
=============================

Kullanım:
  python main.py                           # Streamlit UI başlat
  python main.py --cli "konu"              # CLI mode
  python main.py --test                    # Test mode
"""

import sys
import os
import argparse
import asyncio

# Proje root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.workflow.orchestrator import ResearchOrchestrator


def run_ui():
    """Streamlit UI'ı başlat"""
    import subprocess
    
    ui_file = os.path.join(os.path.dirname(__file__), 'src', 'ui', 'app.py')
    
    print("\n🌐 Streamlit UI başlatılıyor...")
    print("   Tarayıcınızda otomatik açılacak\n")
    print("   Manuel açmak için: http://localhost:8501\n")
    
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run',
        ui_file,
        '--server.headless=true'
    ])


async def run_cli(topic: str, context: str = None):
    """CLI modunda çalıştır"""
    
    orchestrator = ResearchOrchestrator()
    
    print("\n🚀 CLI Mode: Deep Research başlatılıyor...\n")
    
    results = await orchestrator.run_research(topic, context)
    
    if results['success']:
        # Sonuçları kaydet
        files = orchestrator.save_results(results)
        
        print("\n✅ İşlem tamamlandı!")
        print(f"\n📄 Rapor: {files['report']}")
    else:
        print(f"\n❌ Hata: {results.get('error')}")


def run_test():
    """Test modunda çalıştır"""
    
    print("\n🧪 Test Mode\n")
    
    # Test konusu
    topic = "Yapay zeka ve eğitim: Fırsatlar ve zorluklar"
    
    print(f"Test Konusu: {topic}\n")
    
    asyncio.run(run_cli(topic))


def main():
    parser = argparse.ArgumentParser(
        description="AI Deep Research Agent - Otomatik araştırma ve rapor üretme",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python main.py                                    # UI mode (varsayılan)
  python main.py --cli "Kuantum bilgisayarlar"      # CLI mode
  python main.py --test                             # Test mode
        """
    )
    
    parser.add_argument(
        '--cli',
        type=str,
        metavar='TOPIC',
        help='CLI modunda çalıştır (konuyu gir)'
    )
    
    parser.add_argument(
        '--context',
        type=str,
        metavar='CONTEXT',
        help='Ek bağlam (opsiyonel, --cli ile kullan)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test modunda çalıştır'
    )
    
    args = parser.parse_args()
    
    # Mode seçimi
    if args.test:
        run_test()
    elif args.cli:
        asyncio.run(run_cli(args.cli, args.context))
    else:
        # Default: UI
        run_ui()


if __name__ == "__main__":
    main()
