from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List
from datetime import datetime
from ..database import get_db
from ..models.user import User
from ..models.progress import Progress
from ..schemas.progress import ProgressResponse, ProgressUpdate
from ..services.auth import get_current_user

router = APIRouter()

@router.get("/progress/course/{course_id}", response_model=List[ProgressResponse])
def get_course_progress(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get progress for a specific course"""
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.course_id == course_id
    ).all()
    return progress

@router.post("/progress/course/{course_id}/module/{module_id}")
def update_module_progress(
    course_id: str,
    module_id: str,
    progress_data: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update progress for a module"""
    # Find existing progress
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.course_id == course_id,
        Progress.module_id == module_id
    ).first()
    
    if not progress:
        # Create new progress entry
        progress = Progress(
            id=str(uuid4()),
            user_id=current_user.id,
            course_id=course_id,
            module_id=module_id,
            completion_percentage=progress_data.completion_percentage or 0.0,
            time_spent_minutes=progress_data.time_spent_minutes or 0
        )
        db.add(progress)
    else:
        # Update existing
        if progress_data.completion_percentage is not None:
            progress.completion_percentage = progress_data.completion_percentage
        if progress_data.time_spent_minutes is not None:
            progress.time_spent_minutes += progress_data.time_spent_minutes
        progress.last_accessed = datetime.utcnow().isoformat()
    
    db.commit()
    db.refresh(progress)
    
    return progress

@router.get("/progress/stats")
def get_progress_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overall progress statistics for current user"""
    from sqlalchemy import func
    
    stats = db.query(
        func.count(Progress.id).label('total_modules'),
        func.avg(Progress.completion_percentage).label('avg_completion'),
        func.sum(Progress.time_spent_minutes).label('total_time')
    ).filter(Progress.user_id == current_user.id).first()
    
    return {
        "total_modules": stats.total_modules or 0,
        "average_completion": round(stats.avg_completion or 0, 2),
        "total_time_minutes": stats.total_time or 0
    }
