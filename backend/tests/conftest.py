import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from app.main import app
from app.database import Base, get_db
# Import all models to register them on Base.metadata
from app.models.user import User
from app.models.course import Course
from app.models.module import Module
from app.models.enrollment import Enrollment
from app.models.assignment import Assignment
from app.models.quiz import Quiz
from app.models.document import Document
from app.models.notification import Notification
from app.models.progress import Progress
from app.models.schedule import Schedule
from app.models.quiz_attempt import QuizAttempt
from app.models.activity_log import ActivityLog
from app.models.course_statistics import CourseStatistics
from app.models.question_statistics import QuestionStatistics


# Use SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

from sqlalchemy.pool import StaticPool

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db_session):
    # Dependency override
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
