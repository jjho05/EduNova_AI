"""
Activity Log model - Track student activities
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class ActivityType(str, enum.Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    VIEW_MODULE = "view_module"
    START_QUIZ = "start_quiz"
    SUBMIT_QUIZ = "submit_quiz"
    VIEW_DOCUMENT = "view_document"
    CHAT_AI = "chat_ai"
    SUBMIT_ASSIGNMENT = "submit_assignment"
    VIEW_GRADE = "view_grade"


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="SET NULL"), index=True)
    
    # Actividad
    activity_type = Column(SQLEnum(ActivityType), nullable=False)
    
    # Detalles específicos
    details = Column(JSON)  # {"module_id": "...", "quiz_id": "...", etc}
    
    # Tiempo
    duration = Column(Integer)  # segundos (si aplica)
    
    # Metadata
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="activity_logs")
    course = relationship("Course", back_populates="activity_logs")
