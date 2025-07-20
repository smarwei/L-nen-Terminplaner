#!/usr/bin/env python3
"""
Simple test without external dependencies to check committee filtering
"""

def test_committee_filtering_extended():
    """Test the extended committee filtering patterns"""
    print("🎯 Testing extended committee filtering patterns...")
    
    # Test committee names that might represent the missing meeting
    test_committee_names = [
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen",
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung", 
        "Betriebsausschuss ZGB",
        "ZGB Lünen",
        "Zentrale Gebäudebewirtschaftung",
        "Gebäudebewirtschaftung Lünen",
        "Betriebsausschuss der Stadt Lünen",
        "Betriebsausschuss",
        "Ausschuss Gebäudewirtschaft",
        "Immobilienbeirat",
        "Betriebsausschuss Immobilien",
        "Rat der Stadt Lünen",
        "Ausschuss für Arbeitsmarkt",
        "Rechnungsprüfungsausschuss"
    ]
    
    # Relevante Committees aus der Spezifikation
    relevant_committees = [
        "Rat der Stadt Lünen",
        "Rechnungsprüfungsausschuss", 
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen",
        "Ausschuss für Arbeitsmarkt, Wirtschaftsförderung und Innovation"
    ]
    
    # Erweiterte Patterns
    additional_patterns = [
        'betriebsausschuss zentrale gebäudebewirtschaftung',
        'betriebsausschuss zentrale',
        'betriebsausschuss zgb',
        'zentrale gebäudebewirtschaftung',
        'gebäudebewirtschaftung lünen',
        'ausschuss für arbeitsmarkt',
        'arbeitsmarkt, wirtschaftsförderung',
        'rechnungsprüfungsausschuss'
    ]
    
    def is_relevant_committee(committee_name):
        committee_lower = committee_name.lower()
        
        # Check exact matches first
        for relevant in relevant_committees:
            if relevant.lower() in committee_lower:
                return True, f"exact match: '{relevant}'"
        
        # Check additional patterns
        for pattern in additional_patterns:
            if pattern in committee_lower:
                return True, f"pattern match: '{pattern}'"
        
        return False, "no match"
    
    print("\n📋 Committee filtering results:")
    for committee in test_committee_names:
        is_relevant, reason = is_relevant_committee(committee)
        status = "✅" if is_relevant else "❌"
        print(f"  {status} {committee}")
        if is_relevant:
            print(f"      → {reason}")
    
    # Spezial test für mögliche Variationen des gesuchten Meetings
    print(f"\n🎯 Special focus on Betriebsausschuss variations:")
    betriebsausschuss_variations = [
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen, 2. Sitzung",
        "2. Sitzung des Betriebsausschusses Zentrale Gebäudebewirtschaftung",
        "Betriebsausschuss ZGB Lünen - 2. Sitzung",
        "Sitzung Betriebsausschuss Zentrale Gebäudebewirtschaftung",
        "ZGB-Ausschuss Lünen"
    ]
    
    for variation in betriebsausschuss_variations:
        is_relevant, reason = is_relevant_committee(variation)
        status = "✅" if is_relevant else "❌"
        print(f"  {status} {variation}")
        if is_relevant:
            print(f"      → {reason}")

def main():
    print("🔍 Committee Filtering Test for Missing Meeting")
    print("=" * 55)
    
    test_committee_filtering_extended()
    
    print(f"\n📝 Analysis:")
    print("- If all Betriebsausschuss variations show ✅, the filtering should work")
    print("- If they show ❌, we need to adjust the patterns")
    print("- The meeting might be named differently than expected")
    print("- Or the meeting might not be in the system yet")

if __name__ == "__main__":
    main()