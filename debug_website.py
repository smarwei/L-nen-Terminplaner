#!/usr/bin/env python3
"""
Debug the website structure to understand how to scrape it properly
"""

import requests
from bs4 import BeautifulSoup
import re

def analyze_website_structure():
    """Analyze the actual HTML structure of the website"""
    print("🔍 Analyzing website structure...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Test different URLs
    urls = [
        "https://luenen.ratsinfomanagement.net/termine/",
        "https://luenen.ratsinfomanagement.net/termine/?year=2024&month=11",
        "https://luenen.ratsinfomanagement.net/termine/kalender/2024/11",
        "https://luenen.ratsinfomanagement.net/termine/liste",
    ]
    
    for url in urls:
        print(f"\n🌐 Analyzing: {url}")
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            print(f"Status: {response.status_code}")
            print(f"Content-Length: {len(response.content)}")
            
            # Look for different types of containers
            containers_to_check = [
                ('Tables', 'table'),
                ('Table rows', 'tr'),
                ('List items', 'li'),
                ('Divs with classes', 'div[class]'),
                ('Links', 'a[href]'),
                ('Calendar events', '.calendar, .event, .termin'),
                ('Date elements', '[data-date]'),
            ]
            
            for name, selector in containers_to_check:
                elements = soup.select(selector)
                if elements:
                    print(f"  ✅ {name}: {len(elements)} found")
                    if len(elements) <= 5:  # Show details for small numbers
                        for i, elem in enumerate(elements[:3]):
                            text = elem.get_text(strip=True)[:100]
                            print(f"    {i+1}. {text}...")
            
            # Look for script tags that might load data dynamically
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and any(term in script.string.lower() for term in ['ajax', 'fetch', 'xhr', 'json']):
                    print(f"  📜 Found dynamic loading script")
                    break
            
            # Look for specific German meeting terms
            content = response.text.lower()
            meeting_terms = ['sitzung', 'rat', 'ausschuss', 'termin', 'tagesordnung']
            found_terms = [term for term in meeting_terms if term in content]
            if found_terms:
                print(f"  🎯 Meeting terms found: {', '.join(found_terms)}")
            
            # Look for date patterns
            date_patterns = re.findall(r'\d{1,2}\.\d{1,2}\.\d{4}', response.text)
            if date_patterns:
                print(f"  📅 Date patterns found: {len(date_patterns)} (e.g., {date_patterns[0]})")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def find_data_endpoints():
    """Try to find AJAX endpoints or JSON data"""
    print("\n🔎 Looking for data endpoints...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Common AJAX endpoint patterns
    potential_endpoints = [
        "https://luenen.ratsinfomanagement.net/termine/ajax",
        "https://luenen.ratsinfomanagement.net/termine/data",
        "https://luenen.ratsinfomanagement.net/termine/events",
        "https://luenen.ratsinfomanagement.net/api/termine",
        "https://luenen.ratsinfomanagement.net/termine/kalender/events",
        "https://luenen.ratsinfomanagement.net/termine/json",
    ]
    
    for endpoint in potential_endpoints:
        try:
            response = session.get(endpoint, timeout=5)
            if response.status_code == 200:
                print(f"✅ Found endpoint: {endpoint}")
                content_type = response.headers.get('content-type', '')
                print(f"   Content-Type: {content_type}")
                print(f"   Length: {len(response.content)}")
                
                # Check if it's JSON
                if 'json' in content_type:
                    try:
                        data = response.json()
                        print(f"   JSON keys: {list(data.keys()) if isinstance(data, dict) else 'List with ' + str(len(data)) + ' items'}")
                    except:
                        print("   JSON parsing failed")
        except:
            continue

def main():
    print("🕵️ Website Structure Debug Tool")
    print("=" * 40)
    
    analyze_website_structure()
    find_data_endpoints()
    
    print("\n🏁 Analysis completed!")

if __name__ == "__main__":
    main()