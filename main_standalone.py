#!/usr/bin/env python3
"""
Standalone executable entry point for Lünen Terminplaner
Optimized for PyInstaller compilation
"""

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

def open_browser():
    """Open browser after Flask starts"""
    time.sleep(3)  # Wait for Flask to start
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Browser geöffnet auf http://localhost:5000")
    except Exception as e:
        print(f"⚠️ Browser konnte nicht automatisch geöffnet werden: {e}")
        print("📝 Öffnen Sie manuell: http://localhost:5000")

def main():
    """Main entry point"""
    print("🚀 Lünen Terminplaner - Standalone Version")
    print("=" * 50)
    print("📊 Flask-Server startet auf http://localhost:5000")
    print("🌐 Browser wird automatisch geöffnet...")
    print()
    print("📝 Zum Beenden: Strg+C drücken")
    print("=" * 50)
    
    try:
        # Import Flask app
        from app import app
        
        # Start browser in separate thread
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start Flask app
        app.run(
            debug=False, 
            host='127.0.0.1', 
            port=5000, 
            use_reloader=False
        )
        
    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        print("🔧 Stellen Sie sicher, dass alle Abhängigkeiten installiert sind.")
        input("Drücken Sie Enter zum Beenden...")
        return 1
    except KeyboardInterrupt:
        print("\n🛑 Anwendung wird beendet...")
        return 0
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")
        input("Drücken Sie Enter zum Beenden...")
        return 1

if __name__ == '__main__':
    sys.exit(main())