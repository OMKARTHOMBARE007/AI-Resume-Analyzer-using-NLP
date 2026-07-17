"""
Score Pydantic schemas for ATS scoring and matching.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ScoreRequest(BaseModel):
    """Schema for requesting ATS score calculation."""
    resume_id: int
    jd_id: int


class ScoreBreakdown(BaseModel):
    """Schema for individual score breakdown."""
    overall_score: float = 0.0
    skills_score: float = 0.0
    experience_score: float = 0.0
    education_score: float = 0.0
    keyword_score: float = 0.0
    formatting_score: float = 0.0
    projects_score: float = 0.0
    certifications_score: float = 0.0


class MatchResult(BaseModel):
    """Schema for resume vs JD matching results."""
    match_percentage: float = 0.0
    semantic_similarity: float = 0.0
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    missing_keywords: List[str] = []
    strengths: List[str] = []
    weaknesses: List[str] = []


class ATSScoreResponse(BaseModel):
    """Full ATS score response."""
    id: int
    resume_id: int
    jd_id: int
    score_breakdown: ScoreBreakdown
    match_result: MatchResult
    created_at: datetime

    class Config:
        from_attributes = True


class SuggestionItem(BaseModel):
    """Schema for a single suggestion."""
    category: str  # skills, certifications, projects, action_verbs, grammar, formatting, ats_tips
    priority: str  # high, medium, low
    title: str
    description: str
    details: Optional[List[str]] = None


class SuggestionsResponse(BaseModel):
    """Schema for AI suggestions response."""
    resume_id: int
    jd_id: Optional[int] = None
    suggestions: List[SuggestionItem] = []
    total_suggestions: int = 0


class DashboardSummary(BaseModel):
    """Schema for dashboard summary data."""
    total_resumes: int = 0
    total_analyses: int = 0
    average_score: float = 0.0
    best_score: float = 0.0
    recent_scores: List[Dict[str, Any]] = []
    skill_distribution: Dict[str, int] = {}
    top_skills: List[Dict[str, Any]] = []
    keyword_frequency: Dict[str, int] = {}
