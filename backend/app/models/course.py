from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    overall_progress = Column(Float, default=0.0)
    average_grade = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    documents = relationship("Document", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    statistics = relationship("CourseStatistics", back_populates="course", uselist=False)
    activity_logs = relationship("ActivityLog", back_populates="course")
