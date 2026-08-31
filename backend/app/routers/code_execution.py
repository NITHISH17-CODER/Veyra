"""
Code Execution Router — API endpoints for online compiler execution and code persistence.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.services import code_execution_service as service

router = APIRouter(prefix="/api/code", tags=["Code Execution"])


# ── Pydantic Request & Response Schemas ───────────────────────────────────────

class CodeExecuteRequest(BaseModel):
    lessonId: Optional[int] = Field(None, description="Optional ID of lesson being attempted")
    language: str = Field(..., description="Programming language key (e.g. python, javascript)")
    version: Optional[str] = Field(None, description="Language version selected by user")
    sourceCode: str = Field(..., max_length=65536, description="Source code text to execute")
    stdin: Optional[str] = Field("", max_length=10240, description="STDIN input to program")


class CodeSaveRequest(BaseModel):
    language: str = Field(..., description="Language identifier")
    version: Optional[str] = Field(None, description="Language version")
    code: str = Field(..., max_length=65536, description="Source code to save")
    stdin: Optional[str] = Field("", max_length=10240, description="STDIN string to save")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/languages", summary="Get supported languages and versions")
def get_supported_languages_endpoint():
    """Returns list of supported execution languages, available versions, and Monaco editor metadata."""
    return service.get_supported_languages()


@router.post("/execute", summary="Execute user code safely")
def execute_code_endpoint(
    payload: CodeExecuteRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Executes untrusted user code in an isolated sandbox.
    Resolves user identity from authenticated JWT token.
    Enforces per-user rate limiting.
    """
    if not service.check_rate_limit(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many code executions. Please wait a moment and try again."
        )

    if not payload.sourceCode.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source code cannot be empty."
        )

    result = service.execute_code_sandboxed(
        language=payload.language,
        version=payload.version or "",
        source_code=payload.sourceCode,
        stdin=payload.stdin or ""
    )

    return result


@router.get("/lessons/{lesson_id}/saved", summary="Get saved code for a lesson")
def get_saved_code_endpoint(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves saved draft code for current user and lesson."""
    record = service.get_user_lesson_code(db, user_id=current_user.id, lesson_id=lesson_id)
    if not record:
        return {
            "has_saved_code": False,
            "language": None,
            "version": None,
            "code": None,
            "stdin": None
        }

    return {
        "has_saved_code": True,
        "language": record.language,
        "version": record.version,
        "code": record.code,
        "stdin": record.stdin,
        "updated_at": record.updated_at.isoformat() if record.updated_at else None
    }


@router.post("/lessons/{lesson_id}/save", summary="Save user code draft for a lesson")
def save_code_endpoint(
    lesson_id: int,
    payload: CodeSaveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Persists user draft code for a lesson in MySQL."""
    record = service.save_user_lesson_code(
        db=db,
        user_id=current_user.id,
        lesson_id=lesson_id,
        language=payload.language,
        version=payload.version,
        code=payload.code,
        stdin=payload.stdin
    )

    return {
        "success": True,
        "message": "Code saved successfully.",
        "saved_at": record.updated_at.isoformat() if record.updated_at else None
    }
