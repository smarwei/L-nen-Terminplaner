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
* Extraktion von Text
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

## 🧪 Erweiterungen (später möglich)

* Keyword-Suche über alle zusammengefassten Dokumente
* Mail-Benachrichtigung bei neuen Sitzungen
* Analyse von Abstimmungsergebnissen oder Trends
