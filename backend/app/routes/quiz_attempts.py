"""
Quiz Attempt routes - Student quiz taking and submission
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

from ..database import get_db
from ..models.user import User
from ..models.quiz import Quiz
from ..models.quiz_attempt import QuizAttempt, AttemptStatus
from ..models.enrollment import Enrollment
from ..auth import get_current_user
from ..schemas.statistics import QuizAttemptCreate, QuizAttemptResponse
from ..services.statistics_service import StatisticsService

router = APIRouter()


@router.post("/quizzes/{quiz_id}/start")
async def start_quiz(
    quiz_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Start a quiz attempt
    """
    # Check if quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Check if student is enrolled (if quiz has a course)
    if quiz.course_id:
        enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == current_user.id,
            Enrollment.course_id == quiz.course_id,
            Enrollment.status == "active"
        ).first()
        
        if not enrollment:
            raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    # Check if already has an in-progress attempt
    existing = db.query(QuizAttempt).filter(
        QuizAttempt.quiz_id == quiz_id,
        QuizAttempt.student_id == current_user.id,
        QuizAttempt.status == AttemptStatus.IN_PROGRESS
    ).first()
    
    if existing:
        return {
            "attempt_id": existing.id,
            "quiz_id": quiz_id,
            "questions": quiz.questions,
            "total_questions": len(quiz.questions),
            "started_at": existing.started_at,
            "message": "Resuming existing attempt"
        }
    
    # Create new attempt
    attempt = QuizAttempt(
        id=str(uuid4()),
        quiz_id=quiz_id,
        student_id=current_user.id,
        answers={},
        total_questions=len(quiz.questions),
        status=AttemptStatus.IN_PROGRESS
    )
    
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    return {
        "attempt_id": attempt.id,
        "quiz_id": quiz_id,
        "questions": quiz.questions,
        "total_questions": len(quiz.questions),
        "started_at": attempt.started_at
    }


@router.post("/quiz-attempts/{attempt_id}/submit")
async def submit_quiz(
    attempt_id: str,
    answers: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit quiz answers and calculate score
    """
    # Get attempt
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id,
        QuizAttempt.student_id == current_user.id
    ).first()
    
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    if attempt.status != AttemptStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Quiz already submitted")
    
    # Get quiz
    quiz = db.query(Quiz).filter(Quiz.id == attempt.quiz_id).first()
    
    # Calculate score
    correct_count = 0
    total_questions = len(quiz.questions)
    
    for idx, question in enumerate(quiz.questions):
        correct_answer_idx = question.get('correctAnswer')
        student_answer = answers.get(str(idx))
        
        if student_answer and correct_answer_idx is not None:
            options = question.get('options', [])
            if correct_answer_idx < len(options):
                correct_answer = options[correct_answer_idx]
                if student_answer == correct_answer:
                    correct_count += 1
    
    score = (correct_count / total_questions * 100) if total_questions > 0 else 0
    passed = score >= 60  # 60% to pass
    
    # Calculate time taken
    time_taken = int((datetime.utcnow() - attempt.started_at).total_seconds())
    
    # Update attempt
    attempt.answers = answers
    attempt.score = score
    attempt.correct_answers = correct_count
    attempt.passed = passed
    attempt.submitted_at = datetime.utcnow()
    attempt.time_taken = time_taken
    attempt.status = AttemptStatus.SUBMITTED
    
    db.commit()
    
    # Update statistics
    stats_service = StatisticsService(db)
    stats_service.update_question_statistics(quiz.id)
    
    # Update enrollment grade if applicable
    if quiz.course_id:
        enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == current_user.id,
            Enrollment.course_id == quiz.course_id
        ).first()
        
        if enrollment:
            # Recalculate average grade
            all_attempts = db.query(QuizAttempt).join(Quiz).filter(
                QuizAttempt.student_id == current_user.id,
                Quiz.course_id == quiz.course_id,
                QuizAttempt.status == AttemptStatus.SUBMITTED
            ).all()
            
            if all_attempts:
                avg_grade = sum(a.score for a in all_attempts) / len(all_attempts)
                enrollment.current_grade = avg_grade
                enrollment.last_activity_at = datetime.utcnow()
                db.commit()
    
    return {
        "attempt_id": attempt.id,
        "score": score,
        "correct_answers": correct_count,
        "total_questions": total_questions,
        "passed": passed,
        "time_taken": time_taken,
        "message": "¡Aprobado!" if passed else "No aprobado"
    }


@router.get("/quiz-attempts/{attempt_id}")
async def get_attempt(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get quiz attempt details
    """
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id
    ).first()
    
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    # Students can only see their own attempts
    # Teachers can see all attempts
    if current_user.role == "student" and attempt.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return attempt


@router.get("/my-quiz-attempts")
async def get_my_attempts(
    course_id: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all quiz attempts for current student
    """
    query = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == current_user.id
    )
    
    if course_id:
        query = query.join(Quiz).filter(Quiz.course_id == course_id)
    
    attempts = query.order_by(QuizAttempt.created_at.desc()).all()
    
    return {"attempts": attempts, "total": len(attempts)}
