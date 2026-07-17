"""
Authentication Router - Register, Login, Profile, Forgot Password.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.user import (
    UserRegister, UserLogin, UserResponse, UserUpdate,
    TokenResponse, ForgotPasswordRequest, ResetPasswordRequest,
)
from backend.services.auth_service import (
    register_user, login_user, get_current_user,
    generate_reset_token, reset_password,
)
from backend.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account."""
    user = register_user(db, data.email, data.name, data.password)
    login_data = login_user(db, data.email, data.password)
    return TokenResponse(
        access_token=login_data["access_token"],
        refresh_token=login_data["refresh_token"],
        user=UserResponse.model_validate(login_data["user"]),
    )


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password."""
    login_data = login_user(db, data.email, data.password)
    return TokenResponse(
        access_token=login_data["access_token"],
        refresh_token=login_data["refresh_token"],
        user=UserResponse.model_validate(login_data["user"]),
    )


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile."""
    return UserResponse.model_validate(current_user)


@router.put("/profile", response_model=UserResponse)
def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user's profile."""
    if data.name is not None:
        current_user.name = data.name
    if data.phone is not None:
        current_user.phone = data.phone
    if data.bio is not None:
        current_user.bio = data.bio
    if data.avatar_url is not None:
        current_user.avatar_url = data.avatar_url

    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Request a password reset token."""
    token = generate_reset_token(db, data.email)
    # Always return success to not reveal if email exists
    return {"message": "If the email exists, a reset link has been sent.", "reset_token": token}


@router.post("/reset-password")
def reset_password_endpoint(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using a reset token."""
    reset_password(db, data.token, data.new_password)
    return {"message": "Password reset successfully."}
