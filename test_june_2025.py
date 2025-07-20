#!/usr/bin/env python3
"""
Specific test to find the missing meeting from 12.06.2025
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def test_june_2025_direct():
    """Test direct API calls for June 2025"""
    print("🔍 Testing June 2025 directly...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Get CSRF token
    try:
        response = session.get("https://luenen.ratsinfomanagement.net/termine/", timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        csrf_token = None
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        if csrf_meta:
            csrf_token = csrf_meta.get('content')
        
        print(f"CSRF Token: {csrf_token}")
        
    except Exception as e:
        print(f"Error getting CSRF token: {e}")
        return
    
    # Test JSON API for June 2025
    json_url = "https://luenen.ratsinfomanagement.net/termine/json/Sitzungstermine/"
    
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    if csrf_token:
        headers['X-CSRF-Token'] = csrf_token
    
    # Test different date ranges for June 2025
    date_ranges = [
        ('2025-06-01', '2025-06-30'),  # Full month
        ('2025-06-12', '2025-06-12'),  # Specific date
        ('2025-06-10', '2025-06-15'),  # Around the date
        ('2025-05-01', '2025-07-31'),  # Wider range
    ]
    
    for start_date, end_date in date_ranges:
        print(f"\n📅 Testing range {start_date} to {end_date}")
        
        data = {
            'start': start_date,
            'end': end_date
        }
        
        try:
            response = session.post(json_url, data=data, headers=headers, timeout=15)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    print(f"JSON response type: {type(json_data)}")
                    
                    if isinstance(json_data, list):
                        events = json_data
                    elif isinstance(json_data, dict):
                        print(f"JSON keys: {list(json_data.keys())}")
                        events = []
                        for key, value in json_data.items():
                            if isinstance(value, list):
                                events.extend(value)
                    else:
                        events = []
                    
                    print(f"Found {len(events)} events")
                    
                    # Look for events on or around 12.06.2025
                    for event in events:
                        title = event.get('title', event.get('summary', ''))
                        start = event.get('start', event.get('startTime', ''))
                        
                        print(f"  📋 {title} - {start}")
                        
                        # Check if this could be the Betriebsausschuss
                        if ('betriebsausschuss' in title.lower() or 
                            'gebäudebewirtschaftung' in title.lower() or
                            '12.06' in str(start) or
                            '2025-06-12' in str(start)):
                            print(f"  🎯 POTENTIAL MATCH: {title} on {start}")
                        
                        # Also check if any committee matches our patterns
                        committee_patterns = [
                            'betriebsausschuss',
                            'gebäudebewirtschaftung', 
                            'zentrale',
                            'zgb'
                        ]
                        
                        for pattern in committee_patterns:
                            if pattern in title.lower():
                                print(f"  🔍 COMMITTEE PATTERN '{pattern}' found in: {title}")
                    
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print(f"Response content: {response.text[:500]}")
            else:
                print(f"HTTP Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"Request error: {e}")

def test_html_pages():
    """Test different HTML page URLs"""
    print("\n🌐 Testing HTML pages for June 2025...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    urls_to_test = [
        "https://luenen.ratsinfomanagement.net/termine/?year=2025&month=06",
        "https://luenen.ratsinfomanagement.net/termine/kalender/2025/06",
        "https://luenen.ratsinfomanagement.net/termine/liste?von=2025-06-01&bis=2025-06-30",
        "https://luenen.ratsinfomanagement.net/termine/",
    ]
    
    for url in urls_to_test:
        print(f"\n🔗 Testing {url}")
        try:
            response = session.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for any mention of Betriebsausschuss or June 12
                text = soup.get_text().lower()
                if 'betriebsausschuss' in text:
                    print("  ✅ Found 'betriebsausschuss' in page text")
                if 'gebäudebewirtschaftung' in text:
                    print("  ✅ Found 'gebäudebewirtschaftung' in page text")
                if '12.06' in text or '12. juni' in text:
                    print("  ✅ Found date references in page text")
                
                # Look for links that might contain meetings
                links = soup.find_all('a', href=True)
                for link in links:
                    link_text = link.get_text().lower()
                    if ('betriebsausschuss' in link_text or 
                        'gebäudebewirtschaftung' in link_text):
                        print(f"  🔗 Found relevant link: {link_text} -> {link['href']}")
                        
        except Exception as e:
            print(f"Error: {e}")

def main():
    print("🔍 Specific Search for 12.06.2025 Meeting")
    print("=" * 50)
    
    test_june_2025_direct()
    test_html_pages()
    
    print("\n📊 Summary:")
    print("If no specific meetings for 12.06.2025 were found, it could mean:")
    print("1. The meeting is not yet scheduled in the system")
    print("2. The meeting is named differently than expected")
    print("3. The meeting is in a different committee category")
    print("4. The date might be different than 12.06.2025")

if __name__ == "__main__":
    main()