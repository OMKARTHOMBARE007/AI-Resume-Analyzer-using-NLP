"""
JobDescription model - Stores job descriptions and their parsed requirements.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database.connection import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    raw_text = Column(Text, nullable=False)
    parsed_data = Column(JSON, nullable=True)  # Structured JD data as JSON
    # Extracted fields
    required_skills = Column(JSON, nullable=True)  # List of required skills
    required_experience = Column(String(100), nullable=True)
    required_education = Column(String(255), nullable=True)
    keywords = Column(JSON, nullable=True)  # Important keywords
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    scores = relationship("ResumeScore", back_populates="job_description", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<JobDescription(id={self.id}, title={self.title})>"
