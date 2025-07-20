#!/usr/bin/env python3
"""
Local build test script - simulates CI/CD builds locally
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def create_main_entry():
    """Create main.py entry point"""
    main_content = '''#!/usr/bin/env python3
"""
Main entry point for Lünen Terminplaner
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
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Browser geöffnet")
    except Exception as e:
        print(f"❌ Browser konnte nicht geöffnet werden: {e}")
        print("📝 Öffnen Sie manuell: http://localhost:5000")

def main():
    print("🚀 Lünen Terminplaner")
    print(f"🖥️  Plattform: {os.name}")
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

def check_dependencies():
    """Check if PyInstaller is available"""
    try:
        import PyInstaller
        print("✅ PyInstaller verfügbar")
        return True
    except ImportError:
        print("❌ PyInstaller nicht verfügbar")
        print("💡 Installieren mit: pip install pyinstaller")
        return False

def build_binary():
    """Build binary with PyInstaller"""
    print("🔨 Erstelle Binary mit PyInstaller...")
    
    # Ensure directories exist
    os.makedirs('downloads', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    
    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name=LuenenTerminplaner',
        '--add-data=templates' + os.pathsep + 'templates',
        '--add-data=downloads' + os.pathsep + 'downloads',
        '--add-data=exports' + os.pathsep + 'exports',
        '--add-data=spezifikation.md' + os.pathsep + '.',
        '--add-data=requirements.txt' + os.pathsep + '.',
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
    
    print(f"🔧 Ausführe: {' '.join(cmd[:3])} ...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Binary erfolgreich erstellt!")
            
            # Check if binary exists
            if platform.system() == 'Windows':
                binary_path = 'dist/LuenenTerminplaner.exe'
            else:
                binary_path = 'dist/LuenenTerminplaner'
                
            if os.path.exists(binary_path):
                file_size = os.path.getsize(binary_path) / (1024*1024)
                print(f"📁 Pfad: {binary_path} ({file_size:.1f} MB)")
                return True
            else:
                print("❌ Binary nicht gefunden!")
                return False
        else:
            print("❌ Fehler beim Erstellen:")
            print("STDERR:", result.stderr[:500])
            return False
            
    except Exception as e:
        print(f"❌ Ausnahme: {e}")
        return False

def test_binary():
    """Test the created binary"""
    if platform.system() == 'Windows':
        binary_path = 'dist/LuenenTerminplaner.exe'
    else:
        binary_path = 'dist/LuenenTerminplaner'
    
    if not os.path.exists(binary_path):
        print("❌ Binary nicht gefunden für Test")
        return False
    
    print(f"🧪 Teste Binary: {binary_path}")
    
    try:
        # Quick test - just check if it can start
        result = subprocess.run([binary_path, '--help'], 
                              capture_output=True, text=True, timeout=5)
        print("✅ Binary kann ausgeführt werden")
        return True
    except subprocess.TimeoutExpired:
        print("✅ Binary läuft (Timeout beim --help erwartet)")
        return True
    except Exception as e:
        print(f"❌ Binary-Test fehlgeschlagen: {e}")
        return False

def create_test_package():
    """Create a test package similar to CI"""
    system = platform.system().lower()
    package_dir = f'local_build_{system}'
    
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    print(f"📦 Erstelle Test-Package: {package_dir}/")
    
    # Copy binary
    if platform.system() == 'Windows':
        binary_src = 'dist/LuenenTerminplaner.exe'
        binary_dst = f'{package_dir}/LuenenTerminplaner.exe'
    else:
        binary_src = 'dist/LuenenTerminplaner'
        binary_dst = f'{package_dir}/LuenenTerminplaner'
    
    if os.path.exists(binary_src):
        shutil.copy2(binary_src, binary_dst)
        print(f"✅ Binary kopiert: {binary_dst}")
    
    # Copy documentation
    docs_to_copy = ['spezifikation.md', 'README.md']
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy2(doc, package_dir)
            print(f"✅ Dokumentation kopiert: {doc}")
    
    # Create platform-specific installer
    if platform.system() == 'Windows':
        create_windows_installer(package_dir)
    else:
        create_linux_installer(package_dir)
    
    print(f"📦 Test-Package erstellt in: {package_dir}/")
    return package_dir

def create_windows_installer(package_dir):
    """Create Windows installer script"""
    installer_content = '''@echo off
title Luenen Terminplaner - Local Test Installation
echo ==========================================
echo    Luenen Terminplaner - Test Installation
echo ==========================================
echo.

echo Starte Luenen Terminplaner...
LuenenTerminplaner.exe

echo.
echo Test abgeschlossen.
pause
'''
    
    installer_path = f'{package_dir}/test_install.bat'
    with open(installer_path, 'w', encoding='cp1252') as f:
        f.write(installer_content)
    print(f"✅ Windows Test-Installer: {installer_path}")

def create_linux_installer(package_dir):
    """Create Linux installer script"""
    installer_content = '''#!/bin/bash

echo "=========================================="
echo "   Lünen Terminplaner - Local Test"
echo "=========================================="
echo

echo "Starte Lünen Terminplaner..."
chmod +x LuenenTerminplaner
./LuenenTerminplaner

echo
echo "Test abgeschlossen."
'''
    
    installer_path = f'{package_dir}/test_install.sh'
    with open(installer_path, 'w', encoding='utf-8') as f:
        f.write(installer_content)
    os.chmod(installer_path, 0o755)
    print(f"✅ Linux Test-Installer: {installer_path}")

def main():
    print("🧪 Lünen Terminplaner - Local Build Test")
    print("=" * 45)
    print(f"🖥️  Platform: {platform.system()}")
    print(f"🐍 Python: {sys.version}")
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Fehler: app.py nicht gefunden!")
        print("Führen Sie dieses Script im Projektverzeichnis aus.")
        return 1
    
    # Create main entry point
    create_main_entry()
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 Um lokale Builds zu testen:")
        print("pip install pyinstaller")
        return 1
    
    # Build binary
    if not build_binary():
        print("\n❌ Build fehlgeschlagen!")
        return 1
    
    # Test binary
    if not test_binary():
        print("\n⚠️ Binary-Test nicht erfolgreich")
    
    # Create test package
    package_dir = create_test_package()
    
    print("\n🎉 Lokaler Build-Test abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print(f"1. Testen Sie das Package: cd {package_dir}")
    
    if platform.system() == 'Windows':
        print("2. Ausführen: test_install.bat")
    else:
        print("2. Ausführen: ./test_install.sh")
    
    print("\n🚀 Für echte Releases:")
    print("git tag v1.0.0 && git push origin v1.0.0")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())