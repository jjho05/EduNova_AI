from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum

class QuizType(str, enum.Enum):
    LEVELING = "leveling"
    TOPIC = "topic"
    MODULE_EXAM = "module_exam"

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="SET NULL"), index=True)
    quiz_type = Column(SQLEnum(QuizType), nullable=False)
    topic = Column(String(255))
    questions = Column(JSON, nullable=False)
    answers = Column(JSON)
    score = Column(Integer)
    total_questions = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    attempts = relationship("QuizAttempt", back_populates="quiz")
    question_stats = relationship("QuestionStatistics", back_populates="quiz")
