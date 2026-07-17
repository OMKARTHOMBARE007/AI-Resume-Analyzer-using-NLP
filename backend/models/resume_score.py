"""
ResumeScore model - Stores ATS scores for resume-JD pairs.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database.connection import Base


class ResumeScore(Base):
    __tablename__ = "resume_scores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    jd_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False)

    # Individual category scores (0-100)
    overall_score = Column(Float, default=0.0)
    skills_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    education_score = Column(Float, default=0.0)
    keyword_score = Column(Float, default=0.0)
    formatting_score = Column(Float, default=0.0)
    projects_score = Column(Float, default=0.0)
    certifications_score = Column(Float, default=0.0)

    # Detailed match data
    match_percentage = Column(Float, default=0.0)
    matched_skills = Column(JSON, nullable=True)
    missing_skills = Column(JSON, nullable=True)
    missing_keywords = Column(JSON, nullable=True)
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    semantic_similarity = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    resume = relationship("Resume", back_populates="scores")
    job_description = relationship("JobDescription", back_populates="scores")

    def __repr__(self):
        return f"<ResumeScore(resume_id={self.resume_id}, jd_id={self.jd_id}, overall={self.overall_score})>"
