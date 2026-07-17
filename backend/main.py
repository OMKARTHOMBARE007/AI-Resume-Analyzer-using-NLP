import sys
from pathlib import Path

# Add project root to sys.path to support running from either project root or backend folder
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from backend.config import settings
from backend.database.connection import init_db, SessionLocal
from backend.database.seed import run_seeds

from backend.routers import auth, resume, job_description, analysis, dashboard, report, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    print(f"[STARTUP] {settings.APP_NAME} v{settings.APP_VERSION}")
    init_db()
    print("[STARTUP] Database tables created.")

    # Seed default data
    db = SessionLocal()
    try:
        run_seeds(db)
    finally:
        db.close()

    yield

    # Shutdown
    print("[SHUTDOWN] Application shutting down.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Resume Analyzer using NLP - Analyze resumes, compare with job descriptions, calculate ATS scores, and get intelligent recommendations.",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static/upload directories
import os
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.REPORT_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="uploads")
app.mount("/reports", StaticFiles(directory=str(settings.REPORT_DIR)), name="reports")

# Register routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(job_description.router)
app.include_router(analysis.router)
app.include_router(dashboard.router)
app.include_router(report.router)
app.include_router(admin.router)


@app.get("/", tags=["Root"])
def root():
    """API root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running",
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
