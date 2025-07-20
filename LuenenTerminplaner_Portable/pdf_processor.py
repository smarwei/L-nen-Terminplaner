import os
import requests
try:
    import fitz
    FITZ_AVAILABLE = True
    PDF_LIB = 'fitz'
except ImportError:
    try:
        import pdfplumber
        FITZ_AVAILABLE = False
        PDFPLUMBER_AVAILABLE = True
        PDF_LIB = 'pdfplumber'
    except ImportError:
        FITZ_AVAILABLE = False
        PDFPLUMBER_AVAILABLE = False
        PDF_LIB = None
        print("Warning: No PDF library available. PDF processing will be limited.")

from urllib.parse import urlparse
from pathlib import Path
import hashlib

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer

import re

class PDFProcessor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.stemmer = Stemmer("german")
        self.summarizer = LsaSummarizer(self.stemmer)
        self.summarizer.stop_words = self._get_german_stopwords()
    
    def download_pdf(self, pdf_url, download_folder):
        if not pdf_url:
            return None
            
        try:
            response = self.session.get(pdf_url, stream=True)
            response.raise_for_status()
            
            url_hash = hashlib.md5(pdf_url.encode()).hexdigest()[:8]
            filename = f"document_{url_hash}.pdf"
            filepath = os.path.join(download_folder, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return filepath
            
        except Exception as e:
            print(f"Fehler beim Download der PDF {pdf_url}: {e}")
            return None
    
    def extract_text(self, pdf_path):
        if not pdf_path or not os.path.exists(pdf_path):
            return ""
        
        if PDF_LIB == 'fitz':
            return self._extract_text_fitz(pdf_path)
        elif PDF_LIB == 'pdfplumber':
            return self._extract_text_pdfplumber(pdf_path)
        else:
            print("No PDF library available for text extraction")
            return ""
    
    def _extract_text_fitz(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            
            doc.close()
            
            text = self._clean_text(text)
            return text
            
        except Exception as e:
            print(f"Fehler beim Extrahieren des Textes aus {pdf_path}: {e}")
            return ""
    
    def _extract_text_pdfplumber(self, pdf_path):
        try:
            import pdfplumber
            text = ""
            
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            text = self._clean_text(text)
            return text
            
        except Exception as e:
            print(f"Fehler beim Extrahieren des Textes aus {pdf_path}: {e}")
            return ""
    
    def _clean_text(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\säöüÄÖÜß.,!?;:()\-]', '', text)
        text = text.strip()
        return text
    
    def summarize_text(self, text, sentence_count=3):
        if not text or len(text.strip()) < 100:
            return "Zu wenig Text für eine Zusammenfassung verfügbar."
        
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("german"))
            summary = self.summarizer(parser.document, sentence_count)
            
            summary_text = " ".join([str(sentence) for sentence in summary])
            
            if not summary_text.strip():
                return "Zusammenfassung konnte nicht erstellt werden."
            
            return summary_text
            
        except Exception as e:
            print(f"Fehler bei der Zusammenfassung: {e}")
            return f"Fehler bei der Zusammenfassung: {str(e)}"
    
    def _get_german_stopwords(self):
        return {
            'aber', 'alle', 'allem', 'allen', 'aller', 'alles', 'als', 'also', 'am', 'an', 
            'ander', 'andere', 'anderem', 'anderen', 'anderer', 'anderes', 'anderm', 'andern', 
            'anders', 'auch', 'auf', 'aus', 'bei', 'bin', 'bis', 'bist', 'da', 'damit', 
            'dann', 'der', 'den', 'des', 'dem', 'die', 'das', 'dass', 'daß', 'du', 'er', 
            'eine', 'ein', 'einem', 'einen', 'einer', 'eines', 'für', 'hatte', 'habe', 
            'haben', 'hat', 'hier', 'ich', 'ihm', 'ihn', 'ihnen', 'ihr', 'ihre', 'im', 
            'in', 'ist', 'kann', 'mich', 'mir', 'mit', 'nach', 'nicht', 'noch', 'nur', 
            'oder', 'sie', 'sind', 'so', 'über', 'um', 'und', 'uns', 'unse', 'unser', 
            'unses', 'von', 'vor', 'war', 'waren', 'wir', 'wird', 'zu', 'zum', 'zur'
        }