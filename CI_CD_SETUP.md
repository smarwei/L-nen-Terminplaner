# 🚀 CI/CD Pipeline Setup für Lünen Terminplaner

## 🎯 Übersicht

Automatische Builds für **Windows EXE** und **Linux AppImage** bei jedem Release!

## 📋 GitHub Actions Workflows

### 1. 🏗️ **build-releases.yml** (Produktions-Builds)
**Trigger:** Git Tags (`v*.*.*`) oder Releases  
**Outputs:** 
- `LuenenTerminplaner.exe` (Windows)
- `LuenenTerminplaner_Windows.zip` (Windows Package) 
- `LuenenTerminplaner.AppImage` (Linux)
- `LuenenTerminplaner_Linux.tar.gz` (Linux Package)

### 2. 🧪 **test-and-build.yml** (Development)
**Trigger:** Push zu main/master/develop  
**Checks:**
- Tests auf Python 3.8-3.11
- Code Quality (Black, flake8, isort)
- Security Scans (Bandit, Safety)
- Build-Tests
- Web Interface Tests
- Documentation Checks

## 🔄 Release-Workflow

### Automatischer Release:
```bash
# 1. Tag erstellen
git tag v1.0.0
git push origin v1.0.0

# 2. GitHub Actions bauen automatisch:
#    - Windows EXE mit PyInstaller
#    - Linux AppImage 
#    - Installation Scripts
#    - Documentation

# 3. GitHub Release wird erstellt mit:
#    - Binaries für Windows & Linux
#    - Installer Scripts
#    - Release Notes
```

### Manueller Release:
```bash
# GitHub Interface nutzen:
# 1. Gehe zu Releases
# 2. "Create a new release"
# 3. Tag eingeben (z.B. v1.0.0)
# 4. Titel und Beschreibung
# 5. "Publish release"
# 6. Pipeline startet automatisch
```

## 🛠️ Build-Details

### Windows Build (.github/workflows/build-releases.yml):
```yaml
- name: Build Windows EXE
  run: |
    # PyInstaller with all dependencies
    pyinstaller --onefile --name=LuenenTerminplaner \
      --add-data="templates;templates" \
      --add-data="downloads;downloads" \
      --hidden-import=flask \
      --hidden-import=sumy.parsers.plaintext \
      --console main.py
```

### Linux AppImage Build:
```yaml
- name: Create AppImage
  run: |
    # Build PyInstaller binary
    pyinstaller --onefile LuenenTerminplaner
    
    # Create AppDir structure
    mkdir -p AppDir/usr/bin
    cp dist/LuenenTerminplaner AppDir/usr/bin/
    
    # Create desktop integration
    # Build AppImage with appimagetool
```

## 📦 Erstellte Artefakte

### Windows Release Package:
```
LuenenTerminplaner_Windows.zip
├── LuenenTerminplaner.exe      # Standalone EXE
├── install.bat                 # Windows Installer
├── README_Windows.md           # Windows Anleitung
└── spezifikation.md           # Projekt-Docs
```

### Linux Release Package:
```
LuenenTerminplaner_Linux.tar.gz
├── LuenenTerminplaner.AppImage # Portable AppImage
├── install-linux.sh           # Linux Installer  
├── README_Linux.md             # Linux Anleitung
└── spezifikation.md           # Projekt-Docs
```

## 🔧 Setup-Schritte

### 1. Repository vorbereiten:
```bash
# .gitignore bereits erstellt ✅
# Workflows bereits erstellt ✅

# Erste Commits
git add .gitignore .github/
git commit -m "Add CI/CD pipeline with Windows EXE and Linux AppImage builds"
git push origin main
```

### 2. Ersten Release erstellen:
```bash
# Version taggen
git tag v1.0.0
git push origin v1.0.0

# ODER: GitHub Interface nutzen
# Gehe zu: Releases → Create a new release
```

### 3. GitHub Secrets (Optional):
Für erweiterte Features können Secrets hinzugefügt werden:
- `GITHUB_TOKEN` (automatisch verfügbar)
- `DISCORD_WEBHOOK` (für Notifications)
- `TELEGRAM_BOT_TOKEN` (für Notifications)

## 🎯 Workflow-Trigger

### Automatische Triggers:
```yaml
# Release builds
on:
  push:
    tags: ['v*.*.*', 'release-*']
  release:
    types: [published]

# Development builds  
on:
  push:
    branches: [main, master, develop]
  pull_request:
    branches: [main, master, develop]
```

### Manuelle Triggers:
```yaml
# Manual workflow dispatch
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version tag'
        required: true
        default: 'v1.0.0'
```

## 📊 Build-Matrix

### Test Matrix:
- **Python:** 3.8, 3.9, 3.10, 3.11
- **OS:** Ubuntu Latest, Windows Latest
- **Quality:** Black, flake8, isort, Bandit, Safety

### Build Matrix:
- **Windows:** PyInstaller → EXE
- **Linux:** PyInstaller → AppImage
- **Package:** ZIP (Windows), tar.gz (Linux)

## 🚀 Nach dem Setup

### Jeder Release erstellt automatisch:
1. **GitHub Release** mit beschreibenden Release Notes
2. **Windows EXE** - direkt ausführbar
3. **Linux AppImage** - portable für alle Distributionen
4. **Installer Scripts** - benutzerfreundliche Installation
5. **Dokumentation** - plattformspezifische READMEs

### Benutzer können dann:
- Windows: ZIP herunterladen, install.bat ausführen
- Linux: tar.gz herunterladen, install-linux.sh ausführen  
- Entwickler: Einzelne Binaries für Testing herunterladen

## 🎉 Vorteile

### ✅ **Automatisierung:**
- Keine manuellen Builds mehr
- Konsistente Build-Umgebung
- Reproduzierbare Releases

### ✅ **Qualitätssicherung:**
- Alle Tests laufen vor Release
- Code-Quality-Checks
- Security-Scans

### ✅ **Multi-Platform:**
- Windows EXE automatisch
- Linux AppImage automatisch
- Plattformspezifische Installer

### ✅ **Benutzerfreundlichkeit:**
- Ein-Klick Downloads
- Automatische Release Notes
- Professionelle Präsentation

**Die Pipeline ist bereit! Beim nächsten `git tag v1.0.0` werden automatisch Windows EXE und Linux AppImage gebaut! 🚀**