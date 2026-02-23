from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class ModuleData(BaseModel):
    titulo: str
    subtemas: List[str]

class CourseResponse(CourseBase):
    id: str
    user_id: str
    overall_progress: float
    average_grade: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

class CourseWithModules(CourseResponse):
    modulos: List[dict]
