"""
PDF text extraction service
"""
from PyPDF2 import PdfReader
from typing import Optional
import os


class PDFExtractor:
    """Extract text from PDF files"""
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract all text from a PDF file.
        Returns empty string if extraction fails.
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_metadata(self, file_path: str) -> dict:
        """Extract PDF metadata"""
        try:
            reader = PdfReader(file_path)
            metadata = reader.metadata
            
            return {
                "title": metadata.get("/Title", ""),
                "author": metadata.get("/Author", ""),
                "subject": metadata.get("/Subject", ""),
                "creator": metadata.get("/Creator", ""),
                "producer": metadata.get("/Producer", ""),
                "num_pages": len(reader.pages)
            }
        except Exception as e:
            print(f"Error extracting PDF metadata: {e}")
            return {"num_pages": 0}
    
    def is_scanned_pdf(self, file_path: str) -> bool:
        """
        Detect if PDF is scanned (image-based).
        Returns True if text extraction yields very little text.
        """
        text = self.extract_text(file_path)
        metadata = self.extract_metadata(file_path)
        
        # If we got very little text relative to number of pages, likely scanned
        num_pages = metadata.get("num_pages", 1)
        chars_per_page = len(text) / num_pages if num_pages > 0 else 0
        
        # Threshold: less than 100 characters per page suggests scanned PDF
        return chars_per_page < 100
