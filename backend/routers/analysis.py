"""
Analysis Router - ATS scoring, matching, and AI suggestions.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.services.auth_service import get_current_user
from backend.services.analysis_service import (
    calculate_ats_score, get_match_result, get_analysis_history,
)
from backend.services.suggestion_service import generate_suggestions
from backend.schemas.score import ScoreRequest
from backend.models.user import User

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.post("/score")
def compute_ats_score(
    data: ScoreRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Calculate ATS score for a resume against a job description."""
    score = calculate_ats_score(db, data.resume_id, data.jd_id, current_user.id)
    return {
        "id": score.id,
        "resume_id": score.resume_id,
        "jd_id": score.jd_id,
        "score_breakdown": {
            "overall_score": score.overall_score,
            "skills_score": score.skills_score,
            "experience_score": score.experience_score,
            "education_score": score.education_score,
            "keyword_score": score.keyword_score,
            "formatting_score": score.formatting_score,
            "projects_score": score.projects_score,
            "certifications_score": score.certifications_score,
        },
        "match_result": {
            "match_percentage": score.match_percentage,
            "semantic_similarity": score.semantic_similarity,
            "matched_skills": score.matched_skills or [],
            "missing_skills": score.missing_skills or [],
            "missing_keywords": score.missing_keywords or [],
            "strengths": score.strengths or [],
            "weaknesses": score.weaknesses or [],
        },
        "created_at": score.created_at.isoformat(),
    }


@router.post("/match")
def match_resume_jd(
    data: ScoreRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get detailed resume vs JD matching results."""
    result = get_match_result(db, data.resume_id, data.jd_id, current_user.id)
    return result


@router.post("/suggestions")
def get_suggestions(
    data: ScoreRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get AI-powered suggestions for resume improvement."""
    result = generate_suggestions(db, data.resume_id, current_user.id, data.jd_id)
    return result


@router.get("/history/{resume_id}")
def analysis_history(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get analysis history for a resume."""
    scores = get_analysis_history(db, resume_id, current_user.id)
    return [
        {
            "id": s.id,
            "jd_id": s.jd_id,
            "overall_score": s.overall_score,
            "match_percentage": s.match_percentage,
            "created_at": s.created_at.isoformat(),
        }
        for s in scores
    ]
