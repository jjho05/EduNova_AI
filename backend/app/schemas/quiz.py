from pydantic import BaseModel
from typing import List, Optional

class QuizQuestion(BaseModel):
    pregunta: str
    opciones: List[str]
    respuesta_correcta: str
    explicacion: str
    subtema: Optional[str] = None

class QuizCreate(BaseModel):
    topic: str
    num_preguntas: int = 5

class QuizResponse(BaseModel):
    id: str
    user_id: str
    quiz_type: str
    topic: Optional[str]
    questions: List[dict]
    score: Optional[int]
    total_questions: int
    
    class Config:
        from_attributes = True
