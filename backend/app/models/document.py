"""
Document model for storing uploaded files
"""
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class DocumentType(str, enum.Enum):
    CURRICULUM = "curriculum"
    SYLLABUS = "syllabus"
    REFERENCE = "reference"
    EXERCISE = "exercise"
    OTHER = "other"


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    
    # Metadata
    name = Column(String(255), nullable=False)
    description = Column(Text)
    document_type = Column(SQLEnum(DocumentType), default=DocumentType.OTHER)
    
    # File info
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50))  # pdf, docx, jpg, etc.
    file_size = Column(Integer)  # bytes
    
    # Processing
    processed = Column(Boolean, default=False)
    extracted_text = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    course = relationship("Course", back_populates="documents")
