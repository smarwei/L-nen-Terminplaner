#!/usr/bin/env python3
"""
Create a Windows distribution package without PyInstaller
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_windows_starter():
    """Create Windows batch starter and Python launcher"""
    
    # Windows Batch Starter
    batch_content = '''@echo off
title Luenen Terminplaner
echo ==========================================
echo    Luenen Terminplaner wird gestartet...
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert!
    echo.
    echo Bitte installieren Sie Python von:
    echo https://www.python.org/downloads/
    echo.
    echo Waehlen Sie bei der Installation "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Python gefunden, installiere Abhaengigkeiten...
python -m pip install -r requirements.txt --user --quiet

echo Starte Anwendung...
echo.
echo Die Anwendung startet auf: http://localhost:5000
echo Browser oeffnet sich automatisch...
echo.
echo Zum Beenden: Strg+C druecken oder dieses Fenster schliessen
echo.

python main.py
'''
    
    with open('start_windows.bat', 'w', encoding='cp1252') as f:
        f.write(batch_content)
    print("✅ start_windows.bat erstellt")

def create_python_launcher():
    """Create Python launcher script"""
    launcher_content = '''#!/usr/bin/env python3
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
        print("\\n🛑 Anwendung wird beendet...")
    except Exception as e:
        print(f"\\n❌ Fehler: {e}")
        input("Drücken Sie Enter zum Beenden...")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
'''
    
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    print("✅ main.py erstellt")

def create_windows_installer():
    """Create Windows installer script"""
    installer_content = '''@echo off
title Luenen Terminplaner - Installation
echo ==========================================
echo    Luenen Terminplaner - Installation
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo WARNUNG: Python ist nicht installiert!
    echo.
    echo Fuer die beste Erfahrung installieren Sie Python von:
    echo https://www.python.org/downloads/
    echo.
    echo Waehlen Sie bei der Installation "Add Python to PATH"
    echo.
)

echo Erstelle Programmordner...
set "INSTALL_DIR=%USERPROFILE%\\LuenenTerminplaner"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Kopiere Dateien...
xcopy /E /I /Y "." "%INSTALL_DIR%" >nul

echo Erstelle Desktop-Verknuepfung...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Luenen Terminplaner.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\start_windows.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Luenen Terminplaner - Ratsinformationen automatisiert'; $Shortcut.Save()"

echo.
echo ========================================
echo Installation erfolgreich abgeschlossen!
echo ========================================
echo.
echo Das Programm wurde installiert in:
echo %INSTALL_DIR%
echo.
echo Zum Starten:
echo 1. Desktop-Verknuepfung verwenden, ODER
echo 2. start_windows.bat doppelklicken
echo.
echo Bei erstem Start werden automatisch die
echo Python-Pakete installiert.
echo.
pause
'''
    
    with open('install.bat', 'w', encoding='cp1252') as f:
        f.write(installer_content)
    print("✅ install.bat erstellt")

def create_windows_readme():
    """Create comprehensive Windows README"""
    readme_content = '''# Lünen Terminplaner - Windows Distribution

## 🎯 Systemanforderungen

- Windows 10 oder neuer
- Python 3.8+ (empfohlen: Python 3.10)
- Internetverbindung für Downloads

## 📦 Installation

### Option 1: Automatische Installation (Empfohlen)
1. Doppelklick auf `install.bat`
2. Folgen Sie den Anweisungen im Fenster
3. Desktop-Verknüpfung wird automatisch erstellt

### Option 2: Portable Nutzung
1. Entpacken Sie alle Dateien in einen Ordner
2. Doppelklick auf `start_windows.bat`

## 🐍 Python Installation (falls erforderlich)

1. Besuchen Sie: https://www.python.org/downloads/
2. Laden Sie Python 3.10+ herunter
3. **WICHTIG:** Wählen Sie "Add Python to PATH" bei der Installation
4. Installieren Sie Python mit Standard-Einstellungen

## 🚀 Programm starten

### Nach Installation:
- Doppelklick auf Desktop-Verknüpfung "Lünen Terminplaner"

### Portable:
- Doppelklick auf `start_windows.bat`

### Was passiert beim ersten Start:
1. Konsolen-Fenster öffnet sich
2. Python-Pakete werden automatisch installiert (einmalig)
3. Web-Server startet auf http://localhost:5000
4. Browser öffnet sich automatisch mit der Anwendung

## 📋 Benutzung

1. **Datum wählen**: Start- und Enddatum festlegen
2. **Gremien filtern**: Gewünschte Ausschüsse auswählen
3. **"Termine laden"** klicken
4. **Ergebnisse ansehen**: Zusammenfassungen und Details
5. **Exportieren**: Als Markdown, HTML oder PDF

## 🛠️ Fehlerbehebung

### Problem: "Python ist nicht installiert"
**Lösung:** 
- Python von python.org herunterladen und installieren
- Bei Installation "Add Python to PATH" wählen
- Computer neu starten

### Problem: "Pakete können nicht installiert werden"
**Lösung:**
- Als Administrator ausführen
- Internetverbindung prüfen
- Antivirus temporär deaktivieren

### Problem: Browser öffnet sich nicht automatisch
**Lösung:**
- Manuell http://localhost:5000 im Browser öffnen
- Konsolen-Fenster offen lassen

### Problem: Anwendung startet nicht
**Lösung:**
- Rechtsklick auf .bat-Datei → "Als Administrator ausführen"
- Windows Defender Ausnahme hinzufügen
- Firewall-Freigabe für Python prüfen

### Problem: Keine Termine gefunden
**Lösung:**
- Internetverbindung prüfen
- Anderen Datumsbereich wählen
- Mehr Gremien auswählen

## 📁 Projektstruktur

```
LuenenTerminplaner/
├── start_windows.bat     # Haupt-Starter
├── main.py              # Python-Launcher
├── app.py               # Flask-Anwendung
├── scraper.py           # Web-Scraping
├── pdf_processor.py     # PDF-Verarbeitung
├── export_manager.py    # Export-Funktionen
├── requirements.txt     # Python-Abhängigkeiten
├── templates/           # HTML-Templates
├── downloads/           # PDF-Cache
└── exports/            # Exportierte Dateien
```

## 📞 Support

Bei Problemen:
1. Konsolen-Ausgabe prüfen (Fehlermeldungen)
2. Python-Version testen: `python --version`
3. Internetverbindung prüfen
4. Als Administrator ausführen

## 🔧 Erweiterte Nutzung

### Kommandozeile:
```cmd
cd LuenenTerminplaner
python main.py
```

### Anderen Port verwenden:
```cmd
# app.py bearbeiten, port=5000 ändern
```

### Debug-Modus:
```cmd
# app.py bearbeiten, debug=True setzen
```

## 📄 Lizenz

Dieses Programm nutzt öffentliche Daten der Stadt Lünen.
Entwickelt für die automatisierte Auswertung von Ratsinformationen.

---

🎉 **Viel Erfolg mit dem Lünen Terminplaner!**
'''
    
    with open('README_Windows.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ README_Windows.md erstellt")

def create_distribution_package():
    """Create a complete Windows distribution package"""
    
    # Create package directory
    package_dir = 'windows_distribution'
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Files to include in distribution
    files_to_copy = [
        'app.py',
        'scraper.py', 
        'pdf_processor.py',
        'export_manager.py',
        'requirements.txt',
        'spezifikation.md',
        'main.py',
        'start_windows.bat',
        'install.bat',
        'README_Windows.md'
    ]
    
    # Directories to copy
    dirs_to_copy = ['templates']
    
    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"📄 Kopiert: {file}")
    
    # Copy directories
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(package_dir, dir_name))
            print(f"📁 Kopiert: {dir_name}/")
    
    # Create empty directories
    os.makedirs(os.path.join(package_dir, 'downloads'), exist_ok=True)
    os.makedirs(os.path.join(package_dir, 'exports'), exist_ok=True)
    
    # Create ZIP file
    zip_filename = 'LuenenTerminplaner_Windows.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_name)
    
    # Get ZIP size
    zip_size = os.path.getsize(zip_filename) / (1024*1024)
    print(f"📦 ZIP erstellt: {zip_filename} ({zip_size:.1f} MB)")
    
    return package_dir, zip_filename

def main():
    print("📦 Lünen Terminplaner - Windows Distribution Creator")
    print("=" * 55)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Fehler: app.py nicht gefunden!")
        print("Führen Sie dieses Script im Projektverzeichnis aus.")
        return 1
    
    # Create all Windows files
    create_python_launcher()
    create_windows_starter()
    create_windows_installer()
    create_windows_readme()
    
    # Create distribution package
    package_dir, zip_file = create_distribution_package()
    
    print("\n🎉 Windows Distribution erfolgreich erstellt!")
    print("\n📦 Erstellte Dateien:")
    print(f"✅ {zip_file} (Komplett-Paket)")
    print(f"✅ {package_dir}/ (Entpacktes Verzeichnis)")
    
    print("\n📋 Für Windows-Benutzer:")
    print("1. LuenenTerminplaner_Windows.zip herunterladen")
    print("2. ZIP entpacken")
    print("3. install.bat ausführen (einmalig)")
    print("4. Desktop-Verknüpfung verwenden")
    
    print("\n📝 Test-Möglichkeiten:")
    print(f"cd {package_dir}")
    print("python main.py")
    
    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)