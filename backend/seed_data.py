"""
Script para poblar la base de datos con datos iniciales de prueba
Ejecutar: python seed_data.py
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.database import engine, SessionLocal
from app.models.user import User, Base
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
from passlib.context import CryptContext
from uuid import uuid4
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_seed_data():
    """Create initial seed data"""
    print("🌱 Iniciando seed de base de datos...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("⚠️  La base de datos ya contiene datos. Limpiando...")
            db.query(Quiz).delete()
            db.query(Assignment).delete()
            db.query(Module).delete()
            db.query(Enrollment).delete()
            db.query(Course).delete()
            db.query(User).delete()
            db.commit()
        
        print("👤 Creando usuarios...")
        
        # Create Teacher
        teacher = User(
            id=str(uuid4()),
            email="profesor@test.com",
            name="Prof. Juan García",
            hashed_password=hash_password("profesor123"),
            role="teacher",
            created_at=datetime.utcnow().isoformat()
        )
        db.add(teacher)
        
        # Create Students
        students = []
        student_names = [
            ("Maria López", "maria@test.com"),
            ("Carlos Ruiz", "carlos@test.com"),
            ("Ana Torres", "ana@test.com"),
        ]
        
        for name, email in student_names:
            student = User(
                id=str(uuid4()),
                email=email,
                name=name,
                hashed_password=hash_password("alumno123"),
                role="student",
                created_at=datetime.utcnow().isoformat()
            )
            students.append(student)
            db.add(student)
        
        db.commit()
        print(f"✅ Creados {1 + len(students)} usuarios (1 profesor, {len(students)} alumnos)")
        
        print("📚 Creando cursos...")
        
        # Create Courses
        courses_data = [
            {
                "title": "Programación en Python",
                "description": "Curso completo de Python desde cero hasta avanzado",
                "modules": [
                    "Introducción a Python",
                    "Estructuras de Control",
                    "Funciones y Módulos",
                    "Programación Orientada a Objetos"
                ]
            },
            {
                "title": "Matemáticas Discretas",
                "description": "Fundamentos matemáticos para ciencias de la computación",
                "modules": [
                    "Lógica Proposicional",
                    "Teoría de Conjuntos",
                    "Grafos y Árboles",
                    "Combinatoria"
                ]
            },
        ]
        
        courses = []
        for course_data in courses_data:
            course = Course(
                id=str(uuid4()),
                title=course_data["title"],
                description=course_data["description"],
                teacher_id=teacher.id,
                created_at=datetime.utcnow().isoformat()
            )
            courses.append(course)
            db.add(course)
            db.commit()
            
            # Create modules for this course
            for idx, module_title in enumerate(course_data["modules"], 1):
                module = Module(
                    id=str(uuid4()),
                    course_id=course.id,
                    title=module_title,
                    order_index=idx,
                    created_at=datetime.utcnow().isoformat()
                )
                db.add(module)
            
            # Create assignments for this course
            assignment = Assignment(
                id=str(uuid4()),
                course_id=course.id,
                title=f"Tarea 1: {course_data['title']}",
                description=f"Resolver ejercicios prácticos del módulo 1",
                max_score=100,
                due_date=(datetime.utcnow() + timedelta(days=7)).isoformat(),
                created_at=datetime.utcnow().isoformat()
            )
            db.add(assignment)
            
            # Create a quiz for this course
            quiz = Quiz(
                id=str(uuid4()),
                course_id=course.id,
                title=f"Quiz 1: {course_data['title']}",
                description="Evaluación del primer módulo",
                topic=course_data['title'],
                quiz_type='topic',
                created_at=datetime.utcnow().isoformat()
            )
            db.add(quiz)
            db.commit()
        
        db.commit()
        print(f"✅ Creados {len(courses)} cursos con módulos, tareas y quizzes")
        
        print("📝 Inscribiendo alumnos en cursos...")
        
        # Enroll students in courses
        enrollments = 0
        for student in students:
            for course in courses:
                enrollment = Enrollment(
                    id=str(uuid4()),
                    user_id=student.id,
                    course_id=course.id,
                    enrolled_at=datetime.utcnow().isoformat()
                )
                db.add(enrollment)
                enrollments += 1
        
        db.commit()
        print(f"✅ Creadas {enrollments} inscripciones")
        
        print("\n🎉 ¡Seed completado exitosamente!")
        print("\n📋 Credenciales de acceso:")
        print("=" * 50)
        print("👨‍🏫 PROFESOR:")
        print("   Email: profesor@test.com")
        print("   Password: profesor123")
        print("\n👨‍🎓 ALUMNOS:")
        for name, email in student_names:
            print(f"   {name}")
            print(f"   Email: {email}")
            print(f"   Password: alumno123")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error durante el seed: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    create_seed_data()
