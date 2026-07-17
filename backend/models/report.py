"""
Report model - Stores generated analysis reports.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database.connection import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    jd_id = Column(Integer, nullable=True)  # Optional JD association
    report_data = Column(JSON, nullable=True)  # Full report data as JSON
    pdf_path = Column(String(500), nullable=True)
    report_type = Column(String(50), default="full_analysis")  # full_analysis, quick_scan, comparison
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="reports")
    resume = relationship("Resume", back_populates="reports")

    def __repr__(self):
        return f"<Report(id={self.id}, user_id={self.user_id}, type={self.report_type})>"
