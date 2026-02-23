from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum, Float
from sqlalchemy.sql import func
from ..database import Base
from datetime import datetime
import enum

class AssignmentType(str, enum.Enum):
    HOMEWORK = "homework"
    EXAM = "exam"
    PROJECT = "project"
    QUIZ = "quiz"

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(String(36), ForeignKey("modules.id", ondelete="SET NULL"), index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    assignment_type = Column(Enum(AssignmentType), default=AssignmentType.HOMEWORK)
    max_score = Column(Integer, default=100)
    due_date = Column(String(50))
    created_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"
    
    id = Column(String(36), primary_key=True)
    assignment_id = Column(String(36), ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text)
    file_url = Column(String(500))
    score = Column(Float)
    feedback = Column(Text)
    submitted_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())
    graded_at = Column(String(50))
