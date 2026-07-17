"""
Resume Router - Upload, list, get, delete resumes.
"""

from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.services.auth_service import get_current_user
from backend.services.resume_service import (
    upload_and_parse_resume, get_user_resumes,
    get_resume_by_id, delete_resume,
)
from backend.models.user import User

router = APIRouter(prefix="/api/resume", tags=["Resume"])


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload and parse a resume file (PDF or DOCX)."""
    resume = await upload_and_parse_resume(db, file, current_user.id)

    return {
        "id": resume.id,
        "filename": resume.filename,
        "file_type": resume.file_type,
        "file_size": resume.file_size,
        "candidate_name": resume.candidate_name,
        "candidate_email": resume.candidate_email,
        "candidate_phone": resume.candidate_phone,
        "uploaded_at": resume.uploaded_at.isoformat(),
        "message": "Resume uploaded and parsed successfully",
    }


@router.get("/list")
def list_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all resumes for the current user."""
    resumes = get_user_resumes(db, current_user.id)
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "file_type": r.file_type,
            "candidate_name": r.candidate_name,
            "candidate_email": r.candidate_email,
            "total_experience_years": r.total_experience_years,
            "skill_count": len(r.skills) if r.skills else 0,
            "uploaded_at": r.uploaded_at.isoformat(),
        }
        for r in resumes
    ]


@router.get("/{resume_id}")
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get detailed resume data."""
    resume = get_resume_by_id(db, resume_id, current_user.id)
    return {
        "id": resume.id,
        "filename": resume.filename,
        "file_type": resume.file_type,
        "file_size": resume.file_size,
        "raw_text": resume.raw_text,
        "parsed_data": resume.parsed_data,
        "candidate_name": resume.candidate_name,
        "candidate_email": resume.candidate_email,
        "candidate_phone": resume.candidate_phone,
        "candidate_address": resume.candidate_address,
        "total_experience_years": resume.total_experience_years,
        "highest_education": resume.highest_education,
        "uploaded_at": resume.uploaded_at.isoformat(),
        "skills": [
            {"name": s.name, "category": s.category, "proficiency_level": s.proficiency_level}
            for s in resume.skills
        ] if resume.skills else [],
        "certifications": [
            {"name": c.name, "issuer": c.issuer, "date": c.date}
            for c in resume.certifications
        ] if resume.certifications else [],
    }


@router.delete("/{resume_id}")
def remove_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a resume."""
    delete_resume(db, resume_id, current_user.id)
    return {"message": "Resume deleted successfully."}


@router.get("/{resume_id}/download")
def download_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Download the original resume file."""
    resume = get_resume_by_id(db, resume_id, current_user.id)

    import os
    if not os.path.exists(resume.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk.",
        )

    return FileResponse(
        path=resume.file_path,
        filename=resume.filename,
        media_type="application/octet-stream",
    )
