"""
Job Description Pydantic schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class JobDescriptionCreate(BaseModel):
    """Schema for creating a job description."""
    title: str = Field(..., min_length=2, max_length=255)
    company: Optional[str] = None
    raw_text: str = Field(..., min_length=10)


class JobDescriptionResponse(BaseModel):
    """Schema for job description response."""
    id: int
    title: str
    company: Optional[str] = None
    raw_text: str
    parsed_data: Optional[Dict[str, Any]] = None
    required_skills: Optional[List[str]] = None
    required_experience: Optional[str] = None
    required_education: Optional[str] = None
    keywords: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class JobDescriptionListItem(BaseModel):
    """Schema for JD list items."""
    id: int
    title: str
    company: Optional[str] = None
    required_skills_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True
