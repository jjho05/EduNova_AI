"""
Statistics routes - Analytics and reporting endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..auth import get_current_user
from ..services.statistics_service import StatisticsService
from ..schemas.statistics import (
    QuizStatisticsResponse,
    QuestionStatsResponse,
    CourseStatisticsResponse,
    StudentComparisonResponse,
    AtRiskListResponse,
    TeacherDashboardResponse
)

router = APIRouter()


@router.get("/quizzes/{quiz_id}/statistics", response_model=QuizStatisticsResponse)
async def get_quiz_statistics(
    quiz_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive quiz statistics
    For teachers only
    """
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view statistics")
    
    stats_service = StatisticsService(db)
    stats = stats_service.calculate_quiz_statistics(quiz_id)
    
    return stats


@router.get("/quizzes/{quiz_id}/question-stats", response_model=dict) # TODO: Define proper wrapper if needed
async def get_question_statistics(
    quiz_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistics for each question in a quiz
    Shows how many students got each question right/wrong
    """
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view statistics")
    
    stats_service = StatisticsService(db)
    question_stats = stats_service.calculate_question_statistics(quiz_id)
    
    # Validate against list of QuestionStatsResponse internally or use a wrapper model
    return {"questions": question_stats}


@router.get("/quizzes/{quiz_id}/student-comparison", response_model=StudentComparisonResponse)
async def get_student_comparison(
    quiz_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get student comparison and ranking for a quiz
    """
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view statistics")
    
    stats_service = StatisticsService(db)
    comparison = stats_service.get_student_comparison(quiz_id)
    
    return comparison


@router.get("/courses/{course_id}/statistics", response_model=CourseStatisticsResponse)
async def get_course_statistics(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get course statistics
    """
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view statistics")
    
    stats_service = StatisticsService(db)
    stats_service.calculate_course_statistics(course_id)
    
    from ..models.course_statistics import CourseStatistics
    course_stats = db.query(CourseStatistics).filter(
        CourseStatistics.course_id == course_id
    ).first()
    
    if not course_stats:
        raise HTTPException(status_code=404, detail="No statistics available")
    
    return course_stats


@router.get("/analytics/at-risk-students", response_model=AtRiskListResponse)
async def get_at_risk_students(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of students at risk of failing
    """
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view this")
    
    stats_service = StatisticsService(db)
    at_risk = stats_service.get_at_risk_students(course_id)
    
    return {"at_risk_students": at_risk, "total": len(at_risk)}


@router.get("/teacher/dashboard", response_model=TeacherDashboardResponse)
async def get_teacher_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get teacher dashboard with all courses and alerts
    """
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can access this")
    
    from ..models.course import Course
    from ..models.enrollment import Enrollment
    from ..models.quiz_attempt import QuizAttempt
    from ..models.quiz import Quiz
    from datetime import datetime
    from sqlalchemy import func
    
    # Get teacher's courses
    courses = db.query(Course).filter(Course.user_id == current_user.id).all()
    
    dashboard_data = []
    for course in courses:
        # Count students
        total_students = db.query(Enrollment).filter(
            Enrollment.course_id == course.id
        ).count()
        
        active_students = db.query(Enrollment).filter(
            Enrollment.course_id == course.id,
            Enrollment.status == "active"
        ).count()
        
        # Recent activity (today)
        today = datetime.utcnow().date()
        quizzes_today = db.query(QuizAttempt).filter(
            QuizAttempt.quiz_id.in_(
                db.query(Quiz.id).filter(Quiz.course_id == course.id)
            ),
            func.date(QuizAttempt.created_at) == today
        ).count()
        
        # Get at-risk students
        stats_service = StatisticsService(db)
        at_risk = stats_service.get_at_risk_students(course.id)
        
        # Build alerts
        alerts = []
        if at_risk:
            alerts.append({
                "type": "at_risk",
                "message": f"{len(at_risk)} estudiantes en riesgo",
                "count": len(at_risk)
            })
        
        dashboard_data.append({
            "course_id": course.id,
            "title": course.title,
            "students": total_students,
            "active_students": active_students,
            "recent_activity": {
                "quizzes_taken_today": quizzes_today
            },
            "alerts": alerts
        })
    
    return {"courses": dashboard_data}
