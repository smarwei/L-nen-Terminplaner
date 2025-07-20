import pytest
import os
import tempfile
import shutil
from unittest.mock import MagicMock

@pytest.fixture(scope="session")
def test_data_dir():
    return os.path.join(os.path.dirname(__file__), 'tests', 'test_data')

@pytest.fixture
def temp_directory():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_requests_session():
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_session.get.return_value = mock_response
    return mock_session

@pytest.fixture
def sample_pdf_content():
    return b"%PDF-1.4\nTest PDF content\n%%EOF"

@pytest.fixture
def sample_html_content():
    return """
    <html>
    <body>
        <table>
            <tr class="table-row-odd">
                <td>15.03.2024</td>
                <td>18:00</td>
                <td><a href="/detail/1">Rat der Stadt Lünen</a></td>
                <td>Rathaus</td>
            </tr>
        </table>
    </body>
    </html>
    """

@pytest.fixture
def sample_meeting_data():
    return {
        'title': 'Rat der Stadt Lünen',
        'date': '15.03.2024',
        'time': '18:00',
        'location': 'Rathaus, Sitzungssaal',
        'committee': 'Rat der Stadt Lünen',
        'detail_url': 'http://example.com/detail/1',
        'pdf_url': 'http://example.com/test.pdf',
        'summary': 'Test summary'
    }