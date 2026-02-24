#!/bin/bash

echo "🚀 Iniciando aplicación en Hugging Face Spaces..."

# Wait for database to be ready (Supabase is usually instant but just in case)
echo "⏳ Verificando conexión a base de datos..."
sleep 2

# Run database migrations (create tables if they don't exist)
echo "📊 Creando/actualizando tablas en PostgreSQL..."
python -c "
from app.database import engine, Base
from app.models.user import User
from app.models.course import Course
from app.models.module import Module
from app.models.enrollment import Enrollment
from app.models.assignment import Assignment
from app.models.quiz import Quiz
from app.models.notification import Notification
from app.models.progress import Progress
from app.models.document import Document
from app.models.schedule import Schedule

print('Creando todas las tablas...')
Base.metadata.create_all(bind=engine)
print('✅ Tablas creadas/verificadas')
"

# Always run seed to ensure data integrity (seed_data.py handles cleanup internally)
echo "🌱 Ejecutando seed de datos iniciales..."
python seed_data.py

# Start FastAPI server on port 7860 (Hugging Face standard)
echo "🔥 Iniciando servidor FastAPI en puerto 7860..."
uvicorn app.main:app --host 0.0.0.0 --port 7860
