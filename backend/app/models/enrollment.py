"""
Enrollment model - Student course registration
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class EnrollmentStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"
    SUSPENDED = "suspended"


class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Estado
    status = Column(SQLEnum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    dropped_at = Column(DateTime)
    
    # Progreso
    progress_percentage = Column(Float, default=0.0)  # 0-100
    modules_completed = Column(Integer, default=0)
    total_modules = Column(Integer, default=0)
    
    # Calificaciones
    current_grade = Column(Float)  # Promedio actual
    final_grade = Column(Float)  # Calificación final
    
    # Engagement
    last_activity_at = Column(DateTime)
    total_time_spent = Column(Integer, default=0)  # minutos
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
