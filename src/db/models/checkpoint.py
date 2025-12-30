"""LangGraphCheckpoint model."""

from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.models.base import Base


class LangGraphCheckpoint(Base):
    """LangGraph state checkpoint for conversation persistence."""
    
    __tablename__ = "langgraph_checkpoints"
    
    thread_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_threads.id", ondelete="CASCADE"),
        primary_key=True
    )
    checkpoint_id = Column(String(255), primary_key=True)
    parent_checkpoint_id = Column(String(255))
    state = Column(JSON, nullable=False)
    metadata_ = Column("metadata", JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    thread = relationship("ChatThread", back_populates="checkpoints")
