# Lünen Terminplaner - Windows Distribution

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
