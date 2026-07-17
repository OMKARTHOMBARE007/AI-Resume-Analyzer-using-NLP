"""
Job Description Service - JD processing and CRUD operations.
"""

from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.models.job_description import JobDescription
from backend.nlp.pipeline import nlp_pipeline


def create_job_description(
    db: Session,
    user_id: int,
    title: str,
    raw_text: str,
    company: str = None,
) -> JobDescription:
    """Create and process a job description."""

    # Process through NLP pipeline
    parsed_data = nlp_pipeline.process_job_description(raw_text)

    jd = JobDescription(
        user_id=user_id,
        title=title,
        company=company,
        raw_text=raw_text,
        parsed_data=parsed_data,
        required_skills=parsed_data.get("required_skills", []),
        required_experience=parsed_data.get("required_experience", ""),
        required_education=parsed_data.get("required_education", ""),
        keywords=parsed_data.get("keywords", []),
    )
    db.add(jd)
    db.commit()
    db.refresh(jd)
    return jd


def get_user_jds(db: Session, user_id: int) -> List[JobDescription]:
    """Get all job descriptions for a user."""
    return (
        db.query(JobDescription)
        .filter(JobDescription.user_id == user_id)
        .order_by(JobDescription.created_at.desc())
        .all()
    )


def get_jd_by_id(db: Session, jd_id: int, user_id: int) -> JobDescription:
    """Get a specific JD by ID."""
    jd = db.query(JobDescription).filter(
        JobDescription.id == jd_id,
        JobDescription.user_id == user_id,
    ).first()

    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found.",
        )
    return jd


def delete_jd(db: Session, jd_id: int, user_id: int) -> bool:
    """Delete a job description."""
    jd = get_jd_by_id(db, jd_id, user_id)
    db.delete(jd)
    db.commit()
    return True
