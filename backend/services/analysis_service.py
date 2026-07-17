"""
Analysis Service - ATS scoring, resume-JD matching, and detailed analysis.
"""

from typing import Dict, Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.models.resume import Resume
from backend.models.job_description import JobDescription
from backend.models.resume_score import ResumeScore
from backend.nlp.pipeline import nlp_pipeline


def calculate_ats_score(
    db: Session,
    resume_id: int,
    jd_id: int,
    user_id: int,
) -> ResumeScore:
    """
    Calculate ATS score for a resume against a job description.
    Returns a ResumeScore with detailed breakdowns.
    """
    # Fetch resume and JD
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    jd = db.query(JobDescription).filter(JobDescription.id == jd_id, JobDescription.user_id == user_id).first()
    if not jd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found.")

    resume_data = resume.parsed_data or {}
    jd_data = jd.parsed_data or {}

    # Run comparison
    comparison = nlp_pipeline.compare_resume_jd(
        resume_data, jd_data, resume.raw_text or "", jd.raw_text
    )

    # Calculate individual scores
    skill_comparison = comparison.get("skill_comparison", {})
    keyword_comparison = comparison.get("keyword_comparison", {})
    similarity = comparison.get("similarity", {})

    # Skills Score (30% weight)
    skills_score = min(skill_comparison.get("match_percentage", 0), 100)

    # Keyword Score (20% weight)
    keyword_score = min(keyword_comparison.get("keyword_match_percentage", 0), 100)

    # Experience Score (15% weight)
    experience_score = _calculate_experience_score(resume_data, jd_data)

    # Education Score (10% weight)
    education_score = _calculate_education_score(resume_data, jd_data)

    # Formatting Score (10% weight)
    formatting_score = _calculate_formatting_score(resume_data)

    # Projects Score (10% weight)
    projects_score = _calculate_projects_score(resume_data)

    # Certifications Score (5% weight)
    certifications_score = _calculate_certifications_score(resume_data)

    # Overall ATS Score (weighted average)
    overall_score = (
        skills_score * 0.30 +
        keyword_score * 0.20 +
        experience_score * 0.15 +
        education_score * 0.10 +
        formatting_score * 0.10 +
        projects_score * 0.10 +
        certifications_score * 0.05
    )

    # Semantic similarity boost (up to 10% bonus)
    semantic_boost = similarity.get("semantic_similarity", 0) * 10
    overall_score = min(overall_score + semantic_boost, 100)

    # Create or update score record
    existing_score = db.query(ResumeScore).filter(
        ResumeScore.resume_id == resume_id,
        ResumeScore.jd_id == jd_id,
    ).first()

    if existing_score:
        score = existing_score
    else:
        score = ResumeScore(resume_id=resume_id, jd_id=jd_id)
        db.add(score)

    score.overall_score = round(overall_score, 2)
    score.skills_score = round(skills_score, 2)
    score.experience_score = round(experience_score, 2)
    score.education_score = round(education_score, 2)
    score.keyword_score = round(keyword_score, 2)
    score.formatting_score = round(formatting_score, 2)
    score.projects_score = round(projects_score, 2)
    score.certifications_score = round(certifications_score, 2)
    score.match_percentage = round(similarity.get("match_percentage", 0), 2)
    score.matched_skills = skill_comparison.get("matched", [])
    score.missing_skills = skill_comparison.get("missing", [])
    score.missing_keywords = keyword_comparison.get("missing_keywords", [])
    score.strengths = comparison.get("strengths", [])
    score.weaknesses = comparison.get("weaknesses", [])
    score.semantic_similarity = similarity.get("semantic_similarity", 0)

    db.commit()
    db.refresh(score)
    return score


def get_match_result(
    db: Session,
    resume_id: int,
    jd_id: int,
    user_id: int,
) -> Dict[str, Any]:
    """Get detailed matching results between resume and JD."""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    jd = db.query(JobDescription).filter(JobDescription.id == jd_id, JobDescription.user_id == user_id).first()
    if not jd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found.")

    resume_data = resume.parsed_data or {}
    jd_data = jd.parsed_data or {}

    comparison = nlp_pipeline.compare_resume_jd(
        resume_data, jd_data, resume.raw_text or "", jd.raw_text
    )

    return {
        "resume_id": resume_id,
        "jd_id": jd_id,
        **comparison,
    }


def get_analysis_history(db: Session, resume_id: int, user_id: int):
    """Get all analysis scores for a resume."""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    return (
        db.query(ResumeScore)
        .filter(ResumeScore.resume_id == resume_id)
        .order_by(ResumeScore.created_at.desc())
        .all()
    )


def _calculate_experience_score(resume_data: Dict, jd_data: Dict) -> float:
    """Calculate experience match score."""
    experience = resume_data.get("experience", [])
    if not experience:
        return 20.0  # Base score for having no experience listed

    score = 40.0  # Base for having experience

    # More experience entries = higher score
    score += min(len(experience) * 10, 30)

    # Check for action verbs and quantifiable results
    action_verbs = resume_data.get("action_verbs", {})
    if action_verbs.get("strong_verb_ratio", 0) > 0.5:
        score += 15

    bullet_analysis = resume_data.get("bullet_analysis", {})
    if bullet_analysis.get("with_numbers", 0) > 2:
        score += 15

    return min(score, 100)


def _calculate_education_score(resume_data: Dict, jd_data: Dict) -> float:
    """Calculate education match score."""
    education = resume_data.get("education", [])
    if not education:
        return 30.0

    score = 50.0  # Base for having education

    # Higher degree = higher score
    degree_bonuses = {
        "phd": 50, "ph.d": 50, "doctorate": 50,
        "master": 40, "mba": 40, "m.s": 40, "m.tech": 40,
        "bachelor": 30, "b.s": 30, "b.tech": 30, "b.e": 30,
    }

    for entry in education:
        degree = entry.get("degree", "").lower()
        for keyword, bonus in degree_bonuses.items():
            if keyword in degree:
                score = max(score, 50 + bonus)
                break

    return min(score, 100)


def _calculate_formatting_score(resume_data: Dict) -> float:
    """Calculate resume formatting score."""
    score = 50.0  # Base score

    sections = resume_data.get("sections", [])

    # Check for essential sections
    essential = ["experience", "education", "skills"]
    for section in essential:
        if section in sections:
            score += 10

    # Check for summary
    if "summary" in sections:
        score += 5

    # Check for projects
    if "projects" in sections:
        score += 5

    # Check text length (too short or too long)
    text_length = resume_data.get("cleaned_text_length", 0)
    if 500 < text_length < 5000:
        score += 10
    elif text_length < 200:
        score -= 10

    # Grammar issues penalty
    grammar_issues = resume_data.get("grammar_issues", [])
    score -= len(grammar_issues) * 5

    return max(min(score, 100), 0)


def _calculate_projects_score(resume_data: Dict) -> float:
    """Calculate projects score."""
    projects = resume_data.get("projects", [])
    if not projects:
        return 20.0

    score = 40.0 + min(len(projects) * 15, 60)
    return min(score, 100)


def _calculate_certifications_score(resume_data: Dict) -> float:
    """Calculate certifications score."""
    certs = resume_data.get("certifications", [])
    if not certs:
        return 20.0

    score = 50.0 + min(len(certs) * 15, 50)
    return min(score, 100)
