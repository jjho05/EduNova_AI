# Changelog

Todos los cambios notables del proyecto se documentan en este archivo.

## [1.0.0] - 2026-01-21

### 🎉 Lanzamiento Inicial

#### Agregado
- Sistema completo de backend con FastAPI
- 14 modelos de base de datos
- 42 endpoints API RESTful
- Sistema de autenticación JWT
- 9 servicios de IA con Gemini
- Procesamiento automático de retículas
- Procesamiento automático de syllabi
- Gemini Vision para OCR de PDFs escaneados
- Sistema completo de estadísticas
- Tracking de quiz attempts
- Sistema de inscripciones (enrollments)
- Detección de estudiantes en riesgo
- Dashboard del profesor con alertas
- Context manager con caché para IA
- Frontend Flutter con 13 pantallas
- Gráficas interactivas con fl_chart
- Sistema de navegación con GoRouter
- State management con Provider

#### Características Principales

**Backend:**
- ✅ PDFExtractor - Extracción de texto de PDFs
- ✅ DocumentProcessor - Procesamiento general con Gemini
- ✅ CurriculumProcessor - Procesamiento de retículas
- ✅ SyllabusProcessor - Procesamiento completo de syllabi
- ✅ QuizService - Generación de quizzes
- ✅ ScheduleService - Generación de cronogramas
- ✅ StatisticsService - Análisis completo de rendimiento
- ✅ GeminiVisionService - OCR para documentos escaneados
- ✅ AIContextManager - Gestión de contexto para IA

**Frontend:**
- ✅ LoginScreen y RegisterScreen
- ✅ TeacherDashboard y StudentDashboard
- ✅ CoursesListScreen y CreateCourseScreen
- ✅ QuizStatisticsScreen con visualizaciones
- ✅ QuizScreen interactivo con timer
- ✅ ProgressScreen con gráficas
- ✅ UploadDocumentScreen
- ✅ ChatScreen con IA
- ✅ NotificationsScreen

**Estadísticas:**
- ✅ Análisis completo por quiz
- ✅ Estadísticas por pregunta
- ✅ Ranking de estudiantes
- ✅ Detección de estudiantes en riesgo
- ✅ Dashboard del profesor

#### Endpoints API

**Documentos (7):**
- POST /api/documents/upload
- POST /api/documents/{id}/process
- POST /api/documents/{id}/process-curriculum
- POST /api/documents/{id}/process-syllabus
- GET /api/documents
- GET /api/documents/{id}
- DELETE /api/documents/{id}

**Estadísticas (6):**
- GET /api/quizzes/{id}/statistics
- GET /api/quizzes/{id}/question-stats
- GET /api/quizzes/{id}/student-comparison
- GET /api/courses/{id}/statistics
- GET /api/analytics/at-risk-students
- GET /api/teacher/dashboard

**Quiz Attempts (4):**
- POST /api/quizzes/{id}/start
- POST /api/quiz-attempts/{id}/submit
- GET /api/quiz-attempts/{id}
- GET /api/my-quiz-attempts

**Enrollments (4):**
- POST /api/enrollments
- GET /api/my-enrollments
- GET /api/courses/{id}/enrollments
- DELETE /api/enrollments/{id}

**Otros (21):**
- Auth, Users, Courses, Quizzes, AI, Schedules, Notifications, Assignments, Progress

#### Tecnologías

**Backend:**
- FastAPI 0.109
- SQLAlchemy 2.0
- Google Generative AI 0.3
- PyPDF2 3.0
- pdf2image 1.16
- Pillow 10.1
- python-jose (JWT)

**Frontend:**
- Flutter 3.x
- fl_chart 0.66
- dio 5.4
- provider 6.1
- go_router 13.0
- file_picker 6.1

#### Métricas
- ~16,000 líneas de código
- 14 modelos de BD
- 9 servicios
- 10 rutas
- 13 pantallas
- 98% completado

---

## [Próximas Versiones]

### [1.1.0] - Planeado
- [ ] Tests unitarios completos
- [ ] Tests de integración
- [ ] Optimizaciones de rendimiento
- [ ] Paginación en endpoints
- [ ] Rate limiting para IA
- [ ] Logs estructurados
- [ ] Métricas de uso

### [1.2.0] - Futuro
- [ ] Versionado de contenido
- [ ] Portafolios de evidencia
- [ ] Exportación de reportes (PDF/Excel)
- [ ] Notificaciones push
- [ ] Modo offline
- [ ] Sincronización automática
