"""
Syllabus Processor - Complete processing to create modules
"""
from sqlalchemy.orm import Session
from typing import Dict, List
from uuid import uuid4
import os

from .document_processor import DocumentProcessor
from ..models.course import Course
from ..models.module import Module


class SyllabusProcessor:
    """Process syllabus documents and create course modules"""
    
    def __init__(self, db: Session):
        self.db = db
        self.doc_processor = DocumentProcessor()
    
    async def process_syllabus_complete(
        self,
        file_path: str,
        course_id: str
    ) -> Dict:
        """
        Process syllabus and create all modules/units automatically
        
        Args:
            file_path: Path to syllabus PDF
            course_id: Course ID to attach modules to
            
        Returns:
            Dict with success status and created modules
        """
        # 1. Extract and analyze syllabus
        result = await self.doc_processor.process_document(file_path, "syllabus")
        
        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error"),
                "modules_created": 0
            }
        
        # 2. Get course
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return {
                "success": False,
                "error": "Course not found",
                "modules_created": 0
            }
        
        # 3. Extract units from result
        units = result.get("units", [])
        
        if not units:
            return {
                "success": False,
                "error": "No units found in syllabus",
                "modules_created": 0
            }
        
        # 4. Create modules
        created_modules = []
        
        for idx, unit in enumerate(units):
            try:
                module = Module(
                    id=str(uuid4()),
                    course_id=course_id,
                    title=f"Unidad {unit.get('number', idx+1)}: {unit.get('title', 'Sin título')}",
                    order_index=idx,
                    content=self._build_module_content(unit),
                    hours=unit.get('hours', 0),
                    topics=unit.get('topics', [])
                )
                
                self.db.add(module)
                created_modules.append(module)
                
            except Exception as e:
                print(f"Error creating module {idx}: {e}")
                continue
        
        self.db.commit()
        
        # 5. Update course description with objectives and competencies
        if result.get("objectives"):
            course.description = f"{course.description or ''}\n\nObjetivos:\n" + \
                "\n".join(f"- {obj}" for obj in result["objectives"])
        
        self.db.commit()
        
        return {
            "success": True,
            "modules_created": len(created_modules),
            "total_units": len(units),
            "course_updated": True,
            "modules": [
                {
                    "id": m.id,
                    "title": m.title,
                    "order": m.order_index
                }
                for m in created_modules
            ]
        }
    
    def _build_module_content(self, unit: Dict) -> str:
        """
        Build formatted content for a module from unit data
        """
        content_parts = []
        
        # Title and hours
        content_parts.append(f"# {unit.get('title', 'Unidad')}")
        content_parts.append(f"\n**Horas:** {unit.get('hours', 'N/A')}\n")
        
        # Topics
        if unit.get('topics'):
            content_parts.append("## Temas")
            for topic in unit['topics']:
                content_parts.append(f"- {topic}")
                
                # Subtopics if available
                if unit.get('subtopics', {}).get(topic):
                    for subtopic in unit['subtopics'][topic]:
                        content_parts.append(f"  - {subtopic}")
            content_parts.append("")
        
        # Competencies
        if unit.get('competencies'):
            content_parts.append("## Competencias")
            for comp in unit['competencies']:
                content_parts.append(f"- {comp}")
            content_parts.append("")
        
        # Learning objectives
        if unit.get('objectives'):
            content_parts.append("## Objetivos de Aprendizaje")
            for obj in unit['objectives']:
                content_parts.append(f"- {obj}")
            content_parts.append("")
        
        return "\n".join(content_parts)
