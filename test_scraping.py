#!/usr/bin/env python3
"""
Test script to verify website scraping functionality
"""

from datetime import datetime
from scraper import RatsInfoScraper
from pdf_processor import PDFProcessor
import requests

def test_website_accessibility():
    """Test if the Lünen website is accessible"""
    print("🌐 Testing website accessibility...")
    
    urls_to_test = [
        "https://luenen.ratsinfomanagement.net/termine/",
        "https://luenen.ratsinfomanagement.net/termine/?year=2024&month=07"
    ]
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    for url in urls_to_test:
        try:
            response = session.get(url, timeout=10)
            print(f"✅ {url} - Status: {response.status_code}")
            print(f"   Content length: {len(response.content)} bytes")
            
            # Check for common terms
            content = response.text.lower()
            terms_found = []
            for term in ['rat', 'ausschuss', 'sitzung', 'termin', 'kalender']:
                if term in content:
                    terms_found.append(term)
            
            print(f"   Found terms: {', '.join(terms_found)}")
            
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
        print()

def test_scraper():
    """Test the scraper functionality"""
    print("🔍 Testing scraper functionality...")
    
    scraper = RatsInfoScraper()
    
    # Test for current month
    now = datetime.now()
    print(f"Testing scraper for {now.month}/{now.year}...")
    
    try:
        meetings = scraper._scrape_month(now.year, now.month)
        print(f"✅ Found {len(meetings)} meetings")
        
        for i, meeting in enumerate(meetings[:3]):  # Show first 3
            print(f"   Meeting {i+1}:")
            print(f"     Title: {meeting.get('title', 'N/A')}")
            print(f"     Date: {meeting.get('date', 'N/A')}")
            print(f"     Committee: {meeting.get('committee', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"❌ Scraper error: {e}")

def test_committee_filtering():
    """Test committee filtering"""
    print("🎯 Testing committee filtering...")
    
    scraper = RatsInfoScraper()
    
    test_committees = [
        "Rat der Stadt Lünen",
        "Rechnungsprüfungsausschuss", 
        "Irrelevanter Ausschuss",
        "Betriebsausschuss Zentrale Gebäudebewirtschaftung Lünen"
    ]
    
    for committee in test_committees:
        is_relevant = scraper._is_relevant_committee(committee)
        status = "✅" if is_relevant else "❌"
        print(f"   {status} {committee}: {'relevant' if is_relevant else 'not relevant'}")

def test_pdf_processing():
    """Test PDF processing capabilities"""
    print("📄 Testing PDF processing...")
    
    processor = PDFProcessor()
    
    # Test with sample text
    sample_text = "Dies ist ein wichtiger Beschluss der Stadtverwaltung Lünen. Der Rat hat über verschiedene Angelegenheiten entschieden und wichtige Maßnahmen beschlossen."
    
    try:
        summary = processor.summarize_text(sample_text)
        print(f"✅ Text summarization works")
        print(f"   Original: {sample_text[:50]}...")
        print(f"   Summary: {summary[:50]}...")
        
    except Exception as e:
        print(f"❌ PDF processing error: {e}")

def main():
    print("🧪 Lünen Terminplaner - Functionality Test")
    print("=" * 50)
    
    test_website_accessibility()
    test_scraper()
    test_committee_filtering()
    test_pdf_processing()
    
    print("🏁 Test completed!")

if __name__ == "__main__":
    main()