"""
Gemini Vision Service - Process scanned PDFs with OCR
"""
import google.generativeai as genai
from pdf2image import convert_from_path
from PIL import Image
import os
import logging
from typing import List, Dict
import tempfile
from ..config import settings

logger = logging.getLogger(__name__)

class GeminiVisionService:
    """Process images and scanned PDFs with Gemini Vision"""
    
    def __init__(self):
        # Use settings instead of os.getenv
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        genai.configure(api_key=api_key)
        # Use the correct vision model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def process_scanned_pdf(self, pdf_path: str) -> str:
        """
        Convert scanned PDF to images and extract text with OCR
        
        Args:
            pdf_path: Path to scanned PDF
            
        Returns:
            Extracted text from all pages
        """
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300)
            
            all_text = []
            
            # Process each page
            for i, image in enumerate(images):
                logger.info(f"Processing page {i+1}/{len(images)}...")
                
                # Save image temporarily
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    image.save(tmp.name, 'PNG')
                    tmp_path = tmp.name
                
                try:
                    # Extract text from image
                    page_text = self._extract_text_from_image(tmp_path)
                    all_text.append(f"--- Página {i+1} ---\n{page_text}\n")
                finally:
                    # Clean up temp file
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
            
            return "\n".join(all_text)
            
        except Exception as e:
            logger.error(f"Error processing scanned PDF: {e}")
            return ""
    
    def _extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from a single image using Gemini Vision
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Create prompt for OCR
            prompt = """
Extract all text from this image exactly as it appears.
Maintain the original formatting, structure, and layout as much as possible.
If there are tables, preserve the table structure.
If there are lists, preserve the list format.
Return only the extracted text, no additional commentary.
"""
            
            # Generate content with vision model
            response = self.model.generate_content([prompt, image])
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return ""
    
    def analyze_document_structure(self, image_path: str) -> Dict:
        """
        Analyze document structure (headings, sections, etc.)
        """
        try:
            image = Image.open(image_path)
            
            prompt = """
Analyze this document image and identify its structure.
Return a JSON with:
{
  "document_type": "curriculum/syllabus/textbook/other",
  "has_tables": true/false,
  "has_images": true/false,
  "main_sections": ["section1", "section2"],
  "language": "es/en"
}
"""
            
            response = self.model.generate_content([prompt, image])
            
            # Parse JSON response
            import json
            result_text = response.text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            return json.loads(result_text.strip())
            
        except Exception as e:
            logger.error(f"Error analyzing document structure: {e}")
            return {}
    
    def extract_table_from_image(self, image_path: str) -> List[List[str]]:
        """
        Extract table data from image
        """
        try:
            image = Image.open(image_path)
            
            prompt = """
Extract the table from this image and return it as JSON array of arrays.
Each row should be an array of cell values.
Example: [["Header1", "Header2"], ["Value1", "Value2"]]
Return only the JSON, no additional text.
"""
            
            response = self.model.generate_content([prompt, image])
            
            import json
            result_text = response.text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            return json.loads(result_text.strip())
            
        except Exception as e:
            logger.error(f"Error extracting table: {e}")
            return []
