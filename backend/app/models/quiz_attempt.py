"""
Quiz Attempt model - Tracks student quiz submissions
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class AttemptStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    GRADED = "graded"


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(String(36), primary_key=True)
    quiz_id = Column(String(36), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Respuestas del estudiante
    answers = Column(JSON)  # {"0": "option_text", "1": "option_text", ...}
    
    # Resultados
    score = Column(Float)  # 0-100
    correct_answers = Column(Integer, default=0)
    total_questions = Column(Integer)
    passed = Column(Boolean, default=False)
    
    # Tiempo
    started_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime)
    time_taken = Column(Integer)  # segundos
    
    # Estado
    status = Column(SQLEnum(AttemptStatus), default=AttemptStatus.IN_PROGRESS)
    
    # Metadata
    ip_address = Column(String(45))  # Para seguridad
    user_agent = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="attempts")
    student = relationship("User", back_populates="quiz_attempts")
