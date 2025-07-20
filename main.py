#!/usr/bin/env python3
"""
Windows launcher for Lünen Terminplaner
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installiere Python-Pakete...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 
            '-r', 'requirements.txt', '--user', '--quiet'
        ], check=True)
        print("✅ Pakete installiert")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler bei Installation: {e}")
        return False

def open_browser():
    """Open browser after Flask starts"""
    time.sleep(3)  # Wait for Flask to start
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Browser geöffnet")
    except Exception as e:
        print(f"❌ Browser konnte nicht geöffnet werden: {e}")
        print("📝 Öffnen Sie manuell: http://localhost:5000")

def main():
    print("🚀 Lünen Terminplaner für Windows")
    print("=" * 40)
    
    # Install requirements first
    if not install_requirements():
        input("❌ Installation fehlgeschlagen. Drücken Sie Enter zum Beenden...")
        return 1
    
    # Import Flask app after installation
    try:
        from app import app
    except ImportError as e:
        print(f"❌ Fehler beim Laden der App: {e}")
        input("Drücken Sie Enter zum Beenden...")
        return 1
    
    print("🌐 Starte Web-Server auf http://localhost:5000")
    print("📝 Zum Beenden: Strg+C drücken")
    print("-" * 40)
    
    # Start browser in separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n🛑 Anwendung wird beendet...")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        input("Drücken Sie Enter zum Beenden...")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
