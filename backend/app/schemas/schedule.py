from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ScheduleCreate(BaseModel):
    course_id: str
    start_date: date
    end_date: date
    hours_per_week: int = 4

class WeekSchedule(BaseModel):
    numero: int
    fecha_inicio: str
    fecha_fin: str
    temas: List[str]
    actividades: List[str]
    evaluacion: Optional[str]

class ScheduleResponse(BaseModel):
    id: str
    course_id: str
    start_date: date
    end_date: date
    schedule_data: dict
    
    class Config:
        from_attributes = True

class RubricCreate(BaseModel):
    course_id: str
    activity_name: str
    activity_type: str
    criteria: Optional[List[str]] = None
    max_score: int = 100

class RubricLevel(BaseModel):
    puntos: int
    descripcion: str

class RubricCriterion(BaseModel):
    nombre: str
    peso: int
    niveles: dict

class RubricResponse(BaseModel):
    id: str
    course_id: str
    activity_name: str
    rubric_data: dict
    
    class Config:
        from_attributes = True
