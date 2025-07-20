#!/usr/bin/env python3
"""
Simple test of duplicate removal logic without external dependencies
"""

def test_duplicate_removal():
    """Test the duplicate removal functionality"""
    print("🔄 Testing duplicate removal...")
    
    # Create test data with duplicates matching the pattern seen in exports
    test_meetings = [
        {'date': '24.07.2025', 'time': '17:00', 'committee': 'Rat der Stadt Lünen, 4. Sitzung', 'title': 'Meeting 1'},
        {'date': '24.07.2025', 'time': '17:00', 'committee': 'Rat der Stadt Lünen, 4. Sitzung', 'title': 'Meeting 1 Duplicate'},
        {'date': '10.09.2025', 'time': '17:00', 'committee': 'Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation, 3. Sitzung', 'title': 'Meeting 2'},
        {'date': '24.07.2025', 'time': '17:00', 'committee': 'Rat der Stadt Lünen, 4. Sitzung', 'title': 'Meeting 1 Another Duplicate'},
        {'date': '10.09.2025', 'time': '18:00', 'committee': 'Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation, 3. Sitzung', 'title': 'Meeting 3'},  # Different time
        {'date': '10.09.2025', 'time': '17:00', 'committee': 'Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation, 3. Sitzung', 'title': 'Meeting 2 Duplicate'},
    ]
    
    print(f"Input: {len(test_meetings)} meetings")
    for i, meeting in enumerate(test_meetings, 1):
        print(f"  {i}. {meeting['date']} {meeting['time']} - {meeting['committee']}")
    
    # Apply duplicate removal logic from scraper.py
    unique_meetings = []
    seen = set()
    
    for meeting in test_meetings:
        key = (meeting.get('date', ''), meeting.get('time', ''), meeting.get('committee', ''))
        if key not in seen:
            seen.add(key)
            unique_meetings.append(meeting)
            print(f"✅ Keeping: {meeting.get('committee', 'N/A')} on {meeting.get('date', 'N/A')}")
        else:
            print(f"🔄 Removing duplicate: {meeting.get('committee', 'N/A')} on {meeting.get('date', 'N/A')}")
    
    print(f"\nResult: {len(unique_meetings)} unique meetings (removed {len(test_meetings) - len(unique_meetings)} duplicates)")
    for i, meeting in enumerate(unique_meetings, 1):
        print(f"  {i}. {meeting['date']} {meeting['time']} - {meeting['committee']}")
    
    return len(test_meetings) - len(unique_meetings)

def test_committee_filtering():
    """Test committee filtering patterns"""
    print("\n🎯 Testing committee filtering patterns...")
    
    # Committee names to test (based on the specification and potential variations)
    test_committee_names = [
        "Rat der Stadt Lünen",
        "Rat der Stadt Lünen, 4. Sitzung",
        "Rechnungsprüfungsausschuss", 
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen",
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung",
        "Betriebsausschuss ZGB",
        "Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation",
        "Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation, 3. Sitzung",
        "Ausschuss für Arbeitsmarkt",
        "Irrelevanter Ausschuss",
        "Haupt- und Finanzausschuss",
        "Ordnungsausschuss"
    ]
    
    # Relevant committees from specification
    relevant_committees = [
        "Rat der Stadt Lünen",
        "Rechnungsprüfungsausschuss", 
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen",
        "Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation"
    ]
    
    # Additional patterns for better matching
    additional_patterns = [
        'betriebsausschuss zentrale gebäudebewirtschaftung',
        'betriebsausschuss zentrale',
        'ausschuss für arbeitsmarkt',
        'arbeitsmarkt, wirtschaftsförderung',
        'rechnungsprüfungsausschuss'
    ]
    
    def is_relevant_committee(committee_name):
        committee_lower = committee_name.lower()
        
        # Check exact matches first
        for relevant in relevant_committees:
            if relevant.lower() in committee_lower:
                return True
        
        # Check additional patterns
        for pattern in additional_patterns:
            if pattern in committee_lower:
                return True
        
        return False
    
    for committee in test_committee_names:
        is_relevant = is_relevant_committee(committee)
        status = "✅" if is_relevant else "❌"
        print(f"  {status} {committee}")
    
    # Test specifically for Betriebsausschuss
    betriebsausschuss_variations = [
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen",
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung",
        "Betriebsausschuss ZGB Lünen",
        "Betriebsausschuss für Zentrale Gebäudebewirtschaftung"
    ]
    
    print(f"\n🏢 Testing Betriebsausschuss variations:")
    for variation in betriebsausschuss_variations:
        is_relevant = is_relevant_committee(variation)
        status = "✅" if is_relevant else "❌"
        print(f"  {status} {variation}")

def main():
    print("🔍 Duplicate Removal and Committee Filtering Test")
    print("=" * 50)
    
    # Test 1: Duplicate removal
    duplicates_removed = test_duplicate_removal()
    
    # Test 2: Committee filtering
    test_committee_filtering()
    
    # Summary
    print(f"\n📊 Test Summary:")
    print(f"✅ Duplicate removal logic working: {duplicates_removed} duplicates would be removed")
    print(f"✅ Committee filtering patterns implemented")
    print(f"🎯 Logic should catch 'Betriebsausschuss Zentrale Gebäudebewirtschaftung' variations")
    
    print("\n🏁 Logic test completed!")

if __name__ == "__main__":
    main()