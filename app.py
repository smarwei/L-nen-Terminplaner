from flask import Flask, render_template, request, jsonify, send_file, url_for
from datetime import datetime, timedelta
import os
import json
from scraper import RatsInfoScraper
from pdf_processor import PDFProcessor
from export_manager import ExportManager

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['SECRET_KEY'] = 'luenen-terminplaner-2024'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

scraper = RatsInfoScraper()
pdf_processor = PDFProcessor()
export_manager = ExportManager()

# Store for meeting details (in production, use a database)
meeting_cache = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/meeting/<meeting_id>')
def meeting_detail(meeting_id):
    """Detailseite für ein Meeting mit ausführlicher Zusammenfassung"""
    meeting = meeting_cache.get(meeting_id)
    if not meeting:
        return "Meeting nicht gefunden", 404
    
    return render_template('meeting_detail.html', meeting=meeting)

@app.route('/api/scrape', methods=['POST'])
def scrape_data():
    data = request.get_json()
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    selected_committees = data.get('committees', [])
    
    try:
        meetings = scraper.scrape_meetings(start_date, end_date)
        
        # Filter meetings by selected committees (if any specified)
        if selected_committees:
            filtered_meetings = []
            for meeting in meetings:
                if meeting.get('committee') in selected_committees:
                    filtered_meetings.append(meeting)
            meetings = filtered_meetings
        
        processed_meetings = []
        
        for i, meeting in enumerate(meetings):
            # Generate unique meeting ID (safe for URLs)
            import re
            safe_committee = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß]', '-', meeting['committee'][:30])
            safe_committee = re.sub(r'-+', '-', safe_committee).strip('-')
            meeting_id = f"{meeting['date'].replace('.', '')}-{safe_committee}-{i}"
            
            processed_meeting = {
                'id': meeting_id,
                'title': meeting['title'],
                'date': meeting['date'],
                'time': meeting['time'],
                'location': meeting['location'],
                'committee': meeting['committee'],
                'detail_url': meeting['detail_url'],
                'pdf_url': meeting.get('pdf_url', ''),
                'summary': '',
                'detail_page_url': url_for('meeting_detail', meeting_id=meeting_id)
            }
            
            # Process PDF for both short and detailed summary
            full_text = ""
            if meeting.get('pdf_url'):
                try:
                    pdf_path = pdf_processor.download_pdf(meeting['pdf_url'], app.config['UPLOAD_FOLDER'])
                    full_text = pdf_processor.extract_text(pdf_path)
                    
                    # Short summary for overview
                    short_summary = pdf_processor.summarize_text(full_text, sentence_count=2)
                    processed_meeting['summary'] = short_summary
                    
                    # Detailed summary for detail page
                    detailed_summary = pdf_processor.summarize_text(full_text, sentence_count=5)
                    processed_meeting['detailed_summary'] = detailed_summary
                    processed_meeting['full_text'] = full_text[:2000] + "..." if len(full_text) > 2000 else full_text
                    
                except Exception as e:
                    processed_meeting['summary'] = f"Fehler beim Verarbeiten der PDF: {str(e)}"
                    processed_meeting['detailed_summary'] = processed_meeting['summary']
                    processed_meeting['full_text'] = ""
            
            # Store in cache for detail page
            meeting_cache[meeting_id] = processed_meeting
            
            processed_meetings.append(processed_meeting)
        
        return jsonify({'success': True, 'meetings': processed_meetings})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/committees')
def get_committees():
    """Get all available committees for filtering"""
    try:
        # Get committees from a few recent months to find available committees
        # This is faster than scanning the whole year
        current_date = datetime.now()
        start_date = datetime(current_date.year, max(1, current_date.month - 3), 1)
        end_date = datetime(current_date.year + 1, 12, 31)
        
        all_meetings = scraper.scrape_meetings(start_date, end_date)
        
        # Extract unique committees
        committees = set()
        for meeting in all_meetings:
            committee = meeting.get('committee', '').strip()
            if committee:
                committees.add(committee)
        
        # Always include the relevant committees from configuration
        relevant_committees = scraper.relevant_committees
        for committee in relevant_committees:
            committees.add(committee)
        
        # Sort committees alphabetically
        sorted_committees = sorted(list(committees))
        
        return jsonify({
            'success': True, 
            'committees': sorted_committees,
            'relevant_committees': relevant_committees
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/export/<format>')
def export_data(format):
    meetings_data = request.args.get('data')
    if not meetings_data:
        return jsonify({'error': 'Keine Daten zum Exportieren'}), 400
    
    try:
        meetings = json.loads(meetings_data)
        filename = export_manager.export(meetings, format)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)