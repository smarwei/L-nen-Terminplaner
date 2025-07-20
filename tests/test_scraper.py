import pytest
import os
from datetime import datetime
from unittest.mock import patch, MagicMock
import responses
from bs4 import BeautifulSoup
from scraper import RatsInfoScraper


class TestRatsInfoScraper:
    
    @pytest.fixture
    def scraper(self):
        return RatsInfoScraper()
    
    @pytest.fixture
    def sample_html(self):
        with open(os.path.join(os.path.dirname(__file__), 'test_data', 'sample_html.html'), 'r') as f:
            return f.read()
    
    @pytest.fixture
    def detail_page_html(self):
        with open(os.path.join(os.path.dirname(__file__), 'test_data', 'detail_page.html'), 'r') as f:
            return f.read()
    
    def test_init(self, scraper):
        assert scraper.base_url == "https://luenen.ratsinfomanagement.net"
        assert scraper.termine_url == "https://luenen.ratsinfomanagement.net/termine/"
        assert len(scraper.relevant_committees) == 4
        assert "Rat der Stadt Lünen" in scraper.relevant_committees
    
    def test_parse_meeting_date_valid(self, scraper):
        date_str = "15.03.2024"
        result = scraper._parse_meeting_date(date_str)
        
        assert result.year == 2024
        assert result.month == 3
        assert result.day == 15
    
    def test_parse_meeting_date_invalid(self, scraper):
        invalid_dates = ["invalid", "32.13.2024", "", None]
        
        for date_str in invalid_dates:
            result = scraper._parse_meeting_date(date_str)
            assert isinstance(result, datetime)
    
    def test_is_relevant_committee_true(self, scraper):
        relevant_names = [
            "Rat der Stadt Lünen",
            "rat der stadt lünen",
            "Rechnungsprüfungsausschuss",
            "Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen",
            "Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation"
        ]
        
        for name in relevant_names:
            assert scraper._is_relevant_committee(name) == True
    
    def test_is_relevant_committee_false(self, scraper):
        irrelevant_names = [
            "Irrelevanter Ausschuss",
            "Sportausschuss",
            "Kulturausschuss",
            ""
        ]
        
        for name in irrelevant_names:
            assert scraper._is_relevant_committee(name) == False
    
    def test_parse_meeting_row_valid(self, scraper, sample_html):
        soup = BeautifulSoup(sample_html, 'html.parser')
        rows = soup.find_all('tr', class_=['table-row-odd', 'table-row-even'])
        
        # Test first row (Rat der Stadt Lünen)
        first_row = rows[0]
        meeting = scraper._parse_meeting_row(first_row)
        
        assert meeting is not None
        assert meeting['date'] == "15.03.2024"
        assert meeting['time'] == "18:00"
        assert meeting['committee'] == "Rat der Stadt Lünen"
        assert meeting['location'] == "Rathaus, Sitzungssaal"
        assert meeting['detail_url'].endswith('/detail/12345')
    
    def test_parse_meeting_row_no_link(self, scraper):
        html = """
        <tr class="table-row-odd">
            <td>15.03.2024</td>
            <td>18:00</td>
            <td>Rat der Stadt Lünen</td>
            <td>Rathaus</td>
        </tr>
        """
        soup = BeautifulSoup(html, 'html.parser')
        row = soup.find('tr')
        
        meeting = scraper._parse_meeting_row(row)
        
        assert meeting is not None
        assert meeting['committee'] == "Rat der Stadt Lünen"
        assert meeting['detail_url'] == ""
    
    def test_parse_meeting_row_insufficient_cells(self, scraper):
        html = """
        <tr class="table-row-odd">
            <td>15.03.2024</td>
            <td>18:00</td>
        </tr>
        """
        soup = BeautifulSoup(html, 'html.parser')
        row = soup.find('tr')
        
        meeting = scraper._parse_meeting_row(row)
        assert meeting is None
    
    def test_parse_meeting_row_exception(self, scraper):
        invalid_row = MagicMock()
        invalid_row.find_all.side_effect = Exception("Parsing error")
        
        meeting = scraper._parse_meeting_row(invalid_row)
        assert meeting is None
    
    @responses.activate
    def test_get_pdf_url_success(self, scraper, detail_page_html):
        detail_url = "https://luenen.ratsinfomanagement.net/detail/12345"
        responses.add(
            responses.GET,
            detail_url,
            body=detail_page_html,
            status=200
        )
        
        pdf_url = scraper._get_pdf_url(detail_url)
        
        assert pdf_url is not None
        assert pdf_url.endswith('.pdf')
        assert 'einladung' in pdf_url.lower()
    
    @responses.activate
    def test_get_pdf_url_no_pdfs(self, scraper):
        detail_url = "https://luenen.ratsinfomanagement.net/detail/12345"
        html_without_pdfs = "<html><body><p>No PDFs here</p></body></html>"
        
        responses.add(
            responses.GET,
            detail_url,
            body=html_without_pdfs,
            status=200
        )
        
        pdf_url = scraper._get_pdf_url(detail_url)
        assert pdf_url is None
    
    def test_get_pdf_url_empty_url(self, scraper):
        pdf_url = scraper._get_pdf_url("")
        assert pdf_url is None
        
        pdf_url = scraper._get_pdf_url(None)
        assert pdf_url is None
    
    @responses.activate
    def test_get_pdf_url_connection_error(self, scraper):
        detail_url = "https://luenen.ratsinfomanagement.net/detail/12345"
        responses.add(
            responses.GET,
            detail_url,
            status=500
        )
        
        pdf_url = scraper._get_pdf_url(detail_url)
        assert pdf_url is None
    
    @responses.activate 
    def test_scrape_month_success(self, scraper, sample_html):
        url = "https://luenen.ratsinfomanagement.net/termine/?year=2024&month=03"
        responses.add(
            responses.GET,
            url,
            body=sample_html,
            status=200
        )
        
        meetings = scraper._scrape_month(2024, 3)
        
        assert len(meetings) == 4
        assert any(m['committee'] == "Rat der Stadt Lünen" for m in meetings)
        assert any(m['committee'] == "Rechnungsprüfungsausschuss" for m in meetings)
    
    @responses.activate
    def test_scrape_month_connection_error(self, scraper):
        url = "https://luenen.ratsinfomanagement.net/termine/?year=2024&month=03"
        responses.add(
            responses.GET,
            url,
            status=500
        )
        
        meetings = scraper._scrape_month(2024, 3)
        assert meetings == []
    
    @patch.object(RatsInfoScraper, '_scrape_month')
    @patch.object(RatsInfoScraper, '_get_pdf_url')
    def test_scrape_meetings_single_month(self, mock_get_pdf, mock_scrape_month, scraper):
        mock_meetings = [
            {
                'date': '15.03.2024',
                'time': '18:00',
                'committee': 'Rat der Stadt Lünen',
                'title': 'Rat der Stadt Lünen',
                'location': 'Rathaus',
                'detail_url': 'http://example.com/detail/1'
            }
        ]
        mock_scrape_month.return_value = mock_meetings
        mock_get_pdf.return_value = 'http://example.com/test.pdf'
        
        start_date = datetime(2024, 3, 1)
        end_date = datetime(2024, 3, 31)
        
        meetings = scraper.scrape_meetings(start_date, end_date)
        
        assert len(meetings) == 1
        assert meetings[0]['committee'] == 'Rat der Stadt Lünen'
        assert meetings[0]['pdf_url'] == 'http://example.com/test.pdf'
    
    @patch.object(RatsInfoScraper, '_scrape_month')
    def test_scrape_meetings_multiple_months(self, mock_scrape_month, scraper):
        mock_scrape_month.return_value = []
        
        start_date = datetime(2024, 2, 15)
        end_date = datetime(2024, 4, 15)
        
        scraper.scrape_meetings(start_date, end_date)
        
        # Should call scrape_month for February, March, and April
        assert mock_scrape_month.call_count == 3
    
    @patch.object(RatsInfoScraper, '_scrape_month')
    @patch.object(RatsInfoScraper, '_get_pdf_url')
    def test_scrape_meetings_filtering(self, mock_get_pdf, mock_scrape_month, scraper):
        mock_meetings = [
            {
                'date': '15.03.2024',
                'time': '18:00',
                'committee': 'Rat der Stadt Lünen',
                'title': 'Rat der Stadt Lünen',
                'location': 'Rathaus',
                'detail_url': 'http://example.com/detail/1'
            },
            {
                'date': '20.03.2024',
                'time': '19:00',
                'committee': 'Irrelevanter Ausschuss',
                'title': 'Irrelevanter Ausschuss',
                'location': 'Anderswo',
                'detail_url': 'http://example.com/detail/2'
            }
        ]
        mock_scrape_month.return_value = mock_meetings
        mock_get_pdf.return_value = None
        
        start_date = datetime(2024, 3, 1)
        end_date = datetime(2024, 3, 31)
        
        meetings = scraper.scrape_meetings(start_date, end_date)
        
        # Should only return the relevant committee
        assert len(meetings) == 1
        assert meetings[0]['committee'] == 'Rat der Stadt Lünen'
    
    @patch.object(RatsInfoScraper, '_scrape_month')
    @patch.object(RatsInfoScraper, '_get_pdf_url')
    def test_scrape_meetings_date_filtering(self, mock_get_pdf, mock_scrape_month, scraper):
        mock_meetings = [
            {
                'date': '01.03.2024',  # Before range
                'time': '18:00',
                'committee': 'Rat der Stadt Lünen',
                'title': 'Rat der Stadt Lünen',
                'location': 'Rathaus',
                'detail_url': 'http://example.com/detail/1'
            },
            {
                'date': '15.03.2024',  # In range
                'time': '18:00',
                'committee': 'Rat der Stadt Lünen',
                'title': 'Rat der Stadt Lünen',
                'location': 'Rathaus',
                'detail_url': 'http://example.com/detail/2'
            },
            {
                'date': '31.03.2024',  # After range
                'time': '18:00',
                'committee': 'Rat der Stadt Lünen',
                'title': 'Rat der Stadt Lünen',
                'location': 'Rathaus',
                'detail_url': 'http://example.com/detail/3'
            }
        ]
        mock_scrape_month.return_value = mock_meetings
        mock_get_pdf.return_value = None
        
        start_date = datetime(2024, 3, 10)
        end_date = datetime(2024, 3, 20)
        
        meetings = scraper.scrape_meetings(start_date, end_date)
        
        # Should only return the meeting in the date range
        assert len(meetings) == 1
        assert meetings[0]['date'] == '15.03.2024'