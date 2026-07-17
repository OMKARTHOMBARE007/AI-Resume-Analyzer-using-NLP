"""
Admin Service - Admin panel operations and analytics.
"""

from typing import Dict, Any, List

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from backend.models.user import User
from backend.models.resume import Resume
from backend.models.resume_score import ResumeScore
from backend.models.skill import Skill
from backend.models.job_description import JobDescription


def get_all_users(db: Session, skip: int = 0, limit: int = 50) -> List[User]:
    """Get all users (admin only)."""
    return db.query(User).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    db.delete(user)
    db.commit()
    return True


def get_platform_analytics(db: Session) -> Dict[str, Any]:
    """Get platform-wide analytics."""
    total_users = db.query(func.count(User.id)).scalar()
    total_resumes = db.query(func.count(Resume.id)).scalar()
    total_jds = db.query(func.count(JobDescription.id)).scalar()
    total_analyses = db.query(func.count(ResumeScore.id)).scalar()

    avg_score = db.query(func.avg(ResumeScore.overall_score)).scalar() or 0

    # Score distribution
    score_ranges = {
        "0-20": db.query(func.count(ResumeScore.id)).filter(ResumeScore.overall_score <= 20).scalar(),
        "21-40": db.query(func.count(ResumeScore.id)).filter(ResumeScore.overall_score.between(21, 40)).scalar(),
        "41-60": db.query(func.count(ResumeScore.id)).filter(ResumeScore.overall_score.between(41, 60)).scalar(),
        "61-80": db.query(func.count(ResumeScore.id)).filter(ResumeScore.overall_score.between(61, 80)).scalar(),
        "81-100": db.query(func.count(ResumeScore.id)).filter(ResumeScore.overall_score > 80).scalar(),
    }

    return {
        "total_users": total_users,
        "total_resumes": total_resumes,
        "total_job_descriptions": total_jds,
        "total_analyses": total_analyses,
        "average_score": round(avg_score, 2),
        "score_distribution": score_ranges,
    }


def get_trending_skills(db: Session, limit: int = 20) -> List[Dict[str, Any]]:
    """Get most common skills across all resumes."""
    results = (
        db.query(Skill.name, Skill.category, func.count(Skill.id).label("count"))
        .group_by(Skill.name, Skill.category)
        .order_by(func.count(Skill.id).desc())
        .limit(limit)
        .all()
    )

    return [
        {"name": name, "category": category, "count": count}
        for name, category, count in results
    ]


def get_all_resumes(db: Session, skip: int = 0, limit: int = 50) -> List[Resume]:
    """Get all resumes (admin only)."""
    return (
        db.query(Resume)
        .order_by(Resume.uploaded_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_candidate_rankings(db: Session, jd_id: int = None, limit: int = 20) -> List[Dict]:
    """Get candidate rankings based on scores."""
    query = (
        db.query(
            ResumeScore.resume_id,
            ResumeScore.overall_score,
            Resume.candidate_name,
            Resume.candidate_email,
            Resume.filename,
        )
        .join(Resume, Resume.id == ResumeScore.resume_id)
    )

    if jd_id:
        query = query.filter(ResumeScore.jd_id == jd_id)

    results = (
        query.order_by(ResumeScore.overall_score.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "resume_id": r.resume_id,
            "overall_score": r.overall_score,
            "candidate_name": r.candidate_name or "Unknown",
            "candidate_email": r.candidate_email or "",
            "filename": r.filename,
        }
        for r in results
    ]
