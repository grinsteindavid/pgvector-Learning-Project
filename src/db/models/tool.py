"""ClinicalTool model."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector

from src.db.models.base import Base


class ClinicalTool(Base):
    """Clinical decision support tool."""
    
    __tablename__ = "clinical_tools"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    target_users = Column(ARRAY(Text))
    problem_solved = Column(Text)
    embedding = Column(Vector(1536))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "target_users": self.target_users or [],
            "problem_solved": self.problem_solved,
        }
