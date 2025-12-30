"""ClinicalOrganization model."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector

from src.db.models.base import Base


class ClinicalOrganization(Base):
    """Healthcare organization with AI use cases."""
    
    __tablename__ = "clinical_organizations"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    org_type = Column(String(50), nullable=False)
    specialty = Column(String(100))
    description = Column(Text, nullable=False)
    city = Column(String(100))
    state = Column(String(50))
    services = Column(JSON, default={})
    ai_use_cases = Column(ARRAY(Text))
    embedding = Column(Vector(1536))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "org_type": self.org_type,
            "specialty": self.specialty,
            "description": self.description,
            "city": self.city,
            "state": self.state,
            "services": self.services,
            "ai_use_cases": self.ai_use_cases or [],
        }
