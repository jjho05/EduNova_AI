from sqlalchemy import Column, String, Date, JSON, ForeignKey
from sqlalchemy.sql import func
from ..database import Base

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    schedule_data = Column(JSON, nullable=False)
    created_at = Column(Date, server_default=func.current_date())

class Rubric(Base):
    __tablename__ = "rubrics"
    
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(String(36), ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    activity_name = Column(String(255), nullable=False)
    rubric_data = Column(JSON, nullable=False)
    created_at = Column(Date, server_default=func.current_date())
