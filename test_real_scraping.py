#!/usr/bin/env python3
"""
Test real scraping with different time periods
"""

from datetime import datetime, timedelta
from scraper import RatsInfoScraper
import json

def test_historical_data():
    """Test scraping historical data that's more likely to exist"""
    print("🕐 Testing historical data scraping...")
    
    scraper = RatsInfoScraper()
    
    # Test different months to find data
    test_periods = [
        (2024, 11),  # November 2024
        (2024, 10),  # Oktober 2024  
        (2024, 9),   # September 2024
        (2024, 6),   # Juni 2024
        (2024, 3),   # März 2024
    ]
    
    for year, month in test_periods:
        print(f"\nTesting {month:02d}/{year}...")
        try:
            meetings = scraper._scrape_month(year, month)
            print(f"✅ Found {len(meetings)} meetings")
            
            if meetings:
                print("Sample meetings:")
                for i, meeting in enumerate(meetings[:2]):
                    print(f"  {i+1}. {meeting.get('title', 'N/A')} - {meeting.get('date', 'N/A')}")
                
                # Test PDF extraction for first meeting
                first_meeting = meetings[0]
                if first_meeting.get('detail_url'):
                    print(f"Testing PDF extraction for: {first_meeting['title']}")
                    pdf_url = scraper._get_pdf_url(first_meeting['detail_url'])
                    if pdf_url:
                        print(f"✅ Found PDF: {pdf_url}")
                    else:
                        print("❌ No PDF found")
                
                return meetings  # Return first successful result
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return []

def test_full_workflow():
    """Test the complete workflow end-to-end"""
    print("\n🔄 Testing full workflow...")
    
    scraper = RatsInfoScraper()
    
    # Test with a date range from a few months ago
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)  # Last 3 months
    
    print(f"Testing date range: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}")
    
    try:
        meetings = scraper.scrape_meetings(start_date, end_date)
        print(f"✅ Complete workflow found {len(meetings)} meetings")
        
        if meetings:
            print("\nSample results:")
            for i, meeting in enumerate(meetings[:3]):
                print(f"  {i+1}. {meeting.get('committee', 'N/A')}")
                print(f"     Date: {meeting.get('date', 'N/A')}")
                print(f"     URL: {meeting.get('detail_url', 'N/A')}")
                print(f"     PDF: {meeting.get('pdf_url', 'N/A')}")
                print()
        
        return meetings
        
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        return []

def main():
    print("🧪 Real Scraping Test for Lünen Terminplaner")
    print("=" * 50)
    
    # Test 1: Historical data
    historical_meetings = test_historical_data()
    
    # Test 2: Full workflow
    workflow_meetings = test_full_workflow()
    
    # Summary
    print("\n📊 Test Summary:")
    print(f"Historical meetings found: {len(historical_meetings)}")
    print(f"Workflow meetings found: {len(workflow_meetings)}")
    
    if historical_meetings or workflow_meetings:
        print("✅ Scraping is working!")
    else:
        print("❌ No meetings found - might need to adjust scraping logic")
    
    print("\n🏁 Real scraping test completed!")

if __name__ == "__main__":
    main()