"""
Report Router - Generate and download PDF reports.
"""

import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.services.auth_service import get_current_user
from backend.services.report_service import generate_report
from backend.schemas.report import ReportRequest
from backend.models.user import User
from backend.models.report import Report

router = APIRouter(prefix="/api/report", tags=["Reports"])


@router.post("/generate")
def create_report(
    data: ReportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate a PDF analysis report."""
    report = generate_report(
        db, current_user.id, data.resume_id, data.jd_id, data.report_type
    )
    return {
        "id": report.id,
        "resume_id": report.resume_id,
        "jd_id": report.jd_id,
        "report_type": report.report_type,
        "pdf_path": report.pdf_path,
        "created_at": report.created_at.isoformat(),
        "message": "Report generated successfully",
    }


@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Download a generated report."""
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id,
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    if not report.pdf_path or not os.path.exists(report.pdf_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found on disk.",
        )

    filename = os.path.basename(report.pdf_path)
    media_type = "application/pdf" if filename.endswith(".pdf") else "application/json"

    return FileResponse(
        path=report.pdf_path,
        filename=filename,
        media_type=media_type,
    )
