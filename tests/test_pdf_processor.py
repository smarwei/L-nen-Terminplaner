import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open, MagicMock
from pdf_processor import PDFProcessor


class TestPDFProcessor:
    
    @pytest.fixture
    def pdf_processor(self):
        return PDFProcessor()
    
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_pdf_path(self):
        return os.path.join(os.path.dirname(__file__), 'test_data', 'sample.pdf')
    
    def test_clean_text(self, pdf_processor):
        dirty_text = "Dies   ist\n\nein\t\tTest   mit\nverschiedenen\n\nWhitespace-Zeichen."
        clean_text = pdf_processor._clean_text(dirty_text)
        
        assert "  " not in clean_text
        assert "\n" not in clean_text
        assert "\t" not in clean_text
        assert clean_text.strip() == clean_text
    
    def test_clean_text_special_characters(self, pdf_processor):
        text_with_special = "Normal text with @#$%^&* special chars!"
        cleaned = pdf_processor._clean_text(text_with_special)
        
        assert "@#$%^&*" not in cleaned
        assert "Normal text with  special chars!" == cleaned
    
    @patch('pdf_processor.requests.Session.get')
    def test_download_pdf_success(self, mock_get, pdf_processor, temp_dir):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b'fake pdf content']
        mock_get.return_value = mock_response
        
        pdf_url = "http://example.com/test.pdf"
        result_path = pdf_processor.download_pdf(pdf_url, temp_dir)
        
        assert result_path is not None
        assert os.path.exists(result_path)
        assert result_path.endswith('.pdf')
        
        with open(result_path, 'rb') as f:
            content = f.read()
            assert content == b'fake pdf content'
    
    @patch('pdf_processor.requests.Session.get')
    def test_download_pdf_failure(self, mock_get, pdf_processor, temp_dir):
        mock_get.side_effect = Exception("Network error")
        
        pdf_url = "http://example.com/test.pdf"
        result_path = pdf_processor.download_pdf(pdf_url, temp_dir)
        
        assert result_path is None
    
    def test_download_pdf_empty_url(self, pdf_processor, temp_dir):
        result = pdf_processor.download_pdf("", temp_dir)
        assert result is None
        
        result = pdf_processor.download_pdf(None, temp_dir)
        assert result is None
    
    @patch('fitz.open')
    def test_extract_text_success(self, mock_fitz_open, pdf_processor):
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Extracted text from PDF"
        mock_doc.page_count = 1
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz_open.return_value = mock_doc
        
        result = pdf_processor.extract_text("/fake/path.pdf")
        
        assert result == "Extracted text from PDF"
        mock_doc.close.assert_called_once()
    
    @patch('fitz.open')
    def test_extract_text_multiple_pages(self, mock_fitz_open, pdf_processor):
        mock_doc = MagicMock()
        mock_page1 = MagicMock()
        mock_page1.get_text.return_value = "Page 1 content"
        mock_page2 = MagicMock()
        mock_page2.get_text.return_value = "Page 2 content"
        
        mock_doc.page_count = 2
        mock_doc.__getitem__.side_effect = [mock_page1, mock_page2]
        mock_fitz_open.return_value = mock_doc
        
        result = pdf_processor.extract_text("/fake/path.pdf")
        
        assert "Page 1 content" in result
        assert "Page 2 content" in result
    
    def test_extract_text_nonexistent_file(self, pdf_processor):
        result = pdf_processor.extract_text("/nonexistent/file.pdf")
        assert result == ""
    
    def test_extract_text_none_path(self, pdf_processor):
        result = pdf_processor.extract_text(None)
        assert result == ""
    
    @patch('fitz.open')
    def test_extract_text_exception(self, mock_fitz_open, pdf_processor):
        mock_fitz_open.side_effect = Exception("PDF reading error")
        
        result = pdf_processor.extract_text("/fake/path.pdf")
        assert result == ""
    
    def test_summarize_text_short_text(self, pdf_processor):
        short_text = "Too short"
        result = pdf_processor.summarize_text(short_text)
        
        assert "Zu wenig Text" in result
    
    def test_summarize_text_empty(self, pdf_processor):
        result = pdf_processor.summarize_text("")
        assert "Zu wenig Text" in result
        
        result = pdf_processor.summarize_text(None)
        assert "Zu wenig Text" in result
    
    def test_summarize_text_success(self, pdf_processor):
        long_text = "Dies ist ein sehr langer Text " * 20
        
        result = pdf_processor.summarize_text(long_text)
        
        # Should use fallback since SUMY might not be available
        assert len(result) > 0
        assert result != "Zu wenig Text für eine Zusammenfassung verfügbar."
    
    def test_summarize_text_fallback(self, pdf_processor):
        long_text = "Dies ist ein Beschluss für die Verwaltung der Stadt. " * 5
        
        result = pdf_processor.summarize_text(long_text)
        
        assert "Beschluss" in result or "Verwaltung" in result or "Stadt" in result
    
    def test_create_simple_summary(self, pdf_processor):
        text = "Dies ist ein wichtiger Beschluss. Der Rat hat entschieden. Die Verwaltung wird handeln. Weitere unwichtige Details folgen."
        
        result = pdf_processor._create_simple_summary(text)
        
        assert len(result) > 0
        assert any(keyword in result.lower() for keyword in ['beschluss', 'rat', 'verwaltung'])
    
    def test_create_simple_summary_no_keywords(self, pdf_processor):
        text = "Dies ist normaler Text ohne wichtige Begriffe. " * 10
        
        result = pdf_processor._create_simple_summary(text)
        
        assert "Automatische Zusammenfassung nicht möglich" in result
    
    def test_get_german_stopwords(self, pdf_processor):
        stopwords = pdf_processor._get_german_stopwords()
        
        assert isinstance(stopwords, set)
        assert "der" in stopwords
        assert "die" in stopwords
        assert "und" in stopwords
        assert len(stopwords) > 50