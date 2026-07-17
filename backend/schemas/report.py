"""
Report Pydantic schemas.
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ReportRequest(BaseModel):
    """Schema for requesting report generation."""
    resume_id: int
    jd_id: Optional[int] = None
    report_type: str = "full_analysis"  # full_analysis, quick_scan, comparison


class ReportResponse(BaseModel):
    """Schema for report response."""
    id: int
    resume_id: int
    jd_id: Optional[int] = None
    report_type: str
    report_data: Optional[Dict[str, Any]] = None
    pdf_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
