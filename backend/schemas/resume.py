"""
Resume Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ResumeUploadResponse(BaseModel):
    """Schema for resume upload response."""
    id: int
    filename: str
    file_type: str
    file_size: Optional[int] = None
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    uploaded_at: datetime
    message: str = "Resume uploaded and parsed successfully"

    class Config:
        from_attributes = True


class ParsedResumeData(BaseModel):
    """Schema for parsed resume data."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    skills: List[str] = []
    education: List[Dict[str, Any]] = []
    experience: List[Dict[str, Any]] = []
    certifications: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    languages: List[str] = []
    achievements: List[str] = []
    summary: Optional[str] = None


class ResumeResponse(BaseModel):
    """Full resume response with parsed data."""
    id: int
    filename: str
    file_type: str
    file_size: Optional[int] = None
    raw_text: Optional[str] = None
    parsed_data: Optional[Dict[str, Any]] = None
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    candidate_address: Optional[str] = None
    total_experience_years: Optional[int] = None
    highest_education: Optional[str] = None
    uploaded_at: datetime
    skills: List[Dict[str, Any]] = []
    certifications: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True


class ResumeListItem(BaseModel):
    """Schema for resume list items (summary view)."""
    id: int
    filename: str
    file_type: str
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    total_experience_years: Optional[int] = None
    skill_count: int = 0
    uploaded_at: datetime

    class Config:
        from_attributes = True
