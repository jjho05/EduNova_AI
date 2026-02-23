"""
Quiz Generation Service
AI-powered quiz and assessment generation
"""
import json
import logging
from typing import Dict, List, Optional
from ..config import settings
from .gemini_service import create_chat_session

logger = logging.getLogger(__name__)

def _construir_modificador_contextual(datos_perfil_usuario: Optional[Dict] = None) -> str:
    """
    Build contextual modifiers based on user profile
    Adapts quiz difficulty and style to user preferences
    """
    if not datos_perfil_usuario:
        return ""
    
    modificadores = []
    
    año_cursado = datos_perfil_usuario.get('año_cursado')
    objetivo = datos_perfil_usuario.get('objetivo_principal')
    autoevaluacion = datos_perfil_usuario.get('autoevaluacion')
    estilo_aprendizaje = datos_perfil_usuario.get('estilo_aprendizaje')
    
    if año_cursado:
        modificadores.append(f"El usuario está cursando {año_cursado}.")
    
    if objetivo == "Pasar un examen":
        modificadores.append("El problema debe tener un formato y tono similar a una pregunta de examen.")
    elif objetivo == "Aprender por curiosidad":
        modificadores.append("El problema puede ser más creativo o aplicado a un caso práctico.")
    
    if autoevaluacion == "Necesito mucha ayuda":
        modificadores.append("El problema debe ser de un nivel fundamental, ideal para un principiante.")
    elif autoevaluacion == "Soy bueno/a pero quiero mejorar":
        modificadores.append("El problema puede incluir un pequeño giro que requiera más atención.")
    
    if estilo_aprendizaje == "Paso a Paso y con Ejemplos Sencillos":
        modificadores.append("IMPORTANTE: La solución debe ser MUY detallada, paso a paso, con ejemplos claros.")
    elif estilo_aprendizaje == "Directo al Grano":
        modificadores.append("La solución debe ser concisa y directa.")
    
    return " ".join(modificadores)

def generar_quiz_nivelacion(chat_session=None) -> Dict:
    """
    Generate a leveling quiz to assess student's baseline knowledge
    
    Returns:
        Dict with quiz questions and answers
    """
    if chat_session is None:
        chat_session = create_chat_session()
    
    prompt = (
        "Actúa como un evaluador educativo. Genera un quiz de nivelación básico "
        "con 5 preguntas de opción múltiple. El JSON debe tener esta estructura: "
        '{"preguntas": [{"pregunta": "...", "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."], '
        '"respuesta_correcta": "A", "explicacion": "..."}]}. '
        "Solo devuelve el JSON, sin texto adicional."
    )
    
    try:
        response = chat_session.send_message(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        quiz_data = json.loads(json_text)
        return quiz_data
    except Exception as e:
        logger.error(f"Error generando quiz de nivelación: {e}")
        return {"preguntas": []}

def generar_quiz_tematico(tema: str, num_preguntas: int = 5, 
                          datos_perfil: Optional[Dict] = None,
                          chat_session=None) -> Dict:
    """
    Generate a quiz on a specific topic
    
    Args:
        tema: Topic to quiz on
        num_preguntas: Number of questions to generate
        datos_perfil: Optional user profile for personalization
        chat_session: Optional existing chat session
        
    Returns:
        Dict with quiz questions and answers
    """
    if chat_session is None:
        chat_session = create_chat_session()
    
    modificador = _construir_modificador_contextual(datos_perfil)
    
    prompt = (
        f"Actúa como un experto en evaluación educativa. Genera un quiz sobre '{tema}' con {num_preguntas} preguntas "
        f"de opción múltiple. {modificador} "
        "El JSON debe tener esta estructura: "
        '{"preguntas": [{"pregunta": "...", "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."], '
        '"respuesta_correcta": "A", "explicacion": "..."}]}. '
        "Solo devuelve el JSON, sin texto adicional."
    )
    
    try:
        response = chat_session.send_message(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        quiz_data = json.loads(json_text)
        return quiz_data
    except Exception as e:
        logger.error(f"Error generando quiz temático: {e}")
        return {"preguntas": []}

def generar_examen_modulo(modulo_titulo: str, subtemas: List[str],
                          datos_perfil: Optional[Dict] = None,
                          chat_session=None) -> Dict:
    """
    Generate a comprehensive exam for a module
    
    Args:
        modulo_titulo: Module title
        subtemas: List of subtopics to cover
        datos_perfil: Optional user profile for personalization
        chat_session: Optional existing chat session
        
    Returns:
        Dict with exam questions and answers
    """
    if chat_session is None:
        chat_session = create_chat_session()
    
    modificador = _construir_modificador_contextual(datos_perfil)
    subtemas_str = ", ".join(subtemas)
    
    prompt = (
        f"Actúa como un experto en diseño de evaluaciones. Genera un examen completo sobre el módulo '{modulo_titulo}' "
        f"que cubre los siguientes subtemas: {subtemas_str}. "
        f"{modificador} "
        "Genera 10 preguntas de opción múltiple que cubran todos los subtemas. "
        "El JSON debe tener esta estructura: "
        '{"preguntas": [{"pregunta": "...", "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."], '
        '"respuesta_correcta": "A", "explicacion": "...", "subtema": "..."}]}. '
        "Solo devuelve el JSON, sin texto adicional."
    )
    
    try:
        response = chat_session.send_message(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        quiz_data = json.loads(json_text)
        return quiz_data
    except Exception as e:
        logger.error(f"Error generando examen de módulo: {e}")
        return {"preguntas": []}
