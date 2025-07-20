#!/usr/bin/env python3
"""
Test the improved JSON-based scraping
"""

from datetime import datetime, timedelta
from scraper import RatsInfoScraper
import json

def test_json_api_directly():
    """Test the JSON API endpoint directly"""
    print("🔍 Testing JSON API directly...")
    
    scraper = RatsInfoScraper()
    
    # Test current and recent months
    test_months = [
        (2024, 12),  # Dezember 2024
        (2024, 11),  # November 2024
        (2025, 1),   # Januar 2025
        (2024, 10),  # Oktober 2024
    ]
    
    for year, month in test_months:
        print(f"\n📅 Testing {month:02d}/{year}...")
        
        try:
            meetings = scraper._scrape_month_json(year, month)
            print(f"✅ Found {len(meetings)} meetings via JSON API")
            
            if meetings:
                print("Sample meetings:")
                for i, meeting in enumerate(meetings[:3]):
                    print(f"  {i+1}. {meeting.get('title', 'N/A')} - {meeting.get('date', 'N/A')} at {meeting.get('time', 'N/A')}")
                
                return meetings  # Return first successful result
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return []

def test_csrf_token():
    """Test CSRF token extraction"""
    print("\n🔐 Testing CSRF token extraction...")
    
    scraper = RatsInfoScraper()
    
    try:
        token = scraper._get_csrf_token()
        if token:
            print(f"✅ CSRF token found: {token[:20]}...")
        else:
            print("❌ No CSRF token found")
        return token
    except Exception as e:
        print(f"❌ CSRF token error: {e}")
        return None

def test_full_workflow_improved():
    """Test the complete improved workflow"""
    print("\n🔄 Testing improved full workflow...")
    
    scraper = RatsInfoScraper()
    
    # Test with recent date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)  # Last 2 months
    
    print(f"Testing date range: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}")
    
    try:
        meetings = scraper.scrape_meetings(start_date, end_date)
        print(f"✅ Complete workflow found {len(meetings)} meetings")
        
        if meetings:
            print("\nDetailed results:")
            for i, meeting in enumerate(meetings[:5]):
                print(f"  {i+1}. Committee: {meeting.get('committee', 'N/A')}")
                print(f"     Date: {meeting.get('date', 'N/A')} {meeting.get('time', '')}")
                print(f"     Location: {meeting.get('location', 'N/A')}")
                print(f"     Detail URL: {meeting.get('detail_url', 'N/A')}")
                print()
        
        return meetings
        
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        return []

def test_api_integration():
    """Test the Flask API with improved scraping"""
    print("\n🌐 Testing Flask API integration...")
    
    import requests
    
    try:
        # Test API endpoint with recent dates
        api_url = "http://localhost:5000/api/scrape"
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        payload = {
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d')
        }
        
        print(f"Sending API request: {payload}")
        
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                meetings = data.get('meetings', [])
                print(f"✅ API returned {len(meetings)} meetings")
                
                if meetings:
                    print("API meeting samples:")
                    for i, meeting in enumerate(meetings[:2]):
                        print(f"  {i+1}. {meeting.get('title', 'N/A')} - {meeting.get('date', 'N/A')}")
                        print(f"     Summary: {meeting.get('summary', 'N/A')[:100]}...")
                return meetings
            else:
                print(f"❌ API error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ API HTTP error: {response.status_code}")
            print(response.text[:200])
            
    except Exception as e:
        print(f"❌ API test error: {e}")
    
    return []

def main():
    print("🧪 Improved Scraping Test for Lünen Terminplaner")
    print("=" * 55)
    
    # Test 1: CSRF token
    csrf_token = test_csrf_token()
    
    # Test 2: JSON API directly
    json_meetings = test_json_api_directly()
    
    # Test 3: Full workflow
    workflow_meetings = test_full_workflow_improved()
    
    # Test 4: API integration
    api_meetings = test_api_integration()
    
    # Summary
    print("\n📊 Improved Test Summary:")
    print(f"CSRF token: {'✅ Found' if csrf_token else '❌ Not found'}")
    print(f"JSON API meetings: {len(json_meetings)}")
    print(f"Workflow meetings: {len(workflow_meetings)}")
    print(f"API meetings: {len(api_meetings)}")
    
    total_found = len(json_meetings) + len(workflow_meetings) + len(api_meetings)
    
    if total_found > 0:
        print("✅ Improved scraping is working!")
        print("\n🎯 Next steps:")
        print("- Test in web interface at http://localhost:5000")
        print("- Try different date ranges")
        print("- Check PDF processing for found meetings")
    else:
        print("❌ Still no meetings found - check JSON API response format")
    
    print("\n🏁 Improved scraping test completed!")

if __name__ == "__main__":
    main()