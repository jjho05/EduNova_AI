from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from ..database import get_db
from ..models.user import User
from ..models.schedule import Schedule, Rubric
from ..schemas.schedule import ScheduleCreate, ScheduleResponse, RubricCreate, RubricResponse
from ..services.auth import get_current_teacher
from ..services.schedule_service import generar_cronograma, generar_rubrica

router = APIRouter()

@router.post("/schedules", response_model=ScheduleResponse)
def create_schedule(
    schedule_data: ScheduleCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Generate a schedule for a course with AI"""
    # Get course from database
    from ..models.course import Course
    from ..models.module import Module
    
    course = db.query(Course).filter(Course.id == schedule_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Get course modules
    modules_query = db.query(Module).filter(Module.course_id == course.id).all()
    modules = [m.title for m in modules_query] if modules_query else ["Módulo 1", "Módulo 2", "Módulo 3"]
    
    # Generate schedule with Gemini
    cronograma = generar_cronograma(
        course_title=course.title,
        modules=modules,
        start_date=schedule_data.start_date.isoformat(),
        end_date=schedule_data.end_date.isoformat(),
        hours_per_week=schedule_data.hours_per_week
    )
    
    if not cronograma or not cronograma.get('semanas'):
        raise HTTPException(status_code=500, detail="Error generating schedule")
    
    # Save to database
    new_schedule = Schedule(
        id=str(uuid4()),
        course_id=schedule_data.course_id,
        start_date=schedule_data.start_date,
        end_date=schedule_data.end_date,
        schedule_data=cronograma
    )
    
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    
    return new_schedule

@router.post("/rubrics", response_model=RubricResponse)
def create_rubric(
    rubric_data: RubricCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Generate a rubric for an activity with AI"""
    # Generate rubric with Gemini
    rubrica = generar_rubrica(
        activity_name=rubric_data.activity_name,
        activity_type=rubric_data.activity_type,
        criteria=rubric_data.criteria,
        max_score=rubric_data.max_score
    )
    
    if not rubrica or not rubrica.get('criterios'):
        raise HTTPException(status_code=500, detail="Error generating rubric")
    
    # Save to database
    new_rubric = Rubric(
        id=str(uuid4()),
        course_id=rubric_data.course_id,
        activity_name=rubric_data.activity_name,
        rubric_data=rubrica
    )
    
    db.add(new_rubric)
    db.commit()
    db.refresh(new_rubric)
    
    return new_rubric

@router.get("/schedules/course/{course_id}")
def get_course_schedules(
    course_id: str,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all schedules for a course"""
    schedules = db.query(Schedule).filter(Schedule.course_id == course_id).all()
    return schedules

@router.get("/rubrics/course/{course_id}")
def get_course_rubrics(
    course_id: str,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all rubrics for a course"""
    rubrics = db.query(Rubric).filter(Rubric.course_id == course_id).all()
    return rubrics
