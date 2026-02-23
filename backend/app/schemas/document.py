"""
Document schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.document import DocumentType


class DocumentBase(BaseModel):
    name: str
    description: Optional[str] = None
    document_type: DocumentType = DocumentType.OTHER
    course_id: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: str
    user_id: str
    file_path: str
    file_type: str
    file_size: int
    processed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
