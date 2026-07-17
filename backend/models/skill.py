"""
Skill model - Stores skills extracted from resumes.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.connection import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False, index=True)
    category = Column(String(100), nullable=True)  # e.g., Programming, Framework, Database
    proficiency_level = Column(String(50), nullable=True)  # Beginner, Intermediate, Expert
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    resume = relationship("Resume", back_populates="skills")

    def __repr__(self):
        return f"<Skill(name={self.name}, category={self.category})>"
