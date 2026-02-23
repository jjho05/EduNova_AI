"""
Statistics Service - Calculate and manage quiz/course statistics
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import statistics as stats

from ..models.quiz import Quiz
from ..models.quiz_attempt import QuizAttempt, AttemptStatus
from ..models.question_statistics import QuestionStatistics
from ..models.course_statistics import CourseStatistics
from ..models.enrollment import Enrollment
from ..models.user import User


class StatisticsService:
    """Service for calculating statistics"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_quiz_statistics(self, quiz_id: str) -> Dict:
        """
        Calculate comprehensive quiz statistics
        """
        # Get all attempts for this quiz
        attempts = self.db.query(QuizAttempt).filter(
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.status == AttemptStatus.SUBMITTED
        ).all()
        
        if not attempts:
            return {
                "quiz_id": quiz_id,
                "total_attempts": 0,
                "message": "No attempts yet"
            }
        
        # Calculate basic stats
        scores = [a.score for a in attempts if a.score is not None]
        times = [a.time_taken for a in attempts if a.time_taken is not None]
        
        # Overall statistics
        overall_stats = {
            "average_score": round(sum(scores) / len(scores), 2) if scores else 0,
            "median_score": round(stats.median(scores), 2) if scores else 0,
            "pass_rate": round(sum(1 for a in attempts if a.passed) / len(attempts) * 100, 2),
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0,
        }
        
        # Score distribution
        score_distribution = {
            "90-100": sum(1 for s in scores if 90 <= s <= 100),
            "80-89": sum(1 for s in scores if 80 <= s < 90),
            "70-79": sum(1 for s in scores if 70 <= s < 80),
            "60-69": sum(1 for s in scores if 60 <= s < 70),
            "0-59": sum(1 for s in scores if s < 60),
        }
        
        # Time statistics
        time_stats = {
            "average_time": round(sum(times) / len(times)) if times else 0,
            "fastest": min(times) if times else 0,
            "slowest": max(times) if times else 0,
        }
        
        # Count by status
        in_progress = self.db.query(QuizAttempt).filter(
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.status == AttemptStatus.IN_PROGRESS
        ).count()
        
        return {
            "quiz_id": quiz_id,
            "total_attempts": len(attempts),
            "completed": len(attempts),
            "in_progress": in_progress,
            "overall_stats": overall_stats,
            "score_distribution": score_distribution,
            "time_stats": time_stats,
        }
    
    def calculate_question_statistics(self, quiz_id: str) -> List[Dict]:
        """
        Calculate statistics for each question in a quiz
        """
        quiz = self.db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            return []
        
        attempts = self.db.query(QuizAttempt).filter(
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.status == AttemptStatus.SUBMITTED
        ).all()
        
        if not attempts:
            return []
        
        questions = quiz.questions
        question_stats = []
        
        for idx, question in enumerate(questions):
            correct_answer = question.get('correctAnswer')
            options = question.get('options', [])
            
            # Count responses for each option
            option_counts = {f"option_{i}": 0 for i in range(len(options))}
            correct_count = 0
            total_attempts = 0
            
            for attempt in attempts:
                answer = attempt.answers.get(str(idx))
                if answer:
                    total_attempts += 1
                    # Find which option was selected
                    try:
                        selected_idx = options.index(answer)
                        option_counts[f"option_{selected_idx}"] += 1
                        
                        if selected_idx == correct_answer:
                            correct_count += 1
                    except ValueError:
                        pass
            
            incorrect_count = total_attempts - correct_count
            success_rate = (correct_count / total_attempts * 100) if total_attempts > 0 else 0
            
            # Calculate difficulty (higher = harder)
            difficulty_score = (incorrect_count / total_attempts) if total_attempts > 0 else 0
            
            question_stats.append({
                "question_number": idx + 1,
                "question_text": question.get('question', ''),
                "correct_answer": options[correct_answer] if correct_answer < len(options) else "",
                "stats": {
                    "total_attempts": total_attempts,
                    "correct": correct_count,
                    "incorrect": incorrect_count,
                    "success_rate": round(success_rate, 2),
                    "option_distribution": option_counts,
                    "difficulty": "easy" if success_rate > 80 else "medium" if success_rate > 60 else "hard",
                    "difficulty_score": round(difficulty_score, 2),
                }
            })
        
        return question_stats
    
    def get_student_comparison(self, quiz_id: str) -> Dict:
        """
        Get student comparison for a quiz
        """
        attempts = self.db.query(QuizAttempt, User).join(
            User, QuizAttempt.student_id == User.id
        ).filter(
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.status == AttemptStatus.SUBMITTED
        ).all()
        
        if not attempts:
            return {"students": [], "class_stats": {}}
        
        # Build student list with scores
        students_data = []
        for attempt, user in attempts:
            students_data.append({
                "student_id": user.id,
                "name": user.name,
                "score": attempt.score,
                "time_taken": attempt.time_taken,
            })
        
        # Sort by score
        students_data.sort(key=lambda x: x['score'], reverse=True)
        
        # Add rank and percentile
        total_students = len(students_data)
        for idx, student in enumerate(students_data):
            student['rank'] = idx + 1
            student['percentile'] = round((total_students - idx) / total_students * 100, 1)
        
        # Calculate class stats
        scores = [s['score'] for s in students_data]
        class_stats = {
            "top_10_percent": scores[int(total_students * 0.1)] if total_students > 10 else scores[0],
            "bottom_10_percent": scores[int(total_students * 0.9)] if total_students > 10 else scores[-1],
            "average": round(sum(scores) / len(scores), 2),
        }
        
        return {
            "students": students_data,
            "class_stats": class_stats,
        }
    
    def update_question_statistics(self, quiz_id: str):
        """
        Update or create question statistics records
        """
        question_stats = self.calculate_question_statistics(quiz_id)
        
        for stat in question_stats:
            idx = stat['question_number'] - 1
            
            # Check if exists
            existing = self.db.query(QuestionStatistics).filter(
                QuestionStatistics.quiz_id == quiz_id,
                QuestionStatistics.question_index == idx
            ).first()
            
            if existing:
                # Update
                existing.total_attempts = stat['stats']['total_attempts']
                existing.correct_count = stat['stats']['correct']
                existing.incorrect_count = stat['stats']['incorrect']
                existing.option_stats = stat['stats']['option_distribution']
                existing.difficulty_score = stat['stats']['difficulty_score']
                existing.updated_at = datetime.utcnow()
            else:
                # Create
                from uuid import uuid4
                new_stat = QuestionStatistics(
                    id=str(uuid4()),
                    quiz_id=quiz_id,
                    question_index=idx,
                    total_attempts=stat['stats']['total_attempts'],
                    correct_count=stat['stats']['correct'],
                    incorrect_count=stat['stats']['incorrect'],
                    option_stats=stat['stats']['option_distribution'],
                    difficulty_score=stat['stats']['difficulty_score']
                )
                self.db.add(new_stat)
        
        self.db.commit()
    
    def calculate_course_statistics(self, course_id: str):
        """
        Calculate and update course statistics
        """
        # Get enrollments
        enrollments = self.db.query(Enrollment).filter(
            Enrollment.course_id == course_id
        ).all()
        
        if not enrollments:
            return
        
        # Count by status
        from ..models.enrollment import EnrollmentStatus
        active = sum(1 for e in enrollments if e.status == EnrollmentStatus.ACTIVE)
        completed = sum(1 for e in enrollments if e.status == EnrollmentStatus.COMPLETED)
        dropped = sum(1 for e in enrollments if e.status == EnrollmentStatus.DROPPED)
        
        # Calculate grades
        grades = [e.current_grade for e in enrollments if e.current_grade is not None]
        avg_grade = sum(grades) / len(grades) if grades else None
        median_grade = stats.median(grades) if grades else None
        
        # Pass rate (assuming 60% is passing)
        pass_rate = (sum(1 for g in grades if g >= 60) / len(grades) * 100) if grades else None
        
        # Completion rate
        completion_rate = (completed / len(enrollments) * 100) if enrollments else 0
        
        # Check if statistics record exists
        course_stats = self.db.query(CourseStatistics).filter(
            CourseStatistics.course_id == course_id
        ).first()
        
        if course_stats:
            # Update
            course_stats.total_students = len(enrollments)
            course_stats.active_students = active
            course_stats.completed_students = completed
            course_stats.dropped_students = dropped
            course_stats.average_grade = avg_grade
            course_stats.median_grade = median_grade
            course_stats.pass_rate = pass_rate
            course_stats.completion_rate = completion_rate
            course_stats.updated_at = datetime.utcnow()
        else:
            # Create
            from uuid import uuid4
            course_stats = CourseStatistics(
                id=str(uuid4()),
                course_id=course_id,
                total_students=len(enrollments),
                active_students=active,
                completed_students=completed,
                dropped_students=dropped,
                average_grade=avg_grade,
                median_grade=median_grade,
                pass_rate=pass_rate,
                completion_rate=completion_rate
            )
            self.db.add(course_stats)
        
        self.db.commit()
    
    def get_at_risk_students(self, course_id: str) -> List[Dict]:
        """
        Identify students at risk of failing
        """
        enrollments = self.db.query(Enrollment, User).join(
            User, Enrollment.student_id == User.id
        ).filter(
            Enrollment.course_id == course_id,
            Enrollment.status == "active"
        ).all()
        
        at_risk = []
        for enrollment, user in enrollments:
            risk_factors = []
            risk_score = 0
            
            # Low grade
            if enrollment.current_grade and enrollment.current_grade < 60:
                risk_factors.append("Calificación baja")
                risk_score += 3
            
            # No recent activity
            if enrollment.last_activity_at:
                days_inactive = (datetime.utcnow() - enrollment.last_activity_at).days
                if days_inactive > 7:
                    risk_factors.append(f"Sin actividad en {days_inactive} días")
                    risk_score += 2
            
            # Low progress
            if enrollment.progress_percentage < 50:
                risk_factors.append("Progreso bajo")
                risk_score += 1
            
            if risk_score >= 2:
                at_risk.append({
                    "student_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "current_grade": enrollment.current_grade,
                    "progress": enrollment.progress_percentage,
                    "risk_factors": risk_factors,
                    "risk_score": risk_score,
                })
        
        # Sort by risk score
        at_risk.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return at_risk
