"""ChatMessage model."""

from datetime import datetime
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.models.base import Base


class ChatMessage(Base):
    """Individual chat message within a thread."""
    
    __tablename__ = "chat_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    thread_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_threads.id", ondelete="CASCADE"),
        nullable=False
    )
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    route = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    thread = relationship("ChatThread", back_populates="messages")
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "thread_id": str(self.thread_id),
            "role": self.role,
            "content": self.content,
            "route": self.route,
            "created_at": self.created_at.isoformat(),
        }
