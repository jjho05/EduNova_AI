"""
Course Statistics model - Aggregated course analytics
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class CourseStatistics(Base):
    __tablename__ = "course_statistics"
    
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Estudiantes
    total_students = Column(Integer, default=0)
    active_students = Column(Integer, default=0)
    completed_students = Column(Integer, default=0)
    dropped_students = Column(Integer, default=0)
    
    # Rendimiento
    average_grade = Column(Float)
    median_grade = Column(Float)
    pass_rate = Column(Float)  # % de estudiantes que pasan
    completion_rate = Column(Float)  # % de estudiantes que completan
    
    # Engagement
    avg_time_spent = Column(Integer)  # minutos por estudiante
    total_submissions = Column(Integer, default=0)
    avg_quiz_score = Column(Float)
    
    # Por módulo
    module_completion_rates = Column(JSON)  # {"module_1": 85.5, "module_2": 70.0}
    module_avg_grades = Column(JSON)
    
    # Tendencias
    grade_trend = Column(String(20))  # "improving", "declining", "stable"
    engagement_trend = Column(String(20))
    
    # Timestamps
    last_calculated = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="statistics")
