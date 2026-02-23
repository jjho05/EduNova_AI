"""
Document processing service with AI
Processes PDFs and extracts educational content
"""
import google.generativeai as genai
from typing import Dict, Optional
import os
import json

from .pdf_extractor import PDFExtractor


class DocumentProcessor:
    """Process educational documents with Gemini AI"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.pdf_extractor = PDFExtractor()
    
    async def process_document(self, file_path: str, document_type: str = "general") -> Dict:
        """
        Process a document and extract structured information.
        
        Args:
            file_path: Path to the document
            document_type: Type of document (curriculum, syllabus, reference, etc.)
        
        Returns:
            Dict with extracted information
        """
        # Extract text from PDF
        text = self.pdf_extractor.extract_text(file_path)
        
        if not text:
            return {
                "success": False,
                "error": "No se pudo extraer texto del documento",
                "extracted_text": ""
            }
        
        # Process based on document type
        if document_type == "curriculum":
            return await self._process_curriculum(text)
        elif document_type == "syllabus":
            return await self._process_syllabus(text)
        else:
            return await self._process_general(text)
    
    async def _process_general(self, text: str) -> Dict:
        """Process general educational document"""
        prompt = f"""
Analiza este documento educativo y extrae la información clave.

DOCUMENTO:
{text[:10000]}  # Limit to first 10k chars

Devuelve un resumen estructurado en formato JSON:
{{
  "title": "título del documento",
  "summary": "resumen breve",
  "key_topics": ["tema1", "tema2", "tema3"],
  "educational_level": "nivel educativo (si se puede determinar)",
  "language": "idioma"
}}
"""
        try:
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            result["success"] = True
            result["extracted_text"] = text
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "extracted_text": text
            }
    
    async def _process_curriculum(self, text: str) -> Dict:
        """Process curriculum/retícula document"""
        prompt = f"""
Analiza esta retícula educativa y extrae TODAS las materias.

RETÍCULA:
{text}

Devuelve SOLO JSON válido con esta estructura:
{{
  "institution": "nombre de la institución",
  "program": "nombre del programa",
  "total_semesters": 8,
  "courses": [
    {{
      "code": "SCD-1008",
      "name": "Fundamentos de Programación",
      "semester": 1,
      "credits": 5,
      "hours_theory": 2,
      "hours_practice": 3,
      "prerequisites": []
    }}
  ]
}}

IMPORTANTE: Extrae TODAS las materias que encuentres.
"""
        try:
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            result["success"] = True
            result["extracted_text"] = text
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "extracted_text": text
            }
    
    async def _process_syllabus(self, text: str) -> Dict:
        """Process course syllabus document"""
        prompt = f"""
Analiza este programa de materia (syllabus) y extrae la información estructurada.

PROGRAMA:
{text}

Devuelve JSON:
{{
  "course_name": "nombre de la materia",
  "course_code": "código (si existe)",
  "objectives": ["objetivo1", "objetivo2"],
  "competencies": ["competencia1", "competencia2"],
  "units": [
    {{
      "number": 1,
      "title": "Introducción",
      "hours": 10,
      "topics": ["tema1", "tema2"],
      "subtopics": {{
        "tema1": ["subtema1.1", "subtema1.2"]
      }}
    }}
  ],
  "evaluation": {{
    "exams": 40,
    "homework": 30,
    "participation": 10,
    "project": 20
  }},
  "bibliography": ["libro1", "libro2"]
}}
"""
        try:
            response = self.model.generate_content(prompt)
            result = self._parse_json_response(response.text)
            result["success"] = True
            result["extracted_text"] = text
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "extracted_text": text
            }
    
    def _parse_json_response(self, response_text: str) -> Dict:
        """Parse JSON from Gemini response"""
        # Remove markdown code blocks if present
        cleaned = response_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return error
            return {
                "error": f"Error parsing JSON: {str(e)}",
                "raw_response": response_text
            }
