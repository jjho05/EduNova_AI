"""
Question Statistics model - Analytics per question
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class QuestionStatistics(Base):
    __tablename__ = "question_statistics"
    
    id = Column(String(36), primary_key=True)
    quiz_id = Column(String(36), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    question_index = Column(Integer, nullable=False)  # 0, 1, 2, ...
    
    # Estadísticas básicas
    total_attempts = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    incorrect_count = Column(Integer, default=0)
    
    # Distribución por opción
    option_stats = Column(JSON)  # {"option_0": 10, "option_1": 5, ...}
    
    # Métricas avanzadas
    difficulty_score = Column(Float)  # 0-1 (% que fallan)
    discrimination_index = Column(Float)  # -1 a 1 (qué tan bien discrimina)
    
    # Tiempo promedio en esta pregunta
    avg_time_spent = Column(Integer)  # segundos
    
    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="question_stats")
