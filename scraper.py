import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from urllib.parse import urljoin, urlparse

class RatsInfoScraper:
    def __init__(self):
        self.base_url = "https://luenen.ratsinfomanagement.net"
        self.termine_url = "https://luenen.ratsinfomanagement.net/termine/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.relevant_committees = [
            "Rat der Stadt Lünen",
            "Rechnungsprüfungsausschuss", 
            "Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen",
            "Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation"
        ]
    
    def scrape_meetings(self, start_date, end_date):
        meetings = []
        current_date = start_date
        
        while current_date <= end_date:
            monthly_meetings = self._scrape_month(current_date.year, current_date.month)
            for meeting in monthly_meetings:
                meeting_date = self._parse_meeting_date(meeting['date'])
                print(f"Checking meeting: {meeting['title']} on {meeting['date']} (parsed: {meeting_date}) against range {start_date.date()} to {end_date.date()}")
                if start_date.date() <= meeting_date.date() <= end_date.date():
                    # Temporarily add all meetings to see what we're getting
                    meeting['pdf_url'] = self._get_pdf_url(meeting['detail_url'])
                    meetings.append(meeting)
                    
                    # Check if it would be relevant
                    if self._is_relevant_committee(meeting['committee']):
                        print(f"✅ Added RELEVANT meeting: {meeting['title']}")
                    else:
                        print(f"📋 Added meeting (not in standard list): {meeting['committee']}")
                else:
                    print(f"❌ Filtered out (date): {meeting_date.date()} not in range")
            
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        # Remove duplicates based on date, time, and committee
        unique_meetings = []
        seen = set()
        
        for meeting in meetings:
            key = (meeting.get('date', ''), meeting.get('time', ''), meeting.get('committee', ''))
            if key not in seen:
                seen.add(key)
                unique_meetings.append(meeting)
            else:
                print(f"🔄 Removed duplicate: {meeting.get('title', 'N/A')} on {meeting.get('date', 'N/A')}")
        
        print(f"📊 Found {len(meetings)} total, {len(unique_meetings)} unique meetings")
        return unique_meetings
    
    def _scrape_month(self, year, month):
        # First try the JSON API endpoint
        meetings = self._scrape_month_json(year, month)
        if meetings:
            return meetings
        
        # Fallback to HTML scraping
        return self._scrape_month_html(year, month)
    
    def _scrape_month_json(self, year, month):
        """Scrape using the JSON API endpoint"""
        try:
            # Get CSRF token first
            csrf_token = self._get_csrf_token()
            
            # Calculate date range for the month
            from datetime import datetime, timedelta
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)
            
            # JSON API endpoint
            json_url = "https://luenen.ratsinfomanagement.net/termine/json/Sitzungstermine/"
            
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            
            if csrf_token:
                headers['X-CSRF-Token'] = csrf_token
            
            data = {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            }
            
            print(f"Requesting JSON data for {month}/{year} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
            response = self.session.post(json_url, data=data, headers=headers, timeout=15)
            response.raise_for_status()
            
            json_data = response.json()
            print(f"JSON response keys: {json_data.keys() if isinstance(json_data, dict) else 'Not a dict'}")
            
            meetings = []
            
            # Parse events from JSON response
            if isinstance(json_data, list):
                events = json_data
            elif isinstance(json_data, dict) and 'events' in json_data:
                events = json_data['events']
            elif isinstance(json_data, dict) and len(json_data) > 0:
                # Try to find events in any key
                events = []
                for key, value in json_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        events = value
                        break
            else:
                events = []
            
            print(f"Found {len(events)} events in JSON response")
            
            for event in events:
                meeting = self._parse_json_event(event)
                if meeting:
                    # Add all meetings for now, filter later
                    print(f"📋 Found meeting: {meeting.get('committee', 'N/A')} on {meeting.get('date', 'N/A')}")
                    meetings.append(meeting)
            
            return meetings
            
        except Exception as e:
            print(f"JSON API fehler: {e}")
            return []
    
    def _get_csrf_token(self):
        """Extract CSRF token from the main page"""
        try:
            response = self.session.get(self.termine_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for CSRF token in meta tags
            csrf_meta = soup.find('meta', {'name': 'csrf-token'})
            if csrf_meta:
                return csrf_meta.get('content')
            
            # Look for CSRF token in script tags
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'csrf' in script.string.lower():
                    import re
                    token_match = re.search(r"'X-CSRF-Token':\s*'([^']+)'", script.string)
                    if token_match:
                        return token_match.group(1)
            
            return None
            
        except Exception as e:
            print(f"CSRF token extraction fehler: {e}")
            return None
    
    def _parse_json_event(self, event):
        """Parse a single event from JSON data"""
        try:
            # Common JSON fields for calendar events
            title = event.get('title', event.get('summary', ''))
            start = event.get('start', event.get('startTime', ''))
            end = event.get('end', event.get('endTime', ''))
            url = event.get('url', event.get('link', ''))
            
            # Parse date from various formats
            if isinstance(start, str):
                if 'T' in start:
                    # ISO format: 2024-12-15T18:00:00
                    date_part = start.split('T')[0]
                    time_part = start.split('T')[1][:5] if 'T' in start else ''
                else:
                    # Date only: 2024-12-15
                    date_part = start
                    time_part = ''
                
                # Convert to German format
                try:
                    from datetime import datetime
                    date_obj = datetime.strptime(date_part, '%Y-%m-%d')
                    date_str = date_obj.strftime('%d.%m.%Y')
                except:
                    date_str = date_part
            else:
                date_str = str(start)
                time_part = ''
            
            # Extract committee name from title
            committee = title
            
            # Build detail URL
            detail_url = url if url else ''
            if detail_url and not detail_url.startswith('http'):
                detail_url = urljoin(self.base_url, detail_url)
            
            meeting = {
                'date': date_str,
                'time': time_part,
                'committee': committee,
                'title': title,
                'location': event.get('location', ''),
                'detail_url': detail_url
            }
            
            print(f"Parsed JSON event: {title} on {date_str}")
            return meeting
            
        except Exception as e:
            print(f"Fehler beim Parsen eines JSON-Events: {e}")
            return None
    
    def _scrape_month_html(self, year, month):
        """Fallback HTML scraping method"""
        urls_to_try = [
            f"{self.termine_url}?year={year}&month={month:02d}",
            f"https://luenen.ratsinfomanagement.net/termine/kalender/{year}/{month:02d}",
            f"https://luenen.ratsinfomanagement.net/termine/liste?von={year}-{month:02d}-01&bis={year}-{month:02d}-31"
        ]
        
        for url in urls_to_try:
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                meetings = []
                
                # Try different selectors for meeting data
                meeting_selectors = [
                    'tr.table-row-odd, tr.table-row-even',
                    '.calendar-event',
                    '.meeting-row',
                    'tr[data-date]',
                    '.list-group-item'
                ]
                
                for selector in meeting_selectors:
                    elements = soup.select(selector)
                    if elements:
                        print(f"Found {len(elements)} elements with selector: {selector}")
                        for element in elements:
                            meeting = self._parse_meeting_element(element)
                            if meeting:
                                meetings.append(meeting)
                        break
                
                if meetings:
                    return meetings
                    
            except requests.RequestException as e:
                print(f"Fehler beim HTML-Scraping von {url}: {e}")
                continue
        
        print(f"Keine Termine gefunden für {month}/{year}")
        return []
    
    def _parse_meeting_row(self, row):
        try:
            cells = row.find_all('td')
            if len(cells) < 4:
                return None
            
            date_cell = cells[0].get_text(strip=True)
            time_cell = cells[1].get_text(strip=True)
            committee_cell = cells[2]
            location_cell = cells[3].get_text(strip=True)
            
            committee_link = committee_cell.find('a')
            if committee_link:
                committee_name = committee_link.get_text(strip=True)
                detail_url = urljoin(self.base_url, committee_link.get('href', ''))
            else:
                committee_name = committee_cell.get_text(strip=True)
                detail_url = ''
            
            return {
                'date': date_cell,
                'time': time_cell,
                'committee': committee_name,
                'title': committee_name,
                'location': location_cell,
                'detail_url': detail_url
            }
            
        except Exception as e:
            print(f"Fehler beim Parsen einer Sitzungszeile: {e}")
            return None
    
    def _parse_meeting_element(self, element):
        """Parse a meeting element (could be tr, div, etc.)"""
        try:
            # Try to extract from tr element first
            if element.name == 'tr':
                return self._parse_meeting_row(element)
            
            # Try to extract from other elements
            text = element.get_text(strip=True)
            date_match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', text)
            time_match = re.search(r'(\d{1,2}):(\d{2})', text)
            
            if date_match:
                day, month, year = date_match.groups()
                date_str = f"{day}.{month}.{year}"
                
                time_str = ""
                if time_match:
                    time_str = time_match.group(0)
                
                # Try to find committee name
                committee = ""
                link = element.find('a')
                if link:
                    committee = link.get_text(strip=True)
                    detail_url = urljoin(self.base_url, link.get('href', ''))
                else:
                    # Extract committee from text
                    for relevant in self.relevant_committees:
                        if relevant.lower() in text.lower():
                            committee = relevant
                            break
                
                if committee:
                    return {
                        'date': date_str,
                        'time': time_str,
                        'committee': committee,
                        'title': committee,
                        'location': '',
                        'detail_url': detail_url if 'detail_url' in locals() else ''
                    }
                    
        except Exception as e:
            print(f"Fehler beim Parsen eines Meeting-Elements: {e}")
        
        return None
    
    def _parse_link_as_meeting(self, link, year, month):
        """Try to parse a link as a meeting"""
        try:
            text = link.get_text(strip=True)
            href = link.get('href', '')
            
            # Check if this looks like a meeting
            committee = ""
            for relevant in self.relevant_committees:
                if relevant.lower() in text.lower():
                    committee = relevant
                    break
            
            if committee:
                return {
                    'date': f"01.{month:02d}.{year}",  # Default date
                    'time': '',
                    'committee': committee,
                    'title': text,
                    'location': '',
                    'detail_url': urljoin(self.base_url, href)
                }
                
        except Exception as e:
            print(f"Fehler beim Parsen eines Links: {e}")
        
        return None
    
    def _parse_meeting_date(self, date_str):
        try:
            date_parts = date_str.split('.')
            if len(date_parts) >= 3:
                day = int(date_parts[0])
                month = int(date_parts[1]) 
                year = int(date_parts[2])
                return datetime(year, month, day)
        except:
            pass
        return datetime.now()
    
    def _is_relevant_committee(self, committee_name):
        # Exact matching and partial matching for committee names
        committee_lower = committee_name.lower()
        
        # Check exact matches first
        for relevant in self.relevant_committees:
            if relevant.lower() in committee_lower:
                return True
        
        # Additional patterns for better matching
        additional_patterns = [
            'betriebsausschuss zentrale gebäudebewirtschaftung',
            'betriebsausschuss zentrale',
            'betriebsausschuss zgb',
            'zentrale gebäudebewirtschaftung',
            'gebäudebewirtschaftung lünen',
            'zgb-ausschuss',
            'ausschuss für arbeitsmarkt',
            'arbeitsmarkt, wirtschaftsförderung',
            'rechnungsprüfungsausschuss'
        ]
        
        for pattern in additional_patterns:
            if pattern in committee_lower:
                print(f"✅ Matched committee pattern: '{pattern}' in '{committee_name}'")
                return True
        
        return False
    
    def _get_pdf_url(self, detail_url):
        if not detail_url:
            return None
            
        try:
            response = self.session.get(detail_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
            
            # Priority 1: Look for "Gesamtes Sitzungspaket"
            for link in pdf_links:
                link_text = link.get_text().lower()
                if 'gesamtes sitzungspaket' in link_text or 'gesamte sitzungspaket' in link_text:
                    href = link.get('href', '')
                    print(f"✅ Found 'Gesamtes Sitzungspaket' PDF: {link_text}")
                    return urljoin(self.base_url, href)
            
            # Priority 2: Look for other important documents
            priority_keywords = ['einladung', 'tagesordnung', 'protokoll', 'vorlage', 'sitzungspaket']
            for link in pdf_links:
                href = link.get('href', '')
                link_text = link.get_text().lower()
                if any(keyword in link_text for keyword in priority_keywords):
                    print(f"📄 Found priority PDF: {link_text}")
                    return urljoin(self.base_url, href)
            
            # Priority 3: Any PDF document
            if pdf_links:
                href = pdf_links[0].get('href', '')
                print(f"📄 Found generic PDF: {pdf_links[0].get_text()}")
                return urljoin(self.base_url, href)
                
        except Exception as e:
            print(f"Fehler beim Abrufen der PDF-URL von {detail_url}: {e}")
        
        return None