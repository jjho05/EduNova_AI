"""
AI Context Manager - Build and cache context for better AI responses
"""
from typing import Dict, List, Optional
import json
import os
from datetime import datetime, timedelta


class AIContextManager:
    """
    Manage context for AI interactions
    Builds comprehensive context from course data
    """
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def build_course_context(self, course_data: Dict) -> str:
        """
        Build comprehensive context for a course
        
        Args:
            course_data: Dict with course info, modules, etc.
            
        Returns:
            Formatted context string for AI
        """
        context_parts = []
        
        # Course info
        context_parts.append(f"CURSO: {course_data.get('title', 'Sin título')}")
        context_parts.append(f"DESCRIPCIÓN: {course_data.get('description', 'N/A')}")
        context_parts.append("")
        
        # Modules
        if course_data.get('modules'):
            context_parts.append("MÓDULOS:")
            for module in course_data['modules']:
                context_parts.append(f"\n- {module.get('title', 'Sin título')}")
                if module.get('topics'):
                    for topic in module['topics']:
                        context_parts.append(f"  • {topic}")
            context_parts.append("")
        
        # Competencies
        if course_data.get('competencies'):
            context_parts.append("COMPETENCIAS:")
            for comp in course_data['competencies']:
                context_parts.append(f"- {comp}")
            context_parts.append("")
        
        # Objectives
        if course_data.get('objectives'):
            context_parts.append("OBJETIVOS:")
            for obj in course_data['objectives']:
                context_parts.append(f"- {obj}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def build_quiz_context(self, course_context: str, topic: str, difficulty: str) -> str:
        """
        Build context for quiz generation
        """
        prompt = f"""
Eres un profesor experto creando un examen.

CONTEXTO DEL CURSO:
{course_context}

TEMA DEL EXAMEN: {topic}
DIFICULTAD: {difficulty}

Genera preguntas que:
1. Estén alineadas con las competencias del curso
2. Cubran los temas relevantes
3. Sean del nivel de dificultad solicitado
4. Incluyan explicaciones claras
"""
        return prompt
    
    def build_content_generation_context(
        self,
        course_context: str,
        module_title: str,
        topics: List[str]
    ) -> str:
        """
        Build context for content generation
        """
        prompt = f"""
Eres un profesor experto creando material educativo.

CONTEXTO DEL CURSO:
{course_context}

MÓDULO: {module_title}
TEMAS A CUBRIR:
{chr(10).join(f'- {t}' for t in topics)}

Genera contenido educativo que:
1. Esté alineado con los objetivos del curso
2. Cubra todos los temas listados
3. Incluya ejemplos prácticos
4. Sea claro y estructurado
"""
        return prompt
    
    def cache_context(self, key: str, context: str, ttl_hours: int = 24):
        """
        Cache context to avoid rebuilding
        
        Args:
            key: Unique identifier
            context: Context string
            ttl_hours: Time to live in hours
        """
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        
        cache_data = {
            "context": context,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(hours=ttl_hours)).isoformat()
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    def get_cached_context(self, key: str) -> Optional[str]:
        """
        Get cached context if not expired
        
        Args:
            key: Unique identifier
            
        Returns:
            Cached context or None if expired/not found
        """
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if expired
            expires_at = datetime.fromisoformat(cache_data['expires_at'])
            if datetime.utcnow() > expires_at:
                # Delete expired cache
                os.remove(cache_file)
                return None
            
            return cache_data['context']
            
        except Exception as e:
            print(f"Error reading cache: {e}")
            return None
    
    def invalidate_cache(self, key: str):
        """
        Invalidate cached context
        """
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_file):
            os.remove(cache_file)
    
    def clear_all_cache(self):
        """
        Clear all cached contexts
        """
        for file in os.listdir(self.cache_dir):
            if file.endswith('.json'):
                os.remove(os.path.join(self.cache_dir, file))
