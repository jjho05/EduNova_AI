# Expose models for easy import
from .user import User, UserRole
from .course import Course
from .quiz import Quiz, QuizType

__all__ = ["User", "UserRole", "Course", "Quiz", "QuizType"]
