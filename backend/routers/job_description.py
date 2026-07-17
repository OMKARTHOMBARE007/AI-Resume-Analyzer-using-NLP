"""
Job Description Router - Create, list, get, delete job descriptions.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.services.auth_service import get_current_user
from backend.services.jd_service import (
    create_job_description, get_user_jds, get_jd_by_id, delete_jd,
)
from backend.schemas.job_description import JobDescriptionCreate
from backend.models.user import User

router = APIRouter(prefix="/api/jd", tags=["Job Description"])


@router.post("/create")
def create_jd(
    data: JobDescriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create and process a job description."""
    jd = create_job_description(
        db, current_user.id, data.title, data.raw_text, data.company
    )
    return {
        "id": jd.id,
        "title": jd.title,
        "company": jd.company,
        "required_skills": jd.required_skills,
        "required_experience": jd.required_experience,
        "required_education": jd.required_education,
        "keywords": jd.keywords,
        "created_at": jd.created_at.isoformat(),
        "message": "Job description created and processed successfully",
    }


@router.get("/list")
def list_jds(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all job descriptions for the current user."""
    jds = get_user_jds(db, current_user.id)
    return [
        {
            "id": jd.id,
            "title": jd.title,
            "company": jd.company,
            "required_skills_count": len(jd.required_skills) if jd.required_skills else 0,
            "created_at": jd.created_at.isoformat(),
        }
        for jd in jds
    ]


@router.get("/{jd_id}")
def get_jd(
    jd_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get detailed job description data."""
    jd = get_jd_by_id(db, jd_id, current_user.id)
    return {
        "id": jd.id,
        "title": jd.title,
        "company": jd.company,
        "raw_text": jd.raw_text,
        "parsed_data": jd.parsed_data,
        "required_skills": jd.required_skills,
        "required_experience": jd.required_experience,
        "required_education": jd.required_education,
        "keywords": jd.keywords,
        "created_at": jd.created_at.isoformat(),
    }


@router.delete("/{jd_id}")
def remove_jd(
    jd_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a job description."""
    delete_jd(db, jd_id, current_user.id)
    return {"message": "Job description deleted successfully."}
