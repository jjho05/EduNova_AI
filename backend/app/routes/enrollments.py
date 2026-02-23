"""
Enrollment routes - Course registration
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from ..database import get_db
from ..models.user import User
from ..models.course import Course
from ..models.enrollment import Enrollment, EnrollmentStatus
from ..auth import get_current_user
from ..schemas.statistics import EnrollmentCreate, EnrollmentResponse

router = APIRouter()


@router.post("/enrollments", response_model=EnrollmentResponse)
async def enroll_in_course(
    enrollment_data: EnrollmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enroll student in a course
    """
    # Check if course exists
    course = db.query(Course).filter(Course.id == enrollment_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == enrollment_data.course_id
    ).first()
    
    if existing:
        if existing.status == EnrollmentStatus.ACTIVE:
            raise HTTPException(status_code=400, detail="Already enrolled")
        else:
            # Reactivate enrollment
            existing.status = EnrollmentStatus.ACTIVE
            existing.enrolled_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing
    
    # Create enrollment
    enrollment = Enrollment(
        id=str(uuid4()),
        student_id=current_user.id,
        course_id=enrollment_data.course_id,
        status=EnrollmentStatus.ACTIVE
    )
    
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    return enrollment


@router.get("/my-enrollments")
async def get_my_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all enrollments for current student
    """
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id
    ).all()
    
    return {"enrollments": enrollments, "total": len(enrollments)}


@router.get("/courses/{course_id}/enrollments")
async def get_course_enrollments(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all enrollments for a course (teacher only)
    """
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view enrollments")
    
    # Verify teacher owns the course
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.user_id == current_user.id
    ).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    enrollments = db.query(Enrollment).filter(
        Enrollment.course_id == course_id
    ).all()
    
    return {"enrollments": enrollments, "total": len(enrollments)}


@router.delete("/enrollments/{enrollment_id}")
async def drop_course(
    enrollment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Drop a course (change status to dropped)
    """
    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id,
        Enrollment.student_id == current_user.id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    enrollment.status = EnrollmentStatus.DROPPED
    enrollment.dropped_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Course dropped successfully"}
