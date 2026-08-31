"""
PathPilot AI — FastAPI Backend Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.database.connection import engine
from app.database.base import Base
import app.models  # Ensure all models are loaded
from app.routers import (
    auth_router,
    onboarding_router,
    profile_router,
    skills_router,
    user_skills_router,
    recommendations_router,
    learning_path_router,
    courses_router,
    projects_router,
    progress_router,
    assessments_router,
    chat_router,
    feedback_router,
    course_learning_router,
    streak_router,
    notifications_router,
    certificates_router,
    code_execution_router,
    news_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database schema is created on startup
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not create tables on startup ({e}). Verify DB connection.")
    yield


import os
from fastapi.staticfiles import StaticFiles

# Ensure upload directories exist
os.makedirs("uploads/avatars", exist_ok=True)
os.makedirs("uploads/resumes", exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered personalized learning path generator",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ---------------------------------------------------------------------------
# CORS — allow Vite dev-server (http://localhost:5173) and configured origins
# ---------------------------------------------------------------------------
allowed_origins = list(set(settings.CORS_ORIGINS + [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "https://veyra3.netlify.app",
]))


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Custom Exception Handlers for Standardized API Responses
# ---------------------------------------------------------------------------
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Formats Pydantic validation errors into clean field-level error messages."""
    field_errors = {}
    for error in exc.errors():
        loc = error.get("loc", [])
        field_name = str(loc[-1]) if loc else "general"
        msg = error.get("msg", "Invalid value")
        # Clean up pydantic prefix if present e.g. "Value error, "
        if msg.startswith("Value error, "):
            msg = msg[len("Value error, "):]
        field_errors[field_name] = msg

    # Pick the most relevant message for top-level summary
    summary_message = "Please correct the highlighted fields."
    if "password" in field_errors:
        summary_message = field_errors["password"]
    elif "email" in field_errors:
        summary_message = field_errors["email"]
    elif "name" in field_errors:
        summary_message = field_errors["name"]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "code": "VALIDATION_ERROR",
            "message": summary_message,
            "errors": field_errors,
            "detail": summary_message,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Ensures HTTP exceptions maintain standard schema compatibility."""
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
            headers=exc.headers,
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "code": "HTTP_ERROR" if exc.status_code != 401 else "UNAUTHORIZED",
            "message": exc.detail,
            "detail": exc.detail,
        },
        headers=exc.headers,
    )


# ---------------------------------------------------------------------------
# Include API Routers
# ---------------------------------------------------------------------------
app.include_router(auth_router)
app.include_router(onboarding_router)
app.include_router(profile_router)
app.include_router(skills_router)
app.include_router(user_skills_router)
app.include_router(recommendations_router)
app.include_router(learning_path_router)
app.include_router(course_learning_router)
app.include_router(courses_router)
app.include_router(projects_router)
app.include_router(progress_router)
app.include_router(assessments_router)
app.include_router(chat_router)
app.include_router(feedback_router)
app.include_router(streak_router)
app.include_router(notifications_router)
app.include_router(certificates_router)
app.include_router(code_execution_router)
app.include_router(news_router)


# ---------------------------------------------------------------------------
# Health-check endpoints
# ---------------------------------------------------------------------------
@app.get("/api/health", tags=["Health"])
async def health_check():
    """Return a simple health-check response."""
    return {
        "status": "ok",
        "message": "PathPilot AI backend is running",
    }


@app.get("/api/health/database", tags=["Health"])
async def database_health_check():
    """Verify that the backend can reach the MySQL database."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
        }
    except Exception as exc:
        error_message = str(exc)
        if "@" in error_message:
            error_message = "Unable to connect to the database. Check your DATABASE_URL in .env."
        return {
            "status": "error",
            "database": "disconnected",
            "detail": error_message,
        }
