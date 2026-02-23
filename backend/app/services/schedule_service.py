"""
Schedule and Rubric Generation Service
"""
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .gemini_service import create_chat_session

logger = logging.getLogger(__name__)

def generar_cronograma(
    course_title: str,
    modules: List[str],
    start_date: str,
    end_date: str,
    hours_per_week: int = 4,
    chat_session=None
) -> Dict:
    """
    Genera un cronograma detallado para un curso
    """
    if chat_session is None:
        chat_session = create_chat_session()
    
    modules_str = ", ".join(modules)
    
    prompt = (
        f"Actúa como un planificador educativo experto. Genera un cronograma detallado para el curso '{course_title}' "
        f"que cubre los siguientes módulos: {modules_str}. "
        f"Fecha de inicio: {start_date}, Fecha de fin: {end_date}. "
        f"Horas por semana: {hours_per_week}. "
        "El cronograma debe incluir: "
        "1. Distribución de temas por semana "
        "2. Actividades sugeridas "
        "3. Evaluaciones programadas "
        "4. Fechas de entrega "
        "Devuelve ÚNICAMENTE un JSON con esta estructura: "
        '{"semanas": [{"numero": 1, "fecha_inicio": "YYYY-MM-DD", "fecha_fin": "YYYY-MM-DD", '
        '"temas": ["tema1", "tema2"], "actividades": ["act1"], "evaluacion": "tipo o null"}]} '
        "Solo JSON, sin texto adicional."
    )
    
    try:
        response = chat_session.send_message(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        cronograma = json.loads(json_text)
        return cronograma
    except Exception as e:
        logger.error(f"Error generando cronograma: {e}")
        return {"semanas": []}

def generar_rubrica(
    activity_name: str,
    activity_type: str,
    criteria: Optional[List[str]] = None,
    max_score: int = 100,
    chat_session=None
) -> Dict:
    """
    Genera una rúbrica de evaluación para una actividad
    """
    if chat_session is None:
        chat_session = create_chat_session()
    
    criteria_str = ", ".join(criteria) if criteria else "criterios estándar de calidad"
    
    prompt = (
        f"Actúa como un evaluador educativo experto. Genera una rúbrica de evaluación detallada "
        f"para la actividad '{activity_name}' de tipo '{activity_type}'. "
        f"Criterios a evaluar: {criteria_str}. "
        f"Puntuación máxima: {max_score}. "
        "La rúbrica debe tener 4 niveles: Excelente, Bueno, Suficiente, Insuficiente. "
        "Devuelve ÚNICAMENTE un JSON con esta estructura: "
        '{"criterios": [{"nombre": "Criterio 1", "peso": 25, "niveles": {'
        '"excelente": {"puntos": 25, "descripcion": "..."}, '
        '"bueno": {"puntos": 20, "descripcion": "..."}, '
        '"suficiente": {"puntos": 15, "descripcion": "..."}, '
        '"insuficiente": {"puntos": 0, "descripcion": "..."}}}]} '
        "Solo JSON, sin texto adicional."
    )
    
    try:
        response = chat_session.send_message(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        rubrica = json.loads(json_text)
        return rubrica
    except Exception as e:
        logger.error(f"Error generando rúbrica: {e}")
        return {"criterios": []}

def generar_syllabus_completo(
    course_title: str,
    description: str,
    objectives: Optional[List[str]] = None,
    chat_session=None
) -> Dict:
    """
    Genera un sílabo completo y detallado para un curso
    """
    if chat_session is None:
        chat_session = create_chat_session()
    
    objectives_str = ", ".join(objectives) if objectives else "objetivos generales del tema"
    
    prompt = (
        f"Actúa como un diseñador curricular experto. Genera un sílabo completo y profesional "
        f"para el curso '{course_title}'. Descripción: {description}. "
        f"Objetivos: {objectives_str}. "
        "El sílabo debe incluir: "
        "1. Objetivos generales y específicos "
        "2. Competencias a desarrollar "
        "3. Módulos con temas detallados "
        "4. Metodología de enseñanza "
        "5. Criterios de evaluación "
        "6. Bibliografía recomendada "
        "Devuelve ÚNICAMENTE un JSON con esta estructura: "
        '{"objetivos_generales": ["obj1"], "objetivos_especificos": ["obj1"], '
        '"competencias": ["comp1"], "modulos": [{"titulo": "Mod 1", "temas": ["tema1"], "horas": 8}], '
        '"metodologia": "descripción", "evaluacion": {"criterios": ["crit1"], "porcentajes": [30, 70]}, '
        '"bibliografia": [{"titulo": "Libro 1", "autor": "Autor", "año": 2023}]} '
        "Solo JSON, sin texto adicional."
    )
    
    try:
        response = chat_session.send_message(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        syllabus = json.loads(json_text)
        return syllabus
    except Exception as e:
        logger.error(f"Error generando sílabo completo: {e}")
        return {
            "objetivos_generales": [],
            "objetivos_especificos": [],
            "competencias": [],
            "modulos": [],
            "metodologia": "",
            "evaluacion": {},
            "bibliografia": []
        }
