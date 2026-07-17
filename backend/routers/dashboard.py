"""
Dashboard Router - Dashboard summary and chart data.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter

from backend.database.connection import get_db
from backend.services.auth_service import get_current_user
from backend.models.user import User
from backend.models.resume import Resume
from backend.models.resume_score import ResumeScore
from backend.models.skill import Skill

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary")
def dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get dashboard summary data for the current user."""
    # Resume count
    total_resumes = db.query(func.count(Resume.id)).filter(
        Resume.user_id == current_user.id
    ).scalar()

    # Analysis count
    total_analyses = (
        db.query(func.count(ResumeScore.id))
        .join(Resume, Resume.id == ResumeScore.resume_id)
        .filter(Resume.user_id == current_user.id)
        .scalar()
    )

    # Average and best scores
    score_stats = (
        db.query(
            func.avg(ResumeScore.overall_score),
            func.max(ResumeScore.overall_score),
        )
        .join(Resume, Resume.id == ResumeScore.resume_id)
        .filter(Resume.user_id == current_user.id)
        .first()
    )

    average_score = round(score_stats[0] or 0, 2)
    best_score = round(score_stats[1] or 0, 2)

    # Recent scores
    recent_scores = (
        db.query(ResumeScore)
        .join(Resume, Resume.id == ResumeScore.resume_id)
        .filter(Resume.user_id == current_user.id)
        .order_by(ResumeScore.created_at.desc())
        .limit(10)
        .all()
    )

    # Skill distribution
    skills = (
        db.query(Skill.category, func.count(Skill.id))
        .join(Resume, Resume.id == Skill.resume_id)
        .filter(Resume.user_id == current_user.id)
        .group_by(Skill.category)
        .all()
    )

    skill_distribution = {
        (cat or "other").replace("_", " ").title(): count
        for cat, count in skills
    }

    # Top skills
    top_skills = (
        db.query(Skill.name, func.count(Skill.id).label("count"))
        .join(Resume, Resume.id == Skill.resume_id)
        .filter(Resume.user_id == current_user.id)
        .group_by(Skill.name)
        .order_by(func.count(Skill.id).desc())
        .limit(15)
        .all()
    )

    return {
        "total_resumes": total_resumes,
        "total_analyses": total_analyses,
        "average_score": average_score,
        "best_score": best_score,
        "recent_scores": [
            {
                "id": s.id,
                "resume_id": s.resume_id,
                "jd_id": s.jd_id,
                "overall_score": s.overall_score,
                "match_percentage": s.match_percentage,
                "created_at": s.created_at.isoformat(),
            }
            for s in recent_scores
        ],
        "skill_distribution": skill_distribution,
        "top_skills": [
            {"name": name, "count": count}
            for name, count in top_skills
        ],
    }


@router.get("/charts")
def dashboard_charts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get chart-ready data for the dashboard."""
    # Score history over time
    scores = (
        db.query(ResumeScore)
        .join(Resume, Resume.id == ResumeScore.resume_id)
        .filter(Resume.user_id == current_user.id)
        .order_by(ResumeScore.created_at.asc())
        .all()
    )

    score_history = [
        {
            "date": s.created_at.isoformat(),
            "overall": s.overall_score,
            "skills": s.skills_score,
            "experience": s.experience_score,
            "education": s.education_score,
            "keywords": s.keyword_score,
        }
        for s in scores
    ]

    # Skill radar data (latest resume)
    latest_resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.uploaded_at.desc())
        .first()
    )

    radar_data = {}
    if latest_resume and latest_resume.skills:
        category_counts = Counter()
        for skill in latest_resume.skills:
            cat = (skill.category or "other").replace("_", " ").title()
            category_counts[cat] += 1
        radar_data = dict(category_counts)

    return {
        "score_history": score_history,
        "skill_radar": radar_data,
    }
