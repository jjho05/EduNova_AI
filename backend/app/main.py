from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .config import settings
from .database import engine, Base

# Import models to create tables
from .models import (
    user, course, quiz, schedule, module, notification, 
    assignment, progress, document, quiz_attempt, enrollment,
    question_statistics, course_statistics, activity_log
)

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Generador de Contenido Educativo Inteligente API",
    description="API para plataforma educativa con Gemini AI",
    version="1.0.0",
    docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
    redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
    openapi_url=None if settings.ENVIRONMENT == "production" else "/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Hugging Face Spaces
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from .routes import (
    auth, users, courses, quizzes, ai, schedules, notifications, 
    assignments, progress, documents, statistics, quiz_attempts, enrollments
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(quizzes.router, prefix="/api/quizzes", tags=["Quizzes"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(schedules.router, prefix="/api", tags=["Schedules & Rubrics"])
app.include_router(notifications.router, prefix="/api", tags=["Notifications"])
app.include_router(assignments.router, prefix="/api", tags=["Assignments"])
app.include_router(progress.router, prefix="/api", tags=["Progress"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(statistics.router, prefix="/api", tags=["Statistics"])
app.include_router(quiz_attempts.router, prefix="/api", tags=["Quiz Attempts"])
app.include_router(enrollments.router, prefix="/api", tags=["Enrollments"])

# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

# Mount static files (Flutter Web)
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")
    app.mount("/canvaskit", StaticFiles(directory=str(static_dir / "canvaskit")), name="canvaskit")
    
    # Serve index.html for all non-API routes (SPA support)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't intercept API routes
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi"):
            return {"error": "Not found"}
        
        # Serve static files if they exist
        file_path = static_dir / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Otherwise serve index.html (SPA routing)
        return FileResponse(static_dir / "index.html")
else:
    # Fallback if static directory doesn't exist
    @app.get("/")
    def read_root():
        return {
            "message": "Generador de Contenido Educativo Inteligente API",
            "version": "1.0.0",
            "docs": "/docs",
            "note": "Frontend not built. Run 'flutter build web' in frontend_flutter/"
        }
