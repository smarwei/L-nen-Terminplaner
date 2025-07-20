import pytest
import os
import json
import tempfile
import shutil
from datetime import datetime
from unittest.mock import patch, MagicMock
from export_manager import ExportManager


class TestExportManager:
    
    @pytest.fixture
    def export_manager(self):
        return ExportManager()
    
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_meetings(self):
        return [
            {
                'title': 'Rat der Stadt Lünen',
                'date': '15.03.2024',
                'time': '18:00',
                'location': 'Rathaus, Sitzungssaal',
                'committee': 'Rat der Stadt Lünen',
                'summary': 'Wichtige Beschlüsse zur Stadtentwicklung wurden gefasst.',
                'pdf_url': 'http://example.com/dokument1.pdf'
            },
            {
                'title': 'Rechnungsprüfungsausschuss',
                'date': '20.03.2024',
                'time': '17:30',
                'location': 'Verwaltungsgebäude',
                'committee': 'Rechnungsprüfungsausschuss',
                'summary': 'Jahresabschluss 2023 wurde geprüft.',
                'pdf_url': 'http://example.com/dokument2.pdf'
            }
        ]
    
    def test_init(self, export_manager):
        assert export_manager.export_folder == "exports"
        assert os.path.exists(export_manager.export_folder)
    
    @patch('export_manager.ExportManager._export_markdown')
    def test_export_markdown(self, mock_export_markdown, export_manager, sample_meetings):
        mock_export_markdown.return_value = '/path/to/file.md'
        
        result = export_manager.export(sample_meetings, 'markdown')
        
        mock_export_markdown.assert_called_once()
        assert result == '/path/to/file.md'
    
    @patch('export_manager.ExportManager._export_html')
    def test_export_html(self, mock_export_html, export_manager, sample_meetings):
        mock_export_html.return_value = '/path/to/file.html'
        
        result = export_manager.export(sample_meetings, 'html')
        
        mock_export_html.assert_called_once()
        assert result == '/path/to/file.html'
    
    @patch('export_manager.ExportManager._export_pdf')
    def test_export_pdf(self, mock_export_pdf, export_manager, sample_meetings):
        mock_export_pdf.return_value = '/path/to/file.pdf'
        
        result = export_manager.export(sample_meetings, 'pdf')
        
        mock_export_pdf.assert_called_once()
        assert result == '/path/to/file.pdf'
    
    @patch('export_manager.ExportManager._export_json')
    def test_export_json(self, mock_export_json, export_manager, sample_meetings):
        mock_export_json.return_value = '/path/to/file.json'
        
        result = export_manager.export(sample_meetings, 'json')
        
        mock_export_json.assert_called_once()
        assert result == '/path/to/file.json'
    
    def test_export_invalid_format(self, export_manager, sample_meetings):
        with pytest.raises(ValueError) as excinfo:
            export_manager.export(sample_meetings, 'invalid_format')
        
        assert "Unbekanntes Export-Format" in str(excinfo.value)
    
    def test_export_case_insensitive(self, export_manager, sample_meetings):
        with patch('export_manager.ExportManager._export_markdown') as mock_markdown:
            mock_markdown.return_value = '/path/to/file.md'
            
            result = export_manager.export(sample_meetings, 'MARKDOWN')
            mock_markdown.assert_called_once()
    
    def test_export_markdown_content(self, export_manager, sample_meetings, temp_dir):
        export_manager.export_folder = temp_dir
        
        filename = export_manager._export_markdown(sample_meetings, "20240315_120000")
        
        assert os.path.exists(filename)
        assert filename.endswith('.md')
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        assert "# Ratsinfo Lünen - Terminübersicht" in content
        assert "Rat der Stadt Lünen" in content
        assert "Rechnungsprüfungsausschuss" in content
        assert "Wichtige Beschlüsse" in content
        assert "Jahresabschluss 2023" in content
        assert "http://example.com/dokument1.pdf" in content
    
    def test_export_html_content(self, export_manager, sample_meetings, temp_dir):
        export_manager.export_folder = temp_dir
        
        filename = export_manager._export_html(sample_meetings, "20240315_120000")
        
        assert os.path.exists(filename)
        assert filename.endswith('.html')
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        assert "<!DOCTYPE html>" in content
        assert "Ratsinfo Lünen - Terminübersicht" in content
        assert "Rat der Stadt Lünen" in content
        assert "meeting-info" in content
        assert "summary" in content
    
    def test_export_json_content(self, export_manager, sample_meetings, temp_dir):
        export_manager.export_folder = temp_dir
        
        filename = export_manager._export_json(sample_meetings, "20240315_120000")
        
        assert os.path.exists(filename)
        assert filename.endswith('.json')
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert 'export_date' in data
        assert 'meetings' in data
        assert len(data['meetings']) == 2
        assert data['meetings'][0]['title'] == 'Rat der Stadt Lünen'
        assert data['meetings'][1]['title'] == 'Rechnungsprüfungsausschuss'
    
    @patch('export_manager.HTML')
    def test_export_pdf_generation(self, mock_html, export_manager, sample_meetings, temp_dir):
        export_manager.export_folder = temp_dir
        
        mock_html_instance = MagicMock()
        mock_html.return_value = mock_html_instance
        
        filename = export_manager._export_pdf(sample_meetings, "20240315_120000")
        
        assert filename.endswith('.pdf')
        mock_html.assert_called_once()
        mock_html_instance.write_pdf.assert_called_once()
    
    def test_generate_html_content(self, export_manager, sample_meetings):
        html_content = export_manager._generate_html_content(sample_meetings)
        
        assert "<!DOCTYPE html>" in html_content
        assert "Rat der Stadt Lünen" in html_content
        assert "Rechnungsprüfungsausschuss" in html_content
        assert "18:00" in html_content
        assert "17:30" in html_content
        assert "Wichtige Beschlüsse" in html_content
        assert "Jahresabschluss 2023" in html_content
        assert "http://example.com/dokument1.pdf" in html_content
    
    def test_generate_html_content_no_summary(self, export_manager):
        meetings_no_summary = [
            {
                'title': 'Test Meeting',
                'date': '15.03.2024',
                'time': '18:00',
                'location': 'Test Location',
                'committee': 'Test Committee',
                'summary': '',
                'pdf_url': ''
            }
        ]
        
        html_content = export_manager._generate_html_content(meetings_no_summary)
        
        assert "Test Meeting" in html_content
        assert "summary" not in html_content.lower() or "keine zusammenfassung" in html_content.lower()
    
    def test_generate_html_content_no_pdf(self, export_manager):
        meetings_no_pdf = [
            {
                'title': 'Test Meeting',
                'date': '15.03.2024',
                'time': '18:00',
                'location': 'Test Location',
                'committee': 'Test Committee',
                'summary': 'Test summary',
                'pdf_url': ''
            }
        ]
        
        html_content = export_manager._generate_html_content(meetings_no_pdf)
        
        assert "Test Meeting" in html_content
        assert 'href=""' not in html_content
    
    def test_markdown_export_special_characters(self, export_manager, temp_dir):
        export_manager.export_folder = temp_dir
        
        meetings_with_special_chars = [
            {
                'title': 'Meeting with Umlauts äöü',
                'date': '15.03.2024',
                'time': '18:00',
                'location': 'Café München',
                'committee': 'Sonderausschuss',
                'summary': 'Beschluss über Straße & Fußgängerzone',
                'pdf_url': 'http://example.com/test.pdf'
            }
        ]
        
        filename = export_manager._export_markdown(meetings_with_special_chars, "20240315_120000")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "äöü" in content
        assert "München" in content
        assert "Straße" in content
        assert "Fußgängerzone" in content
    
    def test_json_export_encoding(self, export_manager, temp_dir):
        export_manager.export_folder = temp_dir
        
        meetings_with_unicode = [
            {
                'title': 'Unicode Test äöüß',
                'date': '15.03.2024',
                'time': '18:00',
                'location': 'Test Location',
                'committee': 'Test Committee',
                'summary': 'Test with special chars: €£¥',
                'pdf_url': 'http://example.com/test.pdf'
            }
        ]
        
        filename = export_manager._export_json(meetings_with_unicode, "20240315_120000")
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data['meetings'][0]['title'] == 'Unicode Test äöüß'
        assert '€£¥' in data['meetings'][0]['summary']