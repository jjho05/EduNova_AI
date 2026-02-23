"""
Schemas for quiz attempts and statistics
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List


# Quiz Attempt Schemas
class QuizAttemptCreate(BaseModel):
    quiz_id: str
    answers: Dict[str, str]  # {"0": "selected_option", "1": "selected_option"}


class QuizAttemptResponse(BaseModel):
    id: str
    quiz_id: str
    student_id: str
    answers: Dict[str, str]
    score: Optional[float] = None
    correct_answers: int
    total_questions: int
    passed: bool
    started_at: datetime
    submitted_at: Optional[datetime] = None
    time_taken: Optional[int] = None
    status: str
    
    class Config:
        from_attributes = True


# Question Statistics Schemas
class QuestionStatsResponse(BaseModel):
    question_index: int
    total_attempts: int
    correct_count: int
    incorrect_count: int
    success_rate: float
    option_stats: Dict[str, int]
    difficulty_score: Optional[float] = None
    
    class Config:
        from_attributes = True


# Quiz Statistics Schemas
class QuizStatisticsResponse(BaseModel):
    quiz_id: str
    title: str
    total_attempts: int
    completed: int
    in_progress: int
    average_score: float
    median_score: float
    pass_rate: float
    highest_score: float
    lowest_score: float
    score_distribution: Dict[str, int]
    average_time: int
    
    class Config:
        from_attributes = True


# Enrollment Schemas
class EnrollmentCreate(BaseModel):
    course_id: str


class EnrollmentResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    status: str
    enrolled_at: datetime
    progress_percentage: float
    modules_completed: int
    current_grade: Optional[float] = None
    
    class Config:
        from_attributes = True


# Course Statistics Schemas
class CourseStatisticsResponse(BaseModel):
    course_id: str
    total_students: int
    active_students: int
    average_grade: Optional[float] = None
    pass_rate: Optional[float] = None
    completion_rate: Optional[float] = None
    avg_time_spent: Optional[int] = None
    
    class Config:
        from_attributes = True


# Student Comparison Schemas
class StudentComparisonResponse(BaseModel):
    student_id: str
    name: str
    quiz_score: float
    class_average: float
    percentile: float
    rank: int
    total_students: int


# At Risk Student Schema
class AtRiskStudentResponse(BaseModel):
    student_id: str
    name: str
    email: str
    risk_factor: float  # 0-1 (1 is high risk)
    average_grade: float
    missed_assignments: int
    last_access_days: int


class AtRiskListResponse(BaseModel):
    at_risk_students: List[AtRiskStudentResponse]
    total: int


# Dashboard Schemas
class DashboardAlert(BaseModel):
    type: str
    message: str
    count: int

class RecentActivity(BaseModel):
    quizzes_taken_today: int

class CourseDashboardStats(BaseModel):
    course_id: str
    title: str
    students: int
    active_students: int
    recent_activity: RecentActivity
    alerts: List[DashboardAlert]

class TeacherDashboardResponse(BaseModel):
    courses: List[CourseDashboardStats]
