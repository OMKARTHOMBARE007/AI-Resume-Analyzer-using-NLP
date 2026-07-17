"""
Resume Service - Resume CRUD operations and processing.
"""

from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile

from backend.models.resume import Resume
from backend.models.skill import Skill
from backend.models.certification import Certification
from backend.utils.file_handler import FileHandler
from backend.utils.resume_parser import parse_resume


async def upload_and_parse_resume(
    db: Session,
    file: UploadFile,
    user_id: int,
) -> Resume:
    """Upload, save, and parse a resume file."""

    # Save file to disk
    filename, file_path, file_size = await FileHandler.save_file(file, user_id)
    file_type = filename.rsplit('.', 1)[-1] if '.' in filename else ''

    # Parse resume
    try:
        parsed_result = parse_resume(file_path, file_type)
    except Exception as e:
        # Clean up file on parse failure
        FileHandler.delete_file(file_path)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse resume: {str(e)}",
        )

    # Create resume record
    resume = Resume(
        user_id=user_id,
        filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        file_type=file_type,
        raw_text=parsed_result.get("raw_text", ""),
        parsed_data=parsed_result.get("parsed_data", {}),
        candidate_name=parsed_result.get("candidate_name"),
        candidate_email=parsed_result.get("candidate_email"),
        candidate_phone=parsed_result.get("candidate_phone"),
        candidate_address=parsed_result.get("candidate_address"),
        total_experience_years=parsed_result.get("total_experience_years"),
        highest_education=parsed_result.get("highest_education"),
    )
    db.add(resume)
    db.flush()

    # Save extracted skills
    parsed_data = parsed_result.get("parsed_data", {})
    for skill_data in parsed_data.get("skills", []):
        skill = Skill(
            resume_id=resume.id,
            name=skill_data.get("name", ""),
            category=skill_data.get("category", ""),
            proficiency_level=skill_data.get("proficiency", "Intermediate"),
        )
        db.add(skill)

    # Save extracted certifications
    for cert_data in parsed_data.get("certifications", []):
        cert = Certification(
            resume_id=resume.id,
            name=cert_data.get("name", ""),
            issuer=cert_data.get("issuer", ""),
            date=cert_data.get("date", ""),
        )
        db.add(cert)

    db.commit()
    db.refresh(resume)
    return resume


def get_user_resumes(db: Session, user_id: int) -> List[Resume]:
    """Get all resumes for a user."""
    return (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .order_by(Resume.uploaded_at.desc())
        .all()
    )


def get_resume_by_id(db: Session, resume_id: int, user_id: int) -> Resume:
    """Get a specific resume by ID."""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == user_id,
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )
    return resume


def delete_resume(db: Session, resume_id: int, user_id: int) -> bool:
    """Delete a resume and its file."""
    resume = get_resume_by_id(db, resume_id, user_id)

    # Delete file from disk
    FileHandler.delete_file(resume.file_path)

    # Delete from database (cascade will delete skills, certs, scores)
    db.delete(resume)
    db.commit()
    return True
