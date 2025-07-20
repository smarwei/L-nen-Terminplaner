import json
import os
from datetime import datetime
from pathlib import Path

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False
    print("Warning: Markdown not available")

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print(f"Warning: WeasyPrint not available ({e}). PDF export will be limited.")

class ExportManager:
    def __init__(self):
        self.export_folder = "exports"
        if not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder)
    
    def export(self, meetings, format_type):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type.lower() == 'markdown':
            return self._export_markdown(meetings, timestamp)
        elif format_type.lower() == 'html':
            return self._export_html(meetings, timestamp)
        elif format_type.lower() == 'pdf':
            return self._export_pdf(meetings, timestamp)
        elif format_type.lower() == 'json':
            return self._export_json(meetings, timestamp)
        else:
            raise ValueError(f"Unbekanntes Export-Format: {format_type}")
    
    def _export_markdown(self, meetings, timestamp):
        filename = os.path.join(self.export_folder, f"ratsinfo_export_{timestamp}.md")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Ratsinfo Lünen - Terminübersicht\n\n")
            f.write(f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")
            f.write("---\n\n")
            
            for meeting in meetings:
                f.write(f"## {meeting['title']}\n\n")
                f.write(f"**Datum:** {meeting['date']}\n")
                f.write(f"**Uhrzeit:** {meeting['time']}\n")
                f.write(f"**Ort:** {meeting['location']}\n")
                f.write(f"**Gremium:** {meeting['committee']}\n\n")
                
                if meeting.get('summary'):
                    f.write("### Zusammenfassung\n\n")
                    f.write(f"{meeting['summary']}\n\n")
                
                if meeting.get('pdf_url'):
                    f.write(f"**PDF-Dokument:** [Link zum Dokument]({meeting['pdf_url']})\n\n")
                
                f.write("---\n\n")
        
        return filename
    
    def _export_html(self, meetings, timestamp):
        filename = os.path.join(self.export_folder, f"ratsinfo_export_{timestamp}.html")
        
        html_content = self._generate_html_content(meetings)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
    
    def _export_pdf(self, meetings, timestamp):
        filename = os.path.join(self.export_folder, f"ratsinfo_export_{timestamp}.pdf")
        
        if not WEASYPRINT_AVAILABLE:
            # Fallback: create HTML file instead
            html_filename = os.path.join(self.export_folder, f"ratsinfo_export_{timestamp}_fallback.html")
            html_content = self._generate_html_content(meetings)
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return html_filename
        
        html_content = self._generate_html_content(meetings)
        
        css = CSS(string='''
            @page {
                margin: 2cm;
                @top-center {
                    content: "Ratsinfo Lünen - Terminübersicht";
                }
            }
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #34495e;
                margin-top: 30px;
                border-left: 4px solid #3498db;
                padding-left: 15px;
            }
            .meeting-info {
                background-color: #f8f9fa;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                border-left: 4px solid #28a745;
            }
            .summary {
                background-color: #fff3cd;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                border-left: 4px solid #ffc107;
            }
        ''')
        
        HTML(string=html_content).write_pdf(filename, stylesheets=[css])
        
        return filename
    
    def _export_json(self, meetings, timestamp):
        filename = os.path.join(self.export_folder, f"ratsinfo_export_{timestamp}.json")
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'meetings': meetings
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def _generate_html_content(self, meetings):
        html = """
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ratsinfo Lünen - Terminübersicht</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                h1 {
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }
                h2 {
                    color: #34495e;
                    margin-top: 30px;
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                }
                .meeting-info {
                    background-color: #f8f9fa;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                    border-left: 4px solid #28a745;
                }
                .summary {
                    background-color: #fff3cd;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                    border-left: 4px solid #ffc107;
                }
                .pdf-link {
                    color: #007bff;
                    text-decoration: none;
                }
                .pdf-link:hover {
                    text-decoration: underline;
                }
                .timestamp {
                    color: #6c757d;
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            <h1>Ratsinfo Lünen - Terminübersicht</h1>
            <p class="timestamp">Erstellt am: """ + datetime.now().strftime('%d.%m.%Y %H:%M') + """</p>
            <hr>
        """
        
        for meeting in meetings:
            html += f"""
            <h2>{meeting['title']}</h2>
            <div class="meeting-info">
                <strong>Datum:</strong> {meeting['date']}<br>
                <strong>Uhrzeit:</strong> {meeting['time']}<br>
                <strong>Ort:</strong> {meeting['location']}<br>
                <strong>Gremium:</strong> {meeting['committee']}
            </div>
            """
            
            if meeting.get('summary'):
                html += f"""
                <div class="summary">
                    <h3>Zusammenfassung</h3>
                    <p>{meeting['summary']}</p>
                </div>
                """
            
            if meeting.get('pdf_url'):
                html += f"""
                <p><strong>PDF-Dokument:</strong> <a href="{meeting['pdf_url']}" class="pdf-link" target="_blank">Link zum Dokument</a></p>
                """
            
            html += "<hr>"
        
        html += """
        </body>
        </html>
        """
        
        return html