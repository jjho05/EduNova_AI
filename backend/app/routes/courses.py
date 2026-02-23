from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.course import Course
from ..schemas.course import CourseCreate, CourseResponse, CourseWithModules
from ..services.auth import get_current_user
from ..services.gemini_service import generar_silabo_curso

router = APIRouter()

@router.post("/", response_model=CourseResponse)
def create_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new course with AI-generated syllabus"""
    # Generate syllabus with Gemini
    curso_completo = generar_silabo_curso(course_data.title)
    
    if not curso_completo:
        raise HTTPException(status_code=500, detail="Error generating course syllabus")
    
    # Create course
    new_course = Course(
        id=str(uuid4()),
        user_id=current_user.id,
        title=course_data.title,
        description=course_data.description or curso_completo.get('tema_general'),
        overall_progress=0.0
    )
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return new_course

@router.get("/", response_model=List[CourseResponse])
def get_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all courses for current user"""
    courses = db.query(Course).filter(Course.user_id == current_user.id).all()
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific course"""
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.user_id == current_user.id
    ).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course

@router.delete("/{course_id}")
def delete_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a course"""
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.user_id == current_user.id
    ).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(course)
    db.commit()
    
    return {"message": "Course deleted successfully"}
