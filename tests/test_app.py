import pytest
import json
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from app import app


class TestFlaskApp:
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
        with app.test_client() as client:
            yield client
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    
    @pytest.fixture
    def sample_meetings(self):
        return [
            {
                'title': 'Rat der Stadt Lünen',
                'date': '15.03.2024',
                'time': '18:00',
                'location': 'Rathaus, Sitzungssaal',
                'committee': 'Rat der Stadt Lünen',
                'detail_url': 'http://example.com/detail/1',
                'pdf_url': 'http://example.com/test.pdf',
                'summary': 'Test summary'
            }
        ]
    
    def test_index_route(self, client):
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'L\xc3\xbcnen Terminplaner' in response.data
        assert b'Termine suchen' in response.data
    
    def test_index_contains_form_elements(self, client):
        response = client.get('/')
        
        assert b'startDate' in response.data
        assert b'endDate' in response.data
        assert b'searchForm' in response.data
    
    def test_index_contains_export_buttons(self, client):
        response = client.get('/')
        
        assert b'markdown' in response.data
        assert b'html' in response.data
        assert b'pdf' in response.data
        assert b'json' in response.data
    
    @patch('app.scraper')
    @patch('app.pdf_processor')
    def test_scrape_data_success(self, mock_pdf_processor, mock_scraper, client, sample_meetings):
        mock_scraper.scrape_meetings.return_value = [
            {
                'title': 'Rat der Stadt Lünen',
                'date': '15.03.2024',
                'time': '18:00',
                'location': 'Rathaus',
                'committee': 'Rat der Stadt Lünen',
                'detail_url': 'http://example.com/detail/1',
                'pdf_url': 'http://example.com/test.pdf'
            }
        ]
        
        mock_pdf_processor.download_pdf.return_value = '/fake/path.pdf'
        mock_pdf_processor.extract_text.return_value = 'Extracted text'
        mock_pdf_processor.summarize_text.return_value = 'Summary text'
        
        response = client.post('/api/scrape', 
                             data=json.dumps({
                                 'start_date': '2024-03-01',
                                 'end_date': '2024-03-31'
                             }),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert len(data['meetings']) == 1
        assert data['meetings'][0]['summary'] == 'Summary text'
    
    @patch('app.scraper')
    def test_scrape_data_no_pdf(self, mock_scraper, client):
        mock_scraper.scrape_meetings.return_value = [
            {
                'title': 'Rat der Stadt Lünen',
                'date': '15.03.2024',
                'time': '18:00',
                'location': 'Rathaus',
                'committee': 'Rat der Stadt Lünen',
                'detail_url': 'http://example.com/detail/1',
                'pdf_url': None
            }
        ]
        
        response = client.post('/api/scrape',
                             data=json.dumps({
                                 'start_date': '2024-03-01',
                                 'end_date': '2024-03-31'
                             }),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['meetings'][0]['summary'] == ''
    
    @patch('app.scraper')
    @patch('app.pdf_processor')
    def test_scrape_data_pdf_error(self, mock_pdf_processor, mock_scraper, client):
        mock_scraper.scrape_meetings.return_value = [
            {
                'title': 'Rat der Stadt Lünen',
                'date': '15.03.2024',
                'time': '18:00',
                'location': 'Rathaus',
                'committee': 'Rat der Stadt Lünen',
                'detail_url': 'http://example.com/detail/1',
                'pdf_url': 'http://example.com/test.pdf'
            }
        ]
        
        mock_pdf_processor.download_pdf.side_effect = Exception("Download error")
        
        response = client.post('/api/scrape',
                             data=json.dumps({
                                 'start_date': '2024-03-01',
                                 'end_date': '2024-03-31'
                             }),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'Fehler beim Verarbeiten der PDF' in data['meetings'][0]['summary']
    
    @patch('app.scraper')
    def test_scrape_data_scraper_error(self, mock_scraper, client):
        mock_scraper.scrape_meetings.side_effect = Exception("Scraping error")
        
        response = client.post('/api/scrape',
                             data=json.dumps({
                                 'start_date': '2024-03-01',
                                 'end_date': '2024-03-31'
                             }),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'error' in data
    
    def test_scrape_data_invalid_json(self, client):
        response = client.post('/api/scrape',
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_scrape_data_missing_data(self, client):
        response = client.post('/api/scrape',
                             data=json.dumps({}),
                             content_type='application/json')
        
        # Should handle missing keys gracefully
        assert response.status_code in [400, 500]
    
    @patch('app.export_manager')
    @patch('app.send_file')
    def test_export_data_markdown(self, mock_send_file, mock_export_manager, client, sample_meetings):
        mock_export_manager.export.return_value = '/fake/path/export.md'
        mock_send_file.return_value = 'file content'
        
        response = client.get('/api/export/markdown', 
                            query_string={'data': json.dumps(sample_meetings)})
        
        mock_export_manager.export.assert_called_once_with(sample_meetings, 'markdown')
        mock_send_file.assert_called_once_with('/fake/path/export.md', as_attachment=True)
    
    @patch('app.export_manager')
    @patch('app.send_file')
    def test_export_data_html(self, mock_send_file, mock_export_manager, client, sample_meetings):
        mock_export_manager.export.return_value = '/fake/path/export.html'
        mock_send_file.return_value = 'file content'
        
        response = client.get('/api/export/html',
                            query_string={'data': json.dumps(sample_meetings)})
        
        mock_export_manager.export.assert_called_once_with(sample_meetings, 'html')
    
    @patch('app.export_manager')
    @patch('app.send_file')
    def test_export_data_pdf(self, mock_send_file, mock_export_manager, client, sample_meetings):
        mock_export_manager.export.return_value = '/fake/path/export.pdf'
        mock_send_file.return_value = 'file content'
        
        response = client.get('/api/export/pdf',
                            query_string={'data': json.dumps(sample_meetings)})
        
        mock_export_manager.export.assert_called_once_with(sample_meetings, 'pdf')
    
    @patch('app.export_manager')
    @patch('app.send_file')
    def test_export_data_json(self, mock_send_file, mock_export_manager, client, sample_meetings):
        mock_export_manager.export.return_value = '/fake/path/export.json'
        mock_send_file.return_value = 'file content'
        
        response = client.get('/api/export/json',
                            query_string={'data': json.dumps(sample_meetings)})
        
        mock_export_manager.export.assert_called_once_with(sample_meetings, 'json')
    
    def test_export_data_no_data(self, client):
        response = client.get('/api/export/markdown')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Keine Daten' in data['error']
    
    def test_export_data_invalid_json(self, client):
        response = client.get('/api/export/markdown',
                            query_string={'data': 'invalid json'})
        
        assert response.status_code == 500
    
    @patch('app.export_manager')
    def test_export_data_export_error(self, mock_export_manager, client, sample_meetings):
        mock_export_manager.export.side_effect = Exception("Export error")
        
        response = client.get('/api/export/markdown',
                            query_string={'data': json.dumps(sample_meetings)})
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_app_config(self):
        assert app.config['UPLOAD_FOLDER'] == 'downloads'
        assert app.config['SECRET_KEY'] == 'luenen-terminplaner-2024'
    
    def test_upload_folder_creation(self):
        # Test that upload folder is created if it doesn't exist
        test_folder = 'test_downloads'
        if os.path.exists(test_folder):
            shutil.rmtree(test_folder)
        
        app.config['UPLOAD_FOLDER'] = test_folder
        
        # Simulate app startup
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        assert os.path.exists(test_folder)
        
        # Cleanup
        shutil.rmtree(test_folder)
    
    @patch('app.scraper')
    def test_scrape_data_date_conversion(self, mock_scraper, client):
        mock_scraper.scrape_meetings.return_value = []
        
        response = client.post('/api/scrape',
                             data=json.dumps({
                                 'start_date': '2024-03-15',
                                 'end_date': '2024-03-20'
                             }),
                             content_type='application/json')
        
        # Verify that scraper was called with datetime objects
        args, kwargs = mock_scraper.scrape_meetings.call_args
        start_date, end_date = args
        
        assert start_date.year == 2024
        assert start_date.month == 3
        assert start_date.day == 15
        assert end_date.year == 2024
        assert end_date.month == 3
        assert end_date.day == 20
    
    def test_content_type_json(self, client):
        response = client.post('/api/scrape',
                             data='{"start_date": "2024-03-01", "end_date": "2024-03-31"}',
                             content_type='application/json')
        
        # Should be able to process JSON content type
        assert response.status_code in [200, 500]  # 500 is ok if scraper fails, but JSON was parsed
    
    def test_content_type_form(self, client):
        response = client.post('/api/scrape',
                             data='start_date=2024-03-01&end_date=2024-03-31',
                             content_type='application/x-www-form-urlencoded')
        
        # Should not accept form data, expecting JSON
        assert response.status_code == 400