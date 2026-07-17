"""
Schemas package - imports all Pydantic schemas.
"""

from backend.schemas.user import (
    UserRegister, UserLogin, UserResponse, UserUpdate,
    TokenResponse, ForgotPasswordRequest, ResetPasswordRequest,
    ChangePasswordRequest,
)
from backend.schemas.resume import (
    ResumeUploadResponse, ParsedResumeData, ResumeResponse, ResumeListItem,
)
from backend.schemas.job_description import (
    JobDescriptionCreate, JobDescriptionResponse, JobDescriptionListItem,
)
from backend.schemas.score import (
    ScoreRequest, ScoreBreakdown, MatchResult, ATSScoreResponse,
    SuggestionItem, SuggestionsResponse, DashboardSummary,
)
from backend.schemas.report import (
    ReportRequest, ReportResponse,
)

__all__ = [
    "UserRegister", "UserLogin", "UserResponse", "UserUpdate",
    "TokenResponse", "ForgotPasswordRequest", "ResetPasswordRequest",
    "ChangePasswordRequest",
    "ResumeUploadResponse", "ParsedResumeData", "ResumeResponse", "ResumeListItem",
    "JobDescriptionCreate", "JobDescriptionResponse", "JobDescriptionListItem",
    "ScoreRequest", "ScoreBreakdown", "MatchResult", "ATSScoreResponse",
    "SuggestionItem", "SuggestionsResponse", "DashboardSummary",
    "ReportRequest", "ReportResponse",
]
