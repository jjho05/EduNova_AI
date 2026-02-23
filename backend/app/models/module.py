from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Integer, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Module(Base):
    __tablename__ = "modules"
    
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    content = Column(Text)  # Markdown content
    order_index = Column(Integer, default=0)
    
    # Additional fields
    hours = Column(Integer, default=0)  # Estimated hours
    topics = Column(JSON)  # List of topics
    
    # Status
    is_completed = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    # course = relationship("Course", back_populates="modules")
