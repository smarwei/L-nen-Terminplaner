import pytest
import os
import tempfile
import shutil
from datetime import datetime
from unittest.mock import patch, MagicMock
import responses
from scraper import RatsInfoScraper
from pdf_processor import PDFProcessor
from export_manager import ExportManager


@pytest.mark.integration
class TestIntegration:
    
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_html_response(self):
        return """
        <html>
        <body>
            <table>
                <tr class="table-row-odd">
                    <td>15.03.2024</td>
                    <td>18:00</td>
                    <td><a href="/detail/12345">Rat der Stadt Lünen</a></td>
                    <td>Rathaus, Sitzungssaal</td>
                </tr>
                <tr class="table-row-even">
                    <td>20.03.2024</td>
                    <td>17:30</td>
                    <td><a href="/detail/12346">Irrelevanter Ausschuss</a></td>
                    <td>Verwaltungsgebäude</td>
                </tr>
            </table>
        </body>
        </html>
        """
    
    @pytest.fixture
    def sample_detail_response(self):
        return """
        <html>
        <body>
            <div>
                <a href="/documents/einladung.pdf">Einladung zur Sitzung</a>
                <a href="/documents/tagesordnung.pdf">Tagesordnung</a>
            </div>
        </body>
        </html>
        """
    
    @responses.activate
    def test_scraper_to_pdf_processor_integration(self, temp_dir, sample_html_response, sample_detail_response):
        # Setup mock responses
        responses.add(
            responses.GET,
            "https://luenen.ratsinfomanagement.net/termine/",
            body=sample_html_response,
            status=200
        )
        
        responses.add(
            responses.GET,
            "https://luenen.ratsinfomanagement.net/detail/12345",
            body=sample_detail_response,
            status=200
        )
        
        # Mock PDF download
        pdf_content = b"%PDF-1.4\nTest PDF content\n%%EOF"
        responses.add(
            responses.GET,
            "https://luenen.ratsinfomanagement.net/documents/einladung.pdf",
            body=pdf_content,
            status=200
        )
        
        scraper = RatsInfoScraper()
        pdf_processor = PDFProcessor()
        
        # Test scraping
        start_date = datetime(2024, 3, 1)
        end_date = datetime(2024, 3, 31)
        
        with patch.object(scraper, '_scrape_month') as mock_scrape:
            mock_scrape.return_value = [
                {
                    'date': '15.03.2024',
                    'time': '18:00',
                    'committee': 'Rat der Stadt Lünen',
                    'title': 'Rat der Stadt Lünen',
                    'location': 'Rathaus',
                    'detail_url': 'https://luenen.ratsinfomanagement.net/detail/12345'
                }
            ]
            
            meetings = scraper.scrape_meetings(start_date, end_date)
        
        assert len(meetings) == 1
        assert meetings[0]['committee'] == 'Rat der Stadt Lünen'
        
        # Test PDF processing integration
        if meetings[0].get('pdf_url'):
            pdf_path = pdf_processor.download_pdf(meetings[0]['pdf_url'], temp_dir)
            assert pdf_path is not None
            assert os.path.exists(pdf_path)
    
    @patch('pdf_processor.fitz.open')
    def test_pdf_processor_to_export_integration(self, mock_fitz, temp_dir):
        # Mock PDF text extraction
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Dies ist ein wichtiger Beschluss der Stadtverwaltung. Der Rat hat über wichtige Angelegenheiten entschieden."
        mock_doc.page_count = 1
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz.return_value = mock_doc
        
        pdf_processor = PDFProcessor()
        export_manager = ExportManager()
        export_manager.export_folder = temp_dir
        
        # Test text extraction and summarization
        text = pdf_processor.extract_text("/fake/path.pdf")
        assert len(text) > 0
        
        summary = pdf_processor.summarize_text(text)
        assert len(summary) > 0
        
        # Create meeting data with summary
        meetings = [
            {
                'title': 'Rat der Stadt Lünen',
                'date': '15.03.2024',
                'time': '18:00',
                'location': 'Rathaus',
                'committee': 'Rat der Stadt Lünen',
                'summary': summary,
                'pdf_url': 'http://example.com/test.pdf'
            }
        ]
        
        # Test export integration
        markdown_file = export_manager._export_markdown(meetings, "test")
        assert os.path.exists(markdown_file)
        
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Rat der Stadt Lünen' in content
            assert summary in content
    
    def test_full_workflow_integration(self, temp_dir):
        scraper = RatsInfoScraper()
        pdf_processor = PDFProcessor()
        export_manager = ExportManager()
        export_manager.export_folder = temp_dir
        
        # Mock the entire workflow
        with patch.object(scraper, 'scrape_meetings') as mock_scrape, \
             patch.object(pdf_processor, 'download_pdf') as mock_download, \
             patch.object(pdf_processor, 'extract_text') as mock_extract, \
             patch.object(pdf_processor, 'summarize_text') as mock_summarize:
            
            # Setup mocks
            mock_scrape.return_value = [
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
            
            mock_download.return_value = '/fake/path.pdf'
            mock_extract.return_value = 'Extracted PDF text content'
            mock_summarize.return_value = 'This is a summary of the meeting'
            
            # Simulate the workflow
            start_date = datetime(2024, 3, 1)
            end_date = datetime(2024, 3, 31)
            
            # 1. Scrape meetings
            meetings = scraper.scrape_meetings(start_date, end_date)
            
            # 2. Process PDFs and create summaries
            processed_meetings = []
            for meeting in meetings:
                processed_meeting = meeting.copy()
                
                if meeting.get('pdf_url'):
                    pdf_path = pdf_processor.download_pdf(meeting['pdf_url'], temp_dir)
                    text = pdf_processor.extract_text(pdf_path)
                    summary = pdf_processor.summarize_text(text)
                    processed_meeting['summary'] = summary
                
                processed_meetings.append(processed_meeting)
            
            # 3. Export results
            markdown_file = export_manager.export(processed_meetings, 'markdown')
            html_file = export_manager.export(processed_meetings, 'html')
            
            # Verify the workflow
            assert len(processed_meetings) == 1
            assert processed_meetings[0]['summary'] == 'This is a summary of the meeting'
            assert os.path.exists(markdown_file)
            assert os.path.exists(html_file)
            
            # Verify export content
            with open(markdown_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
                assert 'Rat der Stadt Lünen' in md_content
                assert 'This is a summary of the meeting' in md_content
    
    def test_error_handling_integration(self, temp_dir):
        scraper = RatsInfoScraper()
        pdf_processor = PDFProcessor()
        export_manager = ExportManager()
        export_manager.export_folder = temp_dir
        
        # Test workflow with various error conditions
        with patch.object(scraper, 'scrape_meetings') as mock_scrape, \
             patch.object(pdf_processor, 'download_pdf') as mock_download, \
             patch.object(pdf_processor, 'extract_text') as mock_extract:
            
            mock_scrape.return_value = [
                {
                    'title': 'Test Meeting',
                    'date': '15.03.2024',
                    'time': '18:00',
                    'location': 'Test Location',
                    'committee': 'Rat der Stadt Lünen',
                    'detail_url': 'http://example.com/detail/1',
                    'pdf_url': 'http://example.com/test.pdf'
                }
            ]
            
            # Simulate PDF download failure
            mock_download.return_value = None
            mock_extract.return_value = ""
            
            meetings = scraper.scrape_meetings(datetime(2024, 3, 1), datetime(2024, 3, 31))
            
            processed_meetings = []
            for meeting in meetings:
                processed_meeting = meeting.copy()
                processed_meeting['summary'] = 'PDF processing failed'
                processed_meetings.append(processed_meeting)
            
            # Should still be able to export even with failed PDF processing
            markdown_file = export_manager.export(processed_meetings, 'markdown')
            assert os.path.exists(markdown_file)
    
    def test_committee_filtering_integration(self, temp_dir):
        scraper = RatsInfoScraper()
        
        # Test that committee filtering works end-to-end
        with patch.object(scraper, '_scrape_month') as mock_scrape:
            mock_scrape.return_value = [
                {
                    'date': '15.03.2024',
                    'time': '18:00',
                    'committee': 'Rat der Stadt Lünen',
                    'title': 'Rat der Stadt Lünen',
                    'location': 'Rathaus',
                    'detail_url': 'http://example.com/detail/1'
                },
                {
                    'date': '16.03.2024',
                    'time': '19:00',
                    'committee': 'Irrelevanter Ausschuss',
                    'title': 'Irrelevanter Ausschuss',
                    'location': 'Anderswo',
                    'detail_url': 'http://example.com/detail/2'
                },
                {
                    'date': '17.03.2024',
                    'time': '17:30',
                    'committee': 'Rechnungsprüfungsausschuss',
                    'title': 'Rechnungsprüfungsausschuss',
                    'location': 'Verwaltung',
                    'detail_url': 'http://example.com/detail/3'
                }
            ]
            
            meetings = scraper.scrape_meetings(datetime(2024, 3, 1), datetime(2024, 3, 31))
            
            # Should only return relevant committees
            assert len(meetings) == 2
            committee_names = [m['committee'] for m in meetings]
            assert 'Rat der Stadt Lünen' in committee_names
            assert 'Rechnungsprüfungsausschuss' in committee_names
            assert 'Irrelevanter Ausschuss' not in committee_names