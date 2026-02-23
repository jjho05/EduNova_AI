from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from ..database import get_db
from ..models.user import User
from ..models.quiz import Quiz
from ..schemas.quiz import QuizCreate, QuizResponse
from ..services.auth import get_current_user
from ..services.quiz_service import generar_quiz_tematico, generar_quiz_nivelacion

router = APIRouter()

@router.post("/topic", response_model=QuizResponse)
def generate_topic_quiz(
    quiz_data: QuizCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a quiz on a specific topic"""
    # Generate quiz with Gemini
    quiz_content = generar_quiz_tematico(
        tema=quiz_data.topic,
        num_preguntas=quiz_data.num_preguntas
    )
    
    if not quiz_content or not quiz_content.get('preguntas'):
        raise HTTPException(status_code=500, detail="Error generating quiz")
    
    # Save quiz to database
    new_quiz = Quiz(
        id=str(uuid4()),
        user_id=current_user.id,
        quiz_type='topic',
        topic=quiz_data.topic,
        questions=quiz_content,
        total_questions=len(quiz_content.get('preguntas', []))
    )
    
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    
    return new_quiz

@router.post("/leveling", response_model=QuizResponse)
def generate_leveling_quiz(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a leveling quiz"""
    # Generate quiz with Gemini
    quiz_content = generar_quiz_nivelacion()
    
    if not quiz_content or not quiz_content.get('preguntas'):
        raise HTTPException(status_code=500, detail="Error generating quiz")
    
    # Save quiz to database
    new_quiz = Quiz(
        id=str(uuid4()),
        user_id=current_user.id,
        quiz_type='leveling',
        questions=quiz_content,
        total_questions=len(quiz_content.get('preguntas', []))
    )
    
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    
    return new_quiz

@router.get("/", response_model=list[QuizResponse])
def get_user_quizzes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all quizzes for current user"""
    quizzes = db.query(Quiz).filter(Quiz.user_id == current_user.id).all()
    return quizzes
