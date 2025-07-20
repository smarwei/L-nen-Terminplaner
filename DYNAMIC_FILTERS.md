# Dynamisches Gremien-Filter-System

## 🎯 Problem gelöst

**Vorher**: Filter waren hardcoded in der Spezifikation  
**Nachher**: Alle verfügbaren Gremien werden dynamisch geladen und angezeigt

## ✅ Neue Features

### 1. **Dynamische Committee-Erkennung**
- **API-Endpoint**: `/api/committees`
- **Funktionalität**: Scannt aktuelle und kommende Meetings, um alle verfügbaren Gremien zu finden
- **Performance**: Optimiert durch Beschränkung auf relevante Zeiträume
- **Fallback**: Relevante Gremien aus Spezifikation werden immer angezeigt

### 2. **Intelligente Vorauswahl**
- **Relevante Gremien**: Automatisch vorselektiert (aus `scraper.relevant_committees`)
- **Badge-System**: "Relevant"-Badge für wichtige Gremien
- **Flexibilität**: Benutzer kann Auswahl beliebig anpassen

### 3. **Komfort-Features**
- **"Alle" Button**: Wählt alle verfügbaren Gremien aus
- **"Relevante" Button**: Setzt die Auswahl auf Spezifikations-Standard zurück
- **"Keine" Button**: Deselektiert alle Gremien
- **Scrollbare Liste**: Bei vielen Gremien scrollbar (max-height: 200px)

### 4. **Verbesserte Benutzerführung**
- **Validierung**: Warnung wenn keine Gremien ausgewählt
- **Visuelle Kennzeichnung**: Relevante Gremien mit blauem Badge
- **Responsive Design**: Funktioniert auf allen Geräten

## 🔧 Technische Implementierung

### Backend (app.py)
```python
@app.route('/api/committees')
def get_committees():
    # Lade Meetings der letzten Monate + Zukunft
    all_meetings = scraper.scrape_meetings(start_date, end_date)
    
    # Extrahiere einzigartige Committee-Namen
    committees = set(meeting.get('committee') for meeting in all_meetings)
    
    # Füge immer relevante Committees hinzu
    for committee in scraper.relevant_committees:
        committees.add(committee)
    
    return {
        'committees': sorted(committees),
        'relevant_committees': scraper.relevant_committees
    }

@app.route('/api/scrape', methods=['POST'])
def scrape_data():
    selected_committees = data.get('committees', [])
    
    # Filtere Meetings nach ausgewählten Committees
    if selected_committees:
        meetings = [m for m in meetings if m.get('committee') in selected_committees]
```

### Frontend (templates/index.html)
```javascript
// Lade verfügbare Committees beim Seitenstart
document.addEventListener('DOMContentLoaded', async () => {
    await loadCommittees();
});

async function loadCommittees() {
    const response = await fetch('/api/committees');
    const data = await response.json();
    
    availableCommittees = data.committees;
    relevantCommittees = data.relevant_committees;
    renderCommitteeFilters();
}

function renderCommitteeFilters() {
    // Erstelle Checkbox für jedes Committee
    // Markiere relevante mit Badge und vorselektiert
}

// Komfort-Funktionen
function selectAllCommittees() { /* ... */ }
function selectRelevantCommittees() { /* ... */ }
function clearAllCommittees() { /* ... */ }
```

### UI-Komponenten
```html
<div class="mb-3">
    <label class="form-label">
        <i class="fas fa-filter me-2"></i>
        Gremien-Filter
    </label>
    
    <!-- Quick-Action Buttons -->
    <div class="d-flex justify-content-between">
        <span>Relevante Gremien sind vorausgewählt...</span>
        <div>
            <button onclick="selectAllCommittees()">Alle</button>
            <button onclick="selectRelevantCommittees()">Relevante</button>
            <button onclick="clearAllCommittees()">Keine</button>
        </div>
    </div>
    
    <!-- Scrollbare Committee-Liste -->
    <div id="committeeFilters" style="max-height: 200px; overflow-y: auto;">
        <!-- Dynamisch generierte Checkboxen -->
    </div>
</div>
```

## 📊 Vorteile

### Für Entwickler:
- **Keine hardcoded Listen**: Filter passen sich automatisch an
- **Wartungsfreundlich**: Neue Gremien werden automatisch erkannt
- **Skalierbar**: Funktioniert mit beliebig vielen Committees

### Für Benutzer:
- **Vollständige Kontrolle**: Können jeden verfügbaren Filter wählen
- **Einfache Bedienung**: Komfort-Buttons für häufige Aktionen
- **Transparenz**: Sehen alle verfügbaren Optionen
- **Flexibilität**: Können auch "exotische" Committees erforschen

### Für das System:
- **Bessere Datenqualität**: Findet auch Meetings, die vorher übersehen wurden
- **Zukunftssicher**: Neue Gremien werden automatisch integriert
- **Performance**: Optimierte API-Calls nur für relevante Zeiträume

## 🎯 Anwendungsfälle

### Standard-Nutzer:
1. Seite laden → Relevante Gremien sind bereits ausgewählt
2. Termine laden → Bekommt die wichtigsten Meetings

### Power-User:
1. "Alle" klicken → Sieht alle verfügbaren Gremien
2. Spezifische Auswahl treffen → Kann gezielt nach bestimmten Committees suchen
3. Termine laden → Bekommt maßgeschneiderte Ergebnisse

### Forscher/Journalisten:
1. Können alle Gremien durchsuchen
2. Entdecken möglicherweise interessante, weniger bekannte Committees
3. Vollständige Transparenz über alle verfügbaren Daten

**Das System ist jetzt vollständig flexibel und nutzerfreundlich!**