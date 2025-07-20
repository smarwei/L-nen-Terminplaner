## 🧾 Projektname

**Lünen Ratsinfo-Scraper mit PDF-Zusammenfassung**

---

## 🎯 Ziel

Ein Programm zur automatisierten Extraktion, Filterung und Zusammenfassung von Ratsinformationen aus dem Online-Informationssystem der Stadt Lünen. Es soll Benutzern ermöglichen, Sitzungsdokumente in einem definierten Zeitraum herunterzuladen, zu parsen und deren Inhalte übersichtlich zusammenzufassen.

---

## 🖥️ Zielplattform

* **Option A:** Desktop-GUI mit **Qt (PySide6 oder PyQt5)**
* **Option B:** Lokale **Webanwendung** (Browser-basiert, z. B. mit Flask + Vue/React)

---

## 🔍 Datenquelle

**URL:** [https://luenen.ratsinfomanagement.net/termine/](https://luenen.rats.infomanagement.net/termine/)

---

## 📅 Relevante Filter / Gremien

Nur die folgenden Gremien sind relevant:

* Rat der Stadt Lünen
* Rechnungsprüfungsausschuss
* Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen
* Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation

---

## 📌 Funktionsumfang

### 1. Datumsbasierte Abfrage

* Eingabe per:

  * Zwei **DatePicker** (Startdatum, Enddatum)
  * Alternativ: Auswahl eines konkreten Monats
* Ausgabe: Alle Termine innerhalb dieses Bereichs

---

### 2. Webscraping

* Scraping der Sitzungsübersicht mit Filterung nach oben genannten Gremien
* Für jeden relevanten Termin:

  * **Titel**
  * **Datum/Uhrzeit**
  * **Ort**
  * **Link zur Detailseite**
  * **Link zum PDF (Sitzungsvorlage/-protokoll)**

---

### 3. PDF-Verarbeitung

* Herunterladen der verlinkten PDF-Dateien
* **Priorisierung von "Gesamtes Sitzungspaket" PDFs** für vollständige Dokumentation
* Extraktion von Text mit mehreren Bibliotheken (PyMuPDF, pdfplumber als Fallback)
* Optional: OCR (für gescannte PDFs, z. B. mit Tesseract)
* **Zusammenfassung des Inhalts** (automatisch per NLP, z. B. mit `sumy`, `transformers`, `llm`…)

---

### 4. Darstellung der Ergebnisse

* Übersichtsseite für alle Termine mit:

  * Zusammenfassungen (optional ein-/ausklappbar)
  * Originaltitel, Link zum PDF
  * Exportmöglichkeit als Markdown, HTML oder PDF
* Sortier- und Filtermöglichkeiten nach Gremium oder Datum

---

## ⚙️ Technologiestack (Vorschlag)

| Komponente             | Technologie                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| Webscraping            | `requests`, `BeautifulSoup` oder `playwright` (wenn JS nötig)           |
| PDF-Verarbeitung       | `PyMuPDF`, `pdfminer.six`, ggf. `pytesseract`                           |
| NLP-Zusammenfassung    | `transformers` (z. B. `bert`, `t5-small`, `mistral`), alternativ `sumy` |
| GUI                    | Qt (PySide6) oder lokale Webapp (Flask + Vue.js)                        |
| Speicherung (optional) | SQLite oder lokale JSON-Dateien                                         |

---

## 🔐 Datenschutz und rechtliche Hinweise

* Keine personenbezogenen Daten speichern
* Alle PDFs stammen aus öffentlich zugänglichen Quellen der Stadt Lünen

---

## 📝 Implementierte Verbesserungen

* **Duplikatentfernung**: Automatische Entfernung von doppelten Terminen basierend auf Datum, Uhrzeit und Gremium
* **PDF-Priorisierung**: Bevorzugung von "Gesamtes Sitzungspaket" PDFs für vollständige Dokumentation
* **Erweiterte Ausschusserkennung**: Verbesserte Patterns für Betriebsausschuss Zentrale Gebäudebewirtschaftung und andere Ausschüsse
* **Robuste Fallback-Systeme**: Mehrere PDF-Verarbeitungsbibliotheken und Web-Scraping-Methoden
* **Detailseiten**: Separate Seiten für jedes Meeting mit ausführlichen Zusammenfassungen
* **Mehrstufige Zusammenfassung**: Kurze Übersicht + ausführliche Detailansicht
* **Verbesserte Navigation**: Direkte Links zwischen Übersicht und Detailseiten
* **Dynamische Gremien-Filter**: Alle verfügbaren Gremien werden angezeigt, relevante vorselektiert
* **Flexible Committee-Auswahl**: Benutzer können beliebige Kombinationen von Gremien auswählen
* **Smart Filter-Buttons**: "Alle", "Relevante", "Keine" für schnelle Auswahl

---

## 🧪 Erweiterungen (später möglich)

* Keyword-Suche über alle zusammengefassten Dokumente
* Mail-Benachrichtigung bei neuen Sitzungen
* Analyse von Abstimmungsergebnissen oder Trends
