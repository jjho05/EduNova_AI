from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.sql import func
from ..database import Base
from datetime import datetime

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(String(36), ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    completion_percentage = Column(Float, default=0.0)
    time_spent_minutes = Column(Integer, default=0)
    last_accessed = Column(String(50), default=lambda: datetime.utcnow().isoformat())
    created_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())
