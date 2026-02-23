from pydantic import BaseModel
from typing import Optional

class ProgressResponse(BaseModel):
    id: str
    user_id: str
    course_id: str
    module_id: Optional[str]
    completion_percentage: float
    time_spent_minutes: int
    last_accessed: str
    
    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    completion_percentage: Optional[float] = None
    time_spent_minutes: Optional[int] = None
