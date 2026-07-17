"""
Admin Router - User management, analytics, and platform stats.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.services.auth_service import get_admin_user
from backend.services.admin_service import (
    get_all_users, delete_user, get_platform_analytics,
    get_trending_skills, get_all_resumes, get_candidate_rankings,
)
from backend.models.user import User

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/users")
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """List all users (admin only)."""
    users = get_all_users(db, skip, limit)
    return [
        {
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "role": u.role.value if u.role else "user",
            "is_active": u.is_active,
            "created_at": u.created_at.isoformat(),
        }
        for u in users
    ]


@router.delete("/users/{user_id}")
def remove_user(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Delete a user (admin only)."""
    delete_user(db, user_id)
    return {"message": "User deleted successfully."}


@router.get("/analytics")
def analytics(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Get platform-wide analytics."""
    return get_platform_analytics(db)


@router.get("/resumes")
def list_all_resumes(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """List all uploaded resumes (admin only)."""
    resumes = get_all_resumes(db, skip, limit)
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "filename": r.filename,
            "candidate_name": r.candidate_name,
            "candidate_email": r.candidate_email,
            "uploaded_at": r.uploaded_at.isoformat(),
        }
        for r in resumes
    ]


@router.get("/skills/trending")
def trending_skills(
    limit: int = Query(20, ge=1, le=50),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Get trending/most common skills across all resumes."""
    return get_trending_skills(db, limit)


@router.get("/ranking")
def candidate_ranking(
    jd_id: Optional[int] = None,
    limit: int = Query(20, ge=1, le=50),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Get candidate rankings by ATS score."""
    return get_candidate_rankings(db, jd_id, limit)
