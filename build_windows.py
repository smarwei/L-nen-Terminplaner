#!/usr/bin/env python3
"""
Build script to create Windows executable from Flask app
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

def create_pyinstaller_spec():
    """Create PyInstaller spec file"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('downloads', 'downloads'),
        ('exports', 'exports'),
        ('*.py', '.'),
        ('requirements.txt', '.'),
        ('spezifikation.md', '.'),
        ('*.md', '.'),
    ],
    hiddenimports=[
        'flask',
        'requests',
        'beautifulsoup4',
        'sumy',
        'sumy.parsers.plaintext',
        'sumy.nlp.tokenizers',
        'sumy.summarizers.lsa',
        'sumy.nlp.stemmers',
        'pdfplumber',
        'fitz',
        'PyMuPDF',
        'markdown',
        'weasyprint',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LuenenTerminplaner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('luenen_terminplaner.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("✅ PyInstaller spec file erstellt")

def install_dependencies():
    """Install required dependencies for building"""
    print("📦 Installiere Build-Dependencies...")
    
    dependencies = [
        'pyinstaller',
        'flask',
        'requests', 
        'beautifulsoup4',
        'sumy',
        'pdfplumber',
        'PyMuPDF',
        'markdown',
        'weasyprint'
    ]
    
    for dep in dependencies:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                         check=True, capture_output=True)
            print(f"✅ {dep} installiert")
        except subprocess.CalledProcessError as e:
            print(f"❌ Fehler bei {dep}: {e}")

def build_executable():
    """Build the Windows executable"""
    print("🔨 Erstelle Windows-Executable...")
    
    try:
        # Create directories if they don't exist
        os.makedirs('downloads', exist_ok=True)
        os.makedirs('exports', exist_ok=True)
        
        # Build with PyInstaller
        cmd = [sys.executable, '-m', 'PyInstaller', '--clean', 'luenen_terminplaner.spec']
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable erfolgreich erstellt!")
            print("📁 Pfad: dist/LuenenTerminplaner.exe")
        else:
            print("❌ Fehler beim Erstellen:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False
    
    return True

def create_installer_script():
    """Create a simple installer script"""
    installer_content = '''@echo off
echo ==========================================
echo    Luenen Terminplaner - Installation
echo ==========================================
echo.

if not exist "LuenenTerminplaner.exe" (
    echo FEHLER: LuenenTerminplaner.exe nicht gefunden!
    echo Bitte stellen Sie sicher, dass diese Datei im gleichen Ordner ist.
    pause
    exit /b 1
)

echo Erstelle Programmordner...
set "INSTALL_DIR=%USERPROFILE%\\LuenenTerminplaner"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Kopiere Dateien...
copy "LuenenTerminplaner.exe" "%INSTALL_DIR%\\" >nul
if exist "README.md" copy "README.md" "%INSTALL_DIR%\\" >nul

echo Erstelle Desktop-Verknuepfung...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Luenen Terminplaner.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\LuenenTerminplaner.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Luenen Terminplaner - Ratsinformationen automatisiert'; $Shortcut.Save()"

echo.
echo ========================================
echo Installation erfolgreich abgeschlossen!
echo ========================================
echo.
echo Das Programm wurde installiert in:
echo %INSTALL_DIR%
echo.
echo Eine Desktop-Verknuepfung wurde erstellt.
echo.
pause
'''
    
    with open('install.bat', 'w', encoding='cp1252') as f:
        f.write(installer_content)
    print("✅ Installer-Script erstellt: install.bat")

def create_readme():
    """Create Windows-specific README"""
    readme_content = '''# Lünen Terminplaner - Windows Version

## 📦 Installation

1. **Einfache Installation:**
   - Doppelklick auf `install.bat`
   - Folgen Sie den Anweisungen

2. **Manuelle Installation:**
   - Kopieren Sie `LuenenTerminplaner.exe` in einen Ordner Ihrer Wahl
   - Erstellen Sie eine Verknüpfung auf dem Desktop (optional)

## 🚀 Verwendung

1. **Programm starten:**
   - Doppelklick auf `LuenenTerminplaner.exe`
   - Ihr Browser öffnet sich automatisch mit der Anwendung

2. **Termine suchen:**
   - Wählen Sie Start- und Enddatum
   - Passen Sie die Gremien-Filter an
   - Klicken Sie "Termine laden"

3. **Programm beenden:**
   - Schließen Sie das Browser-Fenster
   - Drücken Sie Strg+C im Konsolen-Fenster

## 🔧 Systemanforderungen

- Windows 10 oder neuer
- Internetverbindung für das Scraping
- Mindestens 100 MB freier Speicherplatz

## ❓ Problembehebung

**Problem:** Programm startet nicht
- Lösung: Als Administrator ausführen
- Alternative: Windows Defender/Antivirus temporär deaktivieren

**Problem:** Browser öffnet sich nicht automatisch
- Lösung: Manuell http://localhost:5000 öffnen

**Problem:** Keine Termine gefunden
- Lösung: Internetverbindung prüfen
- Alternative: Anderen Datumsbereich wählen

## 📞 Support

Bei Problemen wenden Sie sich an den Entwickler oder 
erstellen Sie ein Issue im GitHub-Repository.

## 📄 Lizenz

Dieses Programm ist für die Nutzung mit öffentlichen 
Daten der Stadt Lünen entwickelt worden.
'''
    
    with open('README_Windows.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ Windows README erstellt")

def main():
    print("🏗️  Lünen Terminplaner - Windows Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Fehler: app.py nicht gefunden!")
        print("Führen Sie dieses Script im Projektverzeichnis aus.")
        return
    
    # Create necessary files
    create_main_entry_point()
    create_pyinstaller_spec()
    create_installer_script()
    create_readme()
    
    print("\n📋 Build-Optionen:")
    print("1. Nur Dateien erstellen (bereits erledigt)")
    print("2. Dependencies installieren und EXE erstellen")
    print("3. Vollständiger Build mit allem")
    
    choice = input("\nWählen Sie eine Option (1-3): ").strip()
    
    if choice in ['2', '3']:
        install_dependencies()
        
        if build_executable():
            print("\n🎉 Build erfolgreich!")
            print("\n📦 Erstellte Dateien:")
            print("- dist/LuenenTerminplaner.exe (Hauptprogramm)")
            print("- install.bat (Installer)")
            print("- README_Windows.md (Anleitung)")
            
            print("\n📋 Nächste Schritte:")
            print("1. Testen Sie die EXE: ./dist/LuenenTerminplaner.exe")
            print("2. Verpacken Sie für Distribution:")
            print("   - dist/LuenenTerminplaner.exe")
            print("   - install.bat") 
            print("   - README_Windows.md")
        else:
            print("\n❌ Build fehlgeschlagen!")
    
    print("\n✅ Script abgeschlossen!")

if __name__ == '__main__':
    main()