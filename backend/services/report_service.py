"""
Report Service - Generates PDF analysis reports.
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.models.report import Report
from backend.models.resume import Resume
from backend.models.resume_score import ResumeScore
from backend.config import settings


def generate_report(
    db: Session,
    user_id: int,
    resume_id: int,
    jd_id: Optional[int] = None,
    report_type: str = "full_analysis",
) -> Report:
    """Generate a PDF analysis report."""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    # Gather report data
    report_data = {
        "candidate_name": resume.candidate_name or "Unknown",
        "candidate_email": resume.candidate_email or "",
        "filename": resume.filename,
        "generated_at": datetime.utcnow().isoformat(),
        "report_type": report_type,
    }

    # Add parsed data
    parsed_data = resume.parsed_data or {}
    report_data["skills"] = parsed_data.get("skill_names", [])
    report_data["skill_distribution"] = parsed_data.get("skill_distribution", {})
    report_data["education"] = parsed_data.get("education", [])
    report_data["experience"] = parsed_data.get("experience", [])
    report_data["certifications"] = parsed_data.get("certifications", [])
    report_data["action_verbs"] = parsed_data.get("action_verbs", {})

    # Add score data if available
    if jd_id:
        score = db.query(ResumeScore).filter(
            ResumeScore.resume_id == resume_id,
            ResumeScore.jd_id == jd_id,
        ).first()
        if score:
            report_data["scores"] = {
                "overall": score.overall_score,
                "skills": score.skills_score,
                "experience": score.experience_score,
                "education": score.education_score,
                "keywords": score.keyword_score,
                "formatting": score.formatting_score,
                "projects": score.projects_score,
                "certifications": score.certifications_score,
            }
            report_data["match_percentage"] = score.match_percentage
            report_data["matched_skills"] = score.matched_skills or []
            report_data["missing_skills"] = score.missing_skills or []
            report_data["strengths"] = score.strengths or []
            report_data["weaknesses"] = score.weaknesses or []

    # Generate PDF
    pdf_path = _generate_pdf_report(report_data, user_id, resume_id)

    # Save report record
    report = Report(
        user_id=user_id,
        resume_id=resume_id,
        jd_id=jd_id,
        report_data=report_data,
        pdf_path=pdf_path,
        report_type=report_type,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def _generate_pdf_report(report_data: Dict, user_id: int, resume_id: int) -> str:
    """Generate a PDF report file using fpdf2."""
    try:
        from fpdf import FPDF
    except ImportError:
        # If fpdf2 not installed, save as JSON
        import json
        report_dir = settings.REPORT_DIR / str(user_id)
        report_dir.mkdir(parents=True, exist_ok=True)
        filename = f"report_{resume_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = report_dir / filename
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        return str(filepath)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 15, "AI Resume Analysis Report", ln=True, align="C")
    pdf.ln(5)

    # Candidate Info
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Candidate Information", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Name: {report_data.get('candidate_name', 'N/A')}", ln=True)
    pdf.cell(0, 7, f"Email: {report_data.get('candidate_email', 'N/A')}", ln=True)
    pdf.cell(0, 7, f"File: {report_data.get('filename', 'N/A')}", ln=True)
    pdf.cell(0, 7, f"Generated: {report_data.get('generated_at', '')}", ln=True)
    pdf.ln(5)

    # Scores
    scores = report_data.get("scores")
    if scores:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "ATS Score Breakdown", ln=True)
        pdf.set_font("Helvetica", "", 11)

        score_items = [
            ("Overall Score", scores.get("overall", 0)),
            ("Skills Match", scores.get("skills", 0)),
            ("Experience Match", scores.get("experience", 0)),
            ("Education Match", scores.get("education", 0)),
            ("Keyword Match", scores.get("keywords", 0)),
            ("Formatting", scores.get("formatting", 0)),
            ("Projects", scores.get("projects", 0)),
            ("Certifications", scores.get("certifications", 0)),
        ]

        for label, value in score_items:
            pdf.cell(80, 7, f"  {label}:", ln=False)
            pdf.cell(0, 7, f"{value:.1f}/100", ln=True)

        pdf.ln(3)
        pdf.cell(0, 7, f"Match Percentage: {report_data.get('match_percentage', 0):.1f}%", ln=True)
        pdf.ln(5)

    # Skills
    skills = report_data.get("skills", [])
    if skills:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, f"Skills ({len(skills)})", ln=True)
        pdf.set_font("Helvetica", "", 10)
        skills_text = ", ".join(skills[:30])
        pdf.multi_cell(0, 6, skills_text)
        pdf.ln(5)

    # Matched Skills
    matched = report_data.get("matched_skills", [])
    if matched:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, f"Matched Skills ({len(matched)})", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(0, 128, 0)
        pdf.multi_cell(0, 6, ", ".join(matched))
        pdf.set_text_color(0, 0, 0)
        pdf.ln(3)

    # Missing Skills
    missing = report_data.get("missing_skills", [])
    if missing:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, f"Missing Skills ({len(missing)})", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(200, 0, 0)
        pdf.multi_cell(0, 6, ", ".join(missing))
        pdf.set_text_color(0, 0, 0)
        pdf.ln(3)

    # Strengths
    strengths = report_data.get("strengths", [])
    if strengths:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Strengths", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for s in strengths:
            pdf.cell(0, 6, f"  + {s}", ln=True)
        pdf.ln(3)

    # Weaknesses
    weaknesses = report_data.get("weaknesses", [])
    if weaknesses:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Areas for Improvement", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for w in weaknesses:
            pdf.cell(0, 6, f"  - {w}", ln=True)
        pdf.ln(3)

    # Save PDF
    report_dir = settings.REPORT_DIR / str(user_id)
    report_dir.mkdir(parents=True, exist_ok=True)
    filename = f"report_{resume_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = str(report_dir / filename)
    pdf.output(filepath)

    return filepath
