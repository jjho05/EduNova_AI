"""
Curriculum processing service
Processes curriculum documents and creates courses automatically
"""
import google.generativeai as genai
from sqlalchemy.orm import Session
from typing import Dict, List
from uuid import uuid4
import os
import logging
from .pdf_extractor import PDFExtractor
from ..models.course import Course
from ..models.user import User
from ..config import settings

logger = logging.getLogger(__name__)

class CurriculumProcessor:
    """Process curriculum/retícula documents and create courses"""
    
    def __init__(self, db: Session):
        self.db = db
        # Use settings
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        genai.configure(api_key=api_key)
        # Use consistent model
        self.model = genai.GenerativeModel('gemini-3.5-flash')
        self.pdf_extractor = PDFExtractor()
    
    async def process_curriculum(
        self,
        file_path: str,
        user_id: str,
        curriculum_name: str
    ) -> Dict:
        """
        Process curriculum PDF and create courses automatically.
        
        Returns:
            Dict with success status, courses created, and any errors
        """
        # 1. Extract text from PDF
        text = self.pdf_extractor.extract_text(file_path)
        
        if not text:
            return {
                "success": False,
                "error": "No se pudo extraer texto del PDF",
                "courses_created": 0
            }
        
        # 2. Analyze with Gemini
        structure = await self._analyze_curriculum(text)
        
        if not structure.get("courses"):
            return {
                "success": False,
                "error": "No se encontraron materias en el documento",
                "courses_created": 0
            }
        
        # 3. Create courses in database
        created_courses = []
        for course_data in structure["courses"]:
            try:
                course = Course(
                    id=str(uuid4()),
                    user_id=user_id,
                    title=f"{course_data.get('code', '')} - {course_data.get('name', 'Sin nombre')}".strip(' -'),
                    description=f"Semestre {course_data.get('semester', 'N/A')} | {course_data.get('credits', 0)} créditos",
                    overall_progress=0.0
                )
                
                self.db.add(course)
                created_courses.append(course)
            except Exception as e:
                logger.error(f"Error creating course {course_data.get('name')}: {e}")
                continue
        
        self.db.commit()
        
        return {
            "success": True,
            "courses_created": len(created_courses),
            "total_found": len(structure["courses"]),
            "institution": structure.get("institution", ""),
            "program": structure.get("program", ""),
            "courses": [
                {
                    "id": c.id,
                    "title": c.title,
                    "description": c.description
                }
                for c in created_courses
            ]
        }
    
    async def _analyze_curriculum(self, text: str) -> Dict:
        """Analyze curriculum text with Gemini"""
        prompt = f"""
Analiza este documento curricular y extrae TODAS las materias.

DOCUMENTO:
{text}

Devuelve SOLO JSON válido con esta estructura exacta:
{{
  "institution": "nombre de la institución",
  "program": "nombre del programa (ej: Ingeniería en Sistemas)",
  "total_semesters": 8,
  "courses": [
    {{
      "code": "COD-123",
      "name": "Nombre Materia",
      "semester": 1,
      "credits": 5,
      "hours_theory": 2,
      "hours_practice": 3,
      "prerequisites": []
    }}
  ]
}}

IMPORTANTE:
- Extrae TODAS las materias que encuentres
- Si no encuentras un dato, usa valores por defecto razonables
- El código debe ser único para cada materia
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean JSON
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            result_text = result_text.strip()
            
            import json
            return json.loads(result_text)
        except Exception as e:
            logger.error(f"Error analyzing curriculum: {e}")
            return {"courses": []}
