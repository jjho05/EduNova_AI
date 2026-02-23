# 🎓 Sistema Educativo Inteligente con IA

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![Flutter](https://img.shields.io/badge/Flutter-3.x-blue.svg)](https://flutter.dev/)
[![Gemini AI](https://img.shields.io/badge/Gemini-1.5%20Pro-orange.svg)](https://ai.google.dev/)

Sistema educativo completo con inteligencia artificial para automatizar la creación de contenido, generar quizzes, procesar documentos y analizar el rendimiento estudiantil.

---

## ✨ Características Principales

### 🤖 **Inteligencia Artificial**
- ✅ Procesamiento automático de retículas → Crea 40+ cursos
- ✅ Procesamiento de syllabi → Genera módulos completos
- ✅ OCR con Gemini Vision para PDFs escaneados
- ✅ Generación de quizzes contextualizados
- ✅ Chat educativo con IA
- ✅ Context manager con caché inteligente

### 📊 **Estadísticas Avanzadas**
- ✅ Análisis completo por quiz (promedio, mediana, distribución)
- ✅ Estadísticas por pregunta (% aciertos, distribución de respuestas)
- ✅ Ranking de estudiantes con percentiles
- ✅ Detección automática de estudiantes en riesgo
- ✅ Dashboard del profesor con alertas

### 👨‍🏫 **Para Profesores**
- ✅ Subir retículas y crear cursos automáticamente
- ✅ Generar contenido educativo con IA
- ✅ Crear quizzes personalizados
- ✅ Ver estadísticas detalladas
- ✅ Identificar estudiantes que necesitan apoyo
- ✅ Generar cronogramas y rúbricas

### 👨‍🎓 **Para Estudiantes**
- ✅ Inscribirse a cursos
- ✅ Tomar quizzes interactivos con timer
- ✅ Ver resultados y retroalimentación inmediata
- ✅ Seguir progreso con gráficas
- ✅ Chat con IA para resolver dudas

---

## 🏗️ Arquitectura

### **Backend (FastAPI + MySQL)**
- 14 modelos de base de datos
- 42 endpoints API RESTful
- 9 servicios de IA
- Autenticación JWT
- Sistema de estadísticas completo

### **Frontend (Flutter)**
- 13 pantallas responsivas
- Gráficas interactivas (fl_chart)
- State management con Provider
- Navegación con GoRouter

---

## 🚀 Instalación Rápida

### **Prerrequisitos**
- Python 3.11+
- MySQL 8.0+
- Flutter 3.x
- API Key de Google Gemini

### **1. Backend**

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Mac/Linux
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales:
# - GEMINI_API_KEY
# - DATABASE_URL
# - SECRET_KEY

# Crear base de datos
mysql -u root -p
CREATE DATABASE educativo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Ejecutar servidor
uvicorn app.main:app --reload
```

**Backend corriendo en:** `http://localhost:8000`  
**Documentación API:** `http://localhost:8000/docs`

### **2. Frontend**

```bash
cd frontend_flutter

# Instalar dependencias
flutter pub get

# Ejecutar en Chrome
flutter run -d chrome

# O en dispositivo móvil
flutter run
```

---

## 📚 Uso

### **Profesor - Crear Cursos desde Retícula**

1. **Login** como profesor
2. **Subir Documento** → Seleccionar tipo "Retícula"
3. **Procesar con IA**
4. ✅ Sistema crea automáticamente todos los cursos

### **Profesor - Generar Contenido de Curso**

1. **Seleccionar curso**
2. **Subir programa de materia** (PDF)
3. Sistema detecta si es escaneado
4. Usa OCR si es necesario
5. ✅ Crea módulos automáticamente con contenido

### **Profesor - Ver Estadísticas de Quiz**

1. **Ir a quiz**
2. **Ver Estadísticas**
3. ✅ Ve distribución completa, análisis por pregunta, ranking

### **Estudiante - Tomar Quiz**

1. **Inscribirse a curso**
2. **Seleccionar quiz**
3. **Iniciar** (se guarda intento en BD)
4. **Responder preguntas**
5. **Finalizar**
6. ✅ Ver resultados y retroalimentación

---

## 📊 Endpoints API Principales

### **Documentos**
```
POST /api/documents/upload
POST /api/documents/{id}/process-curriculum
POST /api/documents/{id}/process-syllabus
```

### **Estadísticas**
```
GET /api/quizzes/{id}/statistics
GET /api/quizzes/{id}/question-stats
GET /api/quizzes/{id}/student-comparison
GET /api/analytics/at-risk-students
GET /api/teacher/dashboard
```

### **Quiz Attempts**
```
POST /api/quizzes/{id}/start
POST /api/quiz-attempts/{id}/submit
GET /api/my-quiz-attempts
```

### **Enrollments**
```
POST /api/enrollments
GET /api/my-enrollments
```

**Documentación completa:** `http://localhost:8000/docs`

---

## 🗄️ Modelos de Base de Datos

- **User** - Usuarios (estudiantes/profesores)
- **Course** - Cursos/Materias
- **Module** - Módulos/Unidades
- **Quiz** - Exámenes
- **QuizAttempt** - Intentos de quiz
- **QuestionStatistics** - Estadísticas por pregunta
- **Enrollment** - Inscripciones
- **CourseStatistics** - Estadísticas del curso
- **ActivityLog** - Logs de actividad
- **Document** - Documentos subidos
- **Schedule** - Cronogramas
- **Notification** - Notificaciones
- **Assignment** - Tareas
- **Progress** - Progreso

---

## 🔧 Configuración

### **Variables de Entorno (.env)**

```env
# Gemini AI
GEMINI_API_KEY=tu_api_key_aqui

# Base de Datos
DATABASE_URL=mysql+pymysql://user:password@localhost/educativo_db

# JWT
SECRET_KEY=tu_secret_key_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Entorno
ENVIRONMENT=development

# Storage (opcional para producción)
S3_BUCKET_NAME=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

---

## 📦 Dependencias Principales

### **Backend**
- FastAPI 0.109
- SQLAlchemy 2.0
- Google Generative AI 0.3
- PyPDF2 3.0
- pdf2image 1.16
- Pillow 10.1
- python-jose (JWT)

### **Frontend**
- fl_chart 0.66 (gráficas)
- dio 5.4 (HTTP)
- provider 6.1 (state management)
- go_router 13.0 (navegación)
- file_picker 6.1

---

## 🎯 Roadmap

### **Completado (98%)**
- ✅ Backend completo con 42 endpoints
- ✅ Sistema de estadísticas
- ✅ Gemini Vision (OCR)
- ✅ Procesamiento de retículas y syllabi
- ✅ Context manager
- ✅ Frontend con visualizaciones

### **Pendiente (2%)**
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Optimizaciones (paginación, rate limiting)
- [ ] Logs estructurados

---

## 📝 Licencia

Este proyecto es de código abierto bajo licencia MIT.

---

## 👨‍💻 Autor

Desarrollado con ❤️ usando FastAPI, Flutter y Gemini AI

---

## 🆘 Soporte

Para reportar bugs o solicitar features, por favor crea un issue en el repositorio.

---

## 📸 Screenshots

### Dashboard del Profesor
![Dashboard](screenshots/teacher_dashboard.png)

### Estadísticas de Quiz
![Statistics](screenshots/quiz_statistics.png)

### Análisis por Pregunta
![Question Analysis](screenshots/question_analysis.png)

### Progreso del Estudiante
![Student Progress](screenshots/student_progress.png)

---

**Estado:** 98% Completo ✅  
**Listo para:** Testing y Despliegue 🚀
