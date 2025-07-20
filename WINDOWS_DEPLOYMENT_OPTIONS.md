# Windows Deployment-Optionen für Lünen Terminplaner

## 🎯 Übersicht der Möglichkeiten

### 1. ✅ **PyInstaller (Empfohlen)**
**Vorteile:**
- Standalone EXE-Datei
- Keine Python-Installation auf Zielrechner nötig
- Funktioniert auch unter NixOS mit Cross-Compilation
- Einfache Distribution

**Nachteile:**
- Große Dateigröße (~50-100 MB)
- Langsamerer Start

**Umsetzung:**
```bash
python build_windows.py
```

### 2. 🐳 **Docker Desktop**
**Vorteile:**
- Identische Umgebung überall
- Einfaches Setup
- Keine Abhängigkeitsprobleme

**Nachteile:**
- Benutzer muss Docker installieren
- Etwas komplexer für Endbenutzer

**Umsetzung:**
```dockerfile
FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

### 3. 📦 **Windows Installer (MSI)**
**Vorteile:**
- Professioneller Installer
- Deinstallation möglich
- Registry-Integration

**Nachteile:**
- Komplexer zu erstellen
- Benötigt zusätzliche Tools

### 4. 🌐 **Portable Python Distribution**
**Vorteile:**
- Kein System-Python nötig
- Portable auf USB-Stick
- Kleinere Dateigröße als PyInstaller

**Nachteile:**
- Mehrere Dateien zu verteilen
- Benutzer sieht Python-Konsole

### 5. ☁️ **Web-Deployment (Heroku/Vercel)**
**Vorteile:**
- Keine lokale Installation
- Automatische Updates
- Von überall zugänglich

**Nachteile:**
- Internetverbindung nötig
- Hosting-Kosten
- Datenschutz-Bedenken

## 🚀 Empfohlener Workflow

### Schritt 1: PyInstaller EXE erstellen
```bash
# Unter NixOS
python build_windows.py

# Das erstellt:
# - main.py (Entry Point)
# - luenen_terminplaner.spec (PyInstaller Config)
# - dist/LuenenTerminplaner.exe (Windows Executable)
# - install.bat (Installer Script)
# - README_Windows.md (Benutzeranleitung)
```

### Schritt 2: Distribution Package
```
📦 LuenenTerminplaner_Windows.zip
├── 📄 LuenenTerminplaner.exe
├── 📄 install.bat
├── 📄 README_Windows.md
└── 📁 examples/
    ├── 📄 demo_export.html
    └── 📄 spezifikation.md
```

### Schritt 3: Benutzer-Installation
1. **Download** der ZIP-Datei
2. **Entpacken** in beliebigen Ordner
3. **Doppelklick** auf `install.bat` ODER
4. **Direkt ausführen** von `LuenenTerminplaner.exe`

## 🔧 Technische Details

### PyInstaller Konfiguration
```python
# luenen_terminplaner.spec
a = Analysis(
    ['main.py'],
    datas=[
        ('templates', 'templates'),  # Flask Templates
        ('downloads', 'downloads'),  # PDF Cache
        ('*.py', '.'),              # Python Module
    ],
    hiddenimports=[
        'flask', 'requests', 'beautifulsoup4',
        'sumy', 'pdfplumber', 'PyMuPDF'
    ],
)

exe = EXE(
    # ... Konfiguration für Windows EXE
    name='LuenenTerminplaner',
    console=True,  # Zeigt Konsole für Debug-Output
)
```

### Startup Behavior
```python
# main.py
def main():
    print("🚀 Lünen Terminplaner wird gestartet...")
    
    # Browser automatisch öffnen
    threading.Thread(target=open_browser).start()
    
    # Flask ohne Debug-Modus starten
    app.run(debug=False, host='127.0.0.1', port=5000)
```

## 🛠️ Build unter NixOS

### Option A: Native Cross-Compilation
```bash
# PyInstaller mit Wine
nix-shell -p wine python3Packages.pyinstaller
python build_windows.py
```

### Option B: Docker Build
```dockerfile
FROM python:3.10-windowsservercore
# Windows Container für echte Windows EXE
```

### Option C: GitHub Actions
```yaml
# .github/workflows/build-windows.yml
- uses: actions/setup-python@v4
  with:
    python-version: '3.10'
- run: python build_windows.py
- uses: actions/upload-artifact@v3
  with:
    name: windows-executable
    path: dist/LuenenTerminplaner.exe
```

## 📊 Vergleich der Optionen

| Methode | Größe | Setup-Aufwand | Benutzerfreundlichkeit | Wartung |
|---------|-------|---------------|----------------------|---------|
| PyInstaller EXE | ~80MB | Mittel | ⭐⭐⭐⭐⭐ | Einfach |
| Docker | ~200MB | Hoch | ⭐⭐⭐ | Mittel |
| MSI Installer | ~80MB | Hoch | ⭐⭐⭐⭐ | Mittel |
| Portable Python | ~150MB | Niedrig | ⭐⭐⭐ | Einfach |
| Web Deployment | 0MB | Mittel | ⭐⭐⭐⭐⭐ | Hoch |

## 🎯 Empfehlung

**Für die meisten Benutzer: PyInstaller EXE**
- Einfachste Distribution
- Keine technischen Kenntnisse erforderlich
- Funktioniert "out of the box"
- Kann auch ohne Internet-Installation verteilt werden

**Kommando zum Starten:**
```bash
python build_windows.py
```

Das erstellt eine vollständige Windows-Distribution!