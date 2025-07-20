#!/usr/bin/env python3
"""
Test to find missing meetings and fix duplicate issues
"""

from datetime import datetime, timedelta
from scraper import RatsInfoScraper
import json

def test_specific_dates():
    """Test specific date ranges to find missing meetings"""
    print("🔍 Testing specific dates for missing meetings...")
    
    scraper = RatsInfoScraper()
    
    # Test around the mentioned date (12.06.2025)
    test_periods = [
        (2025, 6),   # Juni 2025 - wo der Betriebsausschuss sein sollte
        (2025, 5),   # Mai 2025
        (2025, 7),   # Juli 2025
        (2025, 4),   # April 2025
    ]
    
    all_found_meetings = []
    
    for year, month in test_periods:
        print(f"\n📅 Testing {month:02d}/{year}...")
        try:
            meetings = scraper._scrape_month_json(year, month)
            print(f"Found {len(meetings)} meetings in JSON")
            
            # Show all meetings, not just relevant ones
            for meeting in meetings:
                title = meeting.get('title', meeting.get('committee', 'N/A'))
                date = meeting.get('date', 'N/A')
                print(f"  📋 {title} - {date}")
                
                # Check if this is the Betriebsausschuss we're looking for
                if 'betriebsausschuss' in title.lower() or 'gebäudebewirtschaftung' in title.lower():
                    print(f"  🎯 FOUND BETRIEBSAUSSCHUSS: {title}")
                    all_found_meetings.append(meeting)
                
                # Add all meetings for analysis
                all_found_meetings.append(meeting)
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return all_found_meetings

def test_committee_filtering():
    """Test committee filtering with various names"""
    print("\n🎯 Testing committee filtering...")
    
    scraper = RatsInfoScraper()
    
    test_committee_names = [
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen",
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung",
        "Betriebsausschuss ZGB",
        "Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation",
        "Ausschuss für Arbeitsmarkt",
        "Rat der Stadt Lünen",
        "Rechnungsprüfungsausschuss",
        "Irrelevanter Ausschuss"
    ]
    
    for committee in test_committee_names:
        is_relevant = scraper._is_relevant_committee(committee)
        status = "✅" if is_relevant else "❌"
        print(f"  {status} {committee}")

def test_duplicate_removal():
    """Test the duplicate removal functionality"""
    print("\n🔄 Testing duplicate removal...")
    
    # Create test data with duplicates
    test_meetings = [
        {'date': '24.07.2025', 'time': '17:00', 'committee': 'Rat der Stadt Lünen', 'title': 'Meeting 1'},
        {'date': '24.07.2025', 'time': '17:00', 'committee': 'Rat der Stadt Lünen', 'title': 'Meeting 1 Duplicate'},
        {'date': '10.09.2025', 'time': '17:00', 'committee': 'Ausschuss für Arbeitsmarkt', 'title': 'Meeting 2'},
        {'date': '24.07.2025', 'time': '17:00', 'committee': 'Rat der Stadt Lünen', 'title': 'Meeting 1 Another Duplicate'},
        {'date': '10.09.2025', 'time': '18:00', 'committee': 'Ausschuss für Arbeitsmarkt', 'title': 'Meeting 3'},  # Different time
    ]
    
    print(f"Input: {len(test_meetings)} meetings")
    for meeting in test_meetings:
        print(f"  {meeting['date']} {meeting['time']} - {meeting['title']}")
    
    # Simulate duplicate removal logic
    unique_meetings = []
    seen = set()
    
    for meeting in test_meetings:
        key = (meeting.get('date', ''), meeting.get('time', ''), meeting.get('committee', ''))
        if key not in seen:
            seen.add(key)
            unique_meetings.append(meeting)
        else:
            print(f"🔄 Would remove duplicate: {meeting.get('title', 'N/A')}")
    
    print(f"\nOutput: {len(unique_meetings)} unique meetings")
    for meeting in unique_meetings:
        print(f"  {meeting['date']} {meeting['time']} - {meeting['title']}")

def test_wide_date_range():
    """Test with a wide date range to find all available meetings"""
    print("\n📊 Testing wide date range...")
    
    scraper = RatsInfoScraper()
    
    # Test from 2025-01 to 2025-12
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    try:
        meetings = scraper.scrape_meetings(start_date, end_date)
        print(f"✅ Found {len(meetings)} meetings in entire year 2025")
        
        # Group by committee
        by_committee = {}
        for meeting in meetings:
            committee = meeting.get('committee', 'Unknown')
            if committee not in by_committee:
                by_committee[committee] = []
            by_committee[committee].append(meeting)
        
        print("\n📋 Meetings by committee:")
        for committee, committee_meetings in by_committee.items():
            print(f"  {committee}: {len(committee_meetings)} meetings")
            for meeting in committee_meetings[:2]:  # Show first 2
                print(f"    - {meeting.get('date', 'N/A')} {meeting.get('time', '')}")
        
        return meetings
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    print("🔍 Missing Meetings and Duplicate Test")
    print("=" * 45)
    
    # Test 1: Specific dates
    specific_meetings = test_specific_dates()
    
    # Test 2: Committee filtering
    test_committee_filtering()
    
    # Test 3: Duplicate removal
    test_duplicate_removal()
    
    # Test 4: Wide date range
    wide_range_meetings = test_wide_date_range()
    
    # Summary
    print(f"\n📊 Test Summary:")
    print(f"Specific date meetings: {len(specific_meetings)}")
    print(f"Wide range meetings: {len(wide_range_meetings)}")
    
    # Check for Betriebsausschuss
    betriebsausschuss_found = False
    for meeting in specific_meetings + wide_range_meetings:
        title = meeting.get('title', meeting.get('committee', ''))
        if 'betriebsausschuss' in title.lower() or 'gebäudebewirtschaftung' in title.lower():
            betriebsausschuss_found = True
            print(f"🎯 Betriebsausschuss found: {title} on {meeting.get('date', 'N/A')}")
    
    if not betriebsausschuss_found:
        print("❌ Betriebsausschuss Zentrale Gebäudebewirtschaftung not found")
        print("💡 This might be because:")
        print("   1. The meeting is not in the tested date range")
        print("   2. The committee name format is different")
        print("   3. The meeting is not yet scheduled")
    
    print("\n🏁 Missing meetings test completed!")

if __name__ == "__main__":
    main()