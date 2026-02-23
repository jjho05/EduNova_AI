from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List
from datetime import datetime
from ..database import get_db
from ..models.user import User
from ..models.assignment import Assignment, AssignmentSubmission
from ..schemas.assignment import (
    AssignmentCreate, AssignmentResponse,
    SubmissionCreate, SubmissionResponse, GradeSubmission
)
from ..services.auth import get_current_user, get_current_teacher

router = APIRouter()

# Assignment endpoints (Teacher)
@router.post("/assignments", response_model=AssignmentResponse)
def create_assignment(
    assignment_data: AssignmentCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Create a new assignment (Teacher only)"""
    new_assignment = Assignment(
        id=str(uuid4()),
        course_id=assignment_data.course_id,
        module_id=assignment_data.module_id,
        title=assignment_data.title,
        description=assignment_data.description,
        assignment_type=assignment_data.assignment_type,
        max_score=assignment_data.max_score,
        due_date=assignment_data.due_date
    )
    
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    return new_assignment

@router.get("/assignments/course/{course_id}", response_model=List[AssignmentResponse])
def get_course_assignments(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all assignments for a course"""
    assignments = db.query(Assignment).filter(Assignment.course_id == course_id).all()
    return assignments

# Submission endpoints (Student)
@router.post("/submissions", response_model=SubmissionResponse)
def submit_assignment(
    submission_data: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit an assignment (Student)"""
    # Check if already submitted
    existing = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.assignment_id == submission_data.assignment_id,
        AssignmentSubmission.student_id == current_user.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Assignment already submitted")
    
    new_submission = AssignmentSubmission(
        id=str(uuid4()),
        assignment_id=submission_data.assignment_id,
        student_id=current_user.id,
        content=submission_data.content,
        file_url=submission_data.file_url
    )
    
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    
    return new_submission

@router.get("/submissions/assignment/{assignment_id}", response_model=List[SubmissionResponse])
def get_assignment_submissions(
    assignment_id: str,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all submissions for an assignment (Teacher only)"""
    submissions = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.assignment_id == assignment_id
    ).all()
    return submissions

@router.patch("/submissions/{submission_id}/grade", response_model=SubmissionResponse)
def grade_submission(
    submission_id: str,
    grade_data: GradeSubmission,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Grade a submission (Teacher only)"""
    submission = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    submission.score = grade_data.score
    submission.feedback = grade_data.feedback
    submission.graded_at = datetime.utcnow().isoformat()
    
    db.commit()
    db.refresh(submission)
    
    return submission

@router.get("/my-submissions", response_model=List[SubmissionResponse])
def get_my_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all submissions for current student"""
    submissions = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.student_id == current_user.id
    ).all()
    return submissions
