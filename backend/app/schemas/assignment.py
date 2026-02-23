from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssignmentCreate(BaseModel):
    course_id: str
    module_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    assignment_type: str = "homework"
    max_score: int = 100
    due_date: Optional[str] = None

class AssignmentResponse(BaseModel):
    id: str
    course_id: str
    module_id: Optional[str]
    title: str
    description: Optional[str]
    assignment_type: str
    max_score: int
    due_date: Optional[str]
    created_at: str
    
    class Config:
        from_attributes = True

class SubmissionCreate(BaseModel):
    assignment_id: str
    content: Optional[str] = None
    file_url: Optional[str] = None

class SubmissionResponse(BaseModel):
    id: str
    assignment_id: str
    student_id: str
    content: Optional[str]
    file_url: Optional[str]
    score: Optional[float]
    feedback: Optional[str]
    submitted_at: str
    graded_at: Optional[str]
    
    class Config:
        from_attributes = True

class GradeSubmission(BaseModel):
    score: float
    feedback: Optional[str] = None
