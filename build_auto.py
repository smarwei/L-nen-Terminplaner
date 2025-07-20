#!/usr/bin/env python3
"""
Automated build script for Windows executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_main_entry_point():
    """Create a main.py entry point for PyInstaller"""
    main_content = '''#!/usr/bin/env python3
"""
Main entry point for Lünen Terminplaner Windows executable
"""

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from app import app

def open_browser():
    """Open browser after Flask starts"""
    time.sleep(2)  # Wait for Flask to start
    webbrowser.open('http://localhost:5000')

def main():
    print("🚀 Lünen Terminplaner wird gestartet...")
    print("📊 Flask-Server startet auf http://localhost:5000")
    print("🌐 Browser wird automatisch geöffnet...")
    print()
    print("📝 Zum Beenden: Strg+C drücken")
    print("=" * 50)
    
    # Start browser in separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\\n🛑 Anwendung wird beendet...")
        sys.exit(0)

if __name__ == '__main__':
    main()
'''
    
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(main_content)
    print("✅ main.py erstellt")

def install_pyinstaller():
    """Install PyInstaller"""
    print("📦 Installiere PyInstaller...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller', '--user'], 
                     check=True, capture_output=True)
        print("✅ PyInstaller installiert")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler bei PyInstaller Installation: {e}")
        return False

def build_executable():
    """Build the Windows executable"""
    print("🔨 Erstelle Windows-Executable...")
    
    try:
        # Create directories if they don't exist
        os.makedirs('downloads', exist_ok=True)
        os.makedirs('exports', exist_ok=True)
        
        # Build with PyInstaller directly
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--name=LuenenTerminplaner',
            '--add-data=templates:templates',
            '--add-data=downloads:downloads', 
            '--add-data=exports:exports',
            '--add-data=spezifikation.md:.',
            '--add-data=requirements.txt:.',
            '--hidden-import=flask',
            '--hidden-import=requests',
            '--hidden-import=beautifulsoup4',
            '--hidden-import=sumy.parsers.plaintext',
            '--hidden-import=sumy.nlp.tokenizers', 
            '--hidden-import=sumy.summarizers.lsa',
            '--hidden-import=sumy.nlp.stemmers',
            '--console',
            'main.py'
        ]
        
        print(f"🔧 Ausführe: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable erfolgreich erstellt!")
            if os.path.exists('dist/LuenenTerminplaner.exe'):
                file_size = os.path.getsize('dist/LuenenTerminplaner.exe') / (1024*1024)
                print(f"📁 Pfad: dist/LuenenTerminplaner.exe ({file_size:.1f} MB)")
                return True
            else:
                print("❌ EXE-Datei nicht gefunden!")
                return False
        else:
            print("❌ Fehler beim Erstellen:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

def main():
    print("🏗️  Lünen Terminplaner - Automatischer Windows Build")
    print("=" * 55)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Fehler: app.py nicht gefunden!")
        print("Führen Sie dieses Script im Projektverzeichnis aus.")
        return 1
    
    # Create main entry point
    create_main_entry_point()
    
    # Install PyInstaller
    if not install_pyinstaller():
        print("❌ Konnte PyInstaller nicht installieren!")
        return 1
    
    # Build executable
    if build_executable():
        print("\n🎉 Build erfolgreich!")
        print("\n📦 Erstellte Dateien:")
        if os.path.exists('dist/LuenenTerminplaner.exe'):
            print("✅ dist/LuenenTerminplaner.exe (Hauptprogramm)")
        if os.path.exists('install.bat'):
            print("✅ install.bat (Installer)")
        if os.path.exists('README_Windows.md'):
            print("✅ README_Windows.md (Anleitung)")
        
        print("\n📋 Test-Kommando:")
        print("cd dist && ./LuenenTerminplaner.exe")
        
        return 0
    else:
        print("\n❌ Build fehlgeschlagen!")
        return 1

if __name__ == '__main__':
    sys.exit(main())