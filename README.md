# 🧾 Lünen Terminplaner

Ein automatisierter Ratsinfo-Scraper mit PDF-Zusammenfassung für die Stadt Lünen.

## 🎯 Funktionen

- **Webscraping** der Lünen Ratsinfomanagement-Website
- **PDF-Download** und Textextraktion aus Sitzungsdokumenten
- **Automatische Zusammenfassung** der PDF-Inhalte
- **Webbasierte GUI** mit modernem Design
- **Export-Funktionen** (Markdown, HTML, PDF, JSON)
- **Filterung** nach relevanten Gremien

## 🖥️ Installation

1. **Repository klonen**
   ```bash
   git clone <repository-url>
   cd luenen_terminplaner
   ```

2. **Virtuelle Umgebung erstellen**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # oder
   venv\Scripts\activate     # Windows
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Playwright Browser installieren** (für erweiterte Webscraping-Funktionen)
   ```bash
   playwright install chromium
   ```

## 🚀 Verwendung

1. **Server starten**
   ```bash
   python app.py
   ```

2. **Browser öffnen**
   Navigieren Sie zu `http://localhost:5000`

3. **Termine suchen**
   - Wählen Sie Start- und Enddatum
   - Klicken Sie auf "Termine laden"
   - Warten Sie auf die Verarbeitung der PDFs

4. **Ergebnisse exportieren**
   - Verwenden Sie die Export-Buttons für verschiedene Formate

## 📅 Relevante Gremien

Das System filtert automatisch nach folgenden Gremien:

- Rat der Stadt Lünen
- Rechnungsprüfungsausschuss
- Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen
- Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation

## 🔧 Technischer Aufbau

### Backend (Python/Flask)
- **Flask** - Webframework
- **BeautifulSoup** - HTML-Parsing
- **PyMuPDF** - PDF-Textextraktion
- **Sumy** - Textzusammenfassung
- **WeasyPrint** - PDF-Export

### Frontend
- **Bootstrap 5** - UI-Framework
- **Font Awesome** - Icons
- **Vanilla JavaScript** - Interaktivität

### Projektstruktur
```
luenen_terminplaner/
├── app.py                 # Haupt-Flask-Anwendung
├── scraper.py            # Webscraping-Logik
├── pdf_processor.py      # PDF-Verarbeitung und Zusammenfassung
├── export_manager.py     # Export-Funktionalität
├── requirements.txt      # Python-Abhängigkeiten
├── templates/
│   └── index.html       # Haupt-Webinterface
├── downloads/           # Heruntergeladene PDFs
└── exports/            # Exportierte Dateien
```

## 🔍 API-Endpunkte

- `GET /` - Haupt-Webinterface
- `POST /api/scrape` - Termine scrapen und verarbeiten
- `GET /api/export/<format>` - Daten exportieren

## 🔐 Datenschutz

- Keine Speicherung personenbezogener Daten
- Alle PDFs stammen aus öffentlich zugänglichen Quellen
- Lokale Verarbeitung ohne externe Dienste

## 🧪 Tests

Das Projekt enthält umfassende Tests für alle Komponenten:

### Test-Ausführung

```bash
# Alle Tests ausführen
python run_tests.py

# Nur Unit Tests
python run_tests.py --unit

# Nur Integration Tests  
python run_tests.py --integration

# Mit Coverage-Report
python run_tests.py --coverage

# Spezifische Test-Datei
python run_tests.py --file test_scraper.py

# Schnelle Tests (ohne langsame/Integration)
python run_tests.py --fast
```

### Test-Kategorien

- **Unit Tests**: Testen einzelne Funktionen isoliert
  - `test_pdf_processor.py` - PDF-Verarbeitung und Textzusammenfassung
  - `test_scraper.py` - Web-Scraping und HTML-Parsing
  - `test_export_manager.py` - Export-Funktionalität
  
- **Integration Tests**: Testen Zusammenspiel der Komponenten
  - `test_app.py` - Flask-App und API-Endpunkte
  - `test_integration.py` - End-to-End Workflows

### Coverage

```bash
# Coverage-Report generieren
python run_tests.py --coverage

# HTML-Report anzeigen
open htmlcov/index.html
```

## 🧪 Entwicklung

Für die Entwicklung können Sie folgende Befehle verwenden:

```bash
# Entwicklungsserver mit Debug-Modus
python app.py

# Tests ausführen
python run_tests.py

# Tests mit Coverage
python run_tests.py --coverage

# Code-Formatierung
black *.py
```

## 📝 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe LICENSE-Datei für Details.

## 🤝 Beiträge

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue.

## 📞 Support

Bei Fragen oder Problemen erstellen Sie bitte ein Issue im Repository.