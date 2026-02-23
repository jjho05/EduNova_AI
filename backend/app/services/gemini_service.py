"""
Gemini AI Integration Service
Provides AI-powered content generation for educational platform
"""
import json
import uuid
import time
import logging
import google.generativeai as genai
from google.api_core import exceptions
from ..config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Create model
model = genai.GenerativeModel('gemini-3-flash-preview')

# System instruction for educational context
SYSTEM_INSTRUCTION = """
Eres un asistente educativo inteligente y profesional. Tu objetivo es ayudar a estudiantes y profesores 
a crear y consumir contenido educativo de calidad. Siempre sé claro, conciso y pedagógico en tus respuestas.
Cuando generes contenido educativo, asegúrate de que sea preciso, bien estructurado y adaptado al nivel apropiado.
"""

def generate_with_retry(func, *args, max_retries=3, initial_delay=1, **kwargs):
    """Execute a function with exponential backoff retry logic"""
    delay = initial_delay
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except (exceptions.ResourceExhausted, exceptions.ServiceUnavailable, exceptions.GoogleAPIError) as e:
            last_exception = e
            logger.warning(f"Gemini API attempt {attempt + 1} failed: {str(e)}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        except Exception as e:
            # Don't retry on other errors (like bad request)
            logger.error(f"Gemini API non-retriable error: {str(e)}")
            raise e
            
    logger.error(f"Gemini API failed after {max_retries} attempts")
    if last_exception:
        raise last_exception
    raise Exception("Gemini API failed after all retry attempts")

def create_chat_session():
    """Create a new Gemini chat session with educational context"""
    try:
        chat = model.start_chat(history=[
            {'role': 'user', 'parts': [SYSTEM_INSTRUCTION]},
            {'role': 'model', 'parts': ['Entendido. Estoy listo para ayudar con contenido educativo de calidad.']}
        ])
        return chat
    except Exception as e:
        logger.error(f"Error creating chat session: {e}")
        return None

def generar_silabo_curso(tema_general: str, chat_session=None):
    """
    Generate a complete course syllabus for a given topic
    
    Args:
        tema_general: Main course topic
        chat_session: Optional existing chat session
        
    Returns:
        Dict with course structure including modules and subtopics
    """
    if chat_session is None:
        chat_session = create_chat_session()
        if not chat_session:
            return None
    
    prompt = (
        f"Actúa como un diseñador de cursos experto. Para el tema '{tema_general}', crea un sílabo detallado "
        "en formato JSON. El JSON debe tener una clave 'modulos', que es una lista de 3 a 5 módulos. "
        "Cada módulo debe tener un 'titulo' (string) y una lista de 'subtemas' (lista de strings). "
        "No incluyas introducciones, solo el JSON puro. Ejemplo de la estructura deseada: "
        '{"modulos": [{"titulo": "Módulo 1: ...", "subtemas": ["Subtema 1.1", "Subtema 1.2"]}]}'
    )
    
    def _generate():
        response = chat_session.send_message(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_text)

    try:
        silabo = generate_with_retry(_generate)

        curso_completo = {
            "id_curso": f"curso_{uuid.uuid4().hex[:8]}",
            "tema_general": tema_general,
            "progreso_general": 0.0,
            "calificacion_promedio": None,
            "modulos": []
        }
        
        for modulo_data in silabo.get("modulos", []):
            curso_completo["modulos"].append({
                "id_modulo": f"mod_{uuid.uuid4().hex[:6]}",
                "titulo": modulo_data.get("titulo", "Sin título"),
                "subtemas": modulo_data.get("subtemas", []),
                "completado": False,
                "calificacion_examen": None,
                "teoria_generada": {}
            })
        
        return curso_completo
    except Exception as e:
        logger.error(f"Error generando sílabo del curso: {e}")
        return None

def generar_teoria_subtema(subtema: str, chat_session=None):
    """
    Generate educational content for a specific subtopic
    
    Args:
        subtema: The subtopic to explain
        chat_session: Optional existing chat session
        
    Returns:
        String with the generated educational content
    """
    if chat_session is None:
        chat_session = create_chat_session()
        if not chat_session:
            return "Error de conexión con el servicio de IA."
    
    prompt = (
        "Actúa como un profesor experto. Explica el siguiente concepto: "
        f"'{subtema}'. Proporciona la teoría fundamental, cualquier fórmula clave y un ejemplo simple resuelto. "
        "Usa un lenguaje claro y pedagógico."
    )
    
    def _generate():
        response = chat_session.send_message(prompt)
        return response.text.strip()
    
    try:
        return generate_with_retry(_generate)
    except Exception as e:
        logger.error(f"Error generando teoría del subtema: {e}")
        return "No se pudo generar la teoría para este subtema debido a un error temporal."
