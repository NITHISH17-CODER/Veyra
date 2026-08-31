"""
Authentication Router — Registration, Login, and Profile endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.session import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description="Registers a new user with name, email, and password. Returns JWT access token upon successful registration.",
)
def register_user(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    # Normalize email
    normalized_email = payload.email.strip().lower()

    # Check for duplicate email before insert
    existing_user = db.query(User).filter(User.email == normalized_email).first()
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "code": "EMAIL_ALREADY_EXISTS",
                "message": "An account with this email already exists. Please log in.",
                "detail": "An account with this email already exists. Please log in.",
            },
        )

    # Hash password securely with bcrypt
    try:
        hashed = hash_password(payload.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    # Create user record
    new_user = User(
        name=payload.name.strip(),
        email=normalized_email,
        password_hash=hashed,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "code": "EMAIL_ALREADY_EXISTS",
                "message": "An account with this email already exists. Please log in.",
                "detail": "An account with this email already exists. Please log in.",
            },
        )

    # Issue JWT token
    access_token = create_access_token(subject=new_user.id)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(new_user),
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and obtain JWT token",
    description="Validates email and password credentials, returning a signed JWT access token.",
)
def login_user(
    payload: UserLoginRequest,
    db: Session = Depends(get_db),
):
    normalized_email = payload.email.strip().lower()

    user = db.query(User).filter(User.email == normalized_email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.id)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user profile",
    description="Returns the profile information of the user authenticated via Bearer JWT.",
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

