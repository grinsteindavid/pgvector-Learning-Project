"""Thread and message management using SQLAlchemy ORM."""

from datetime import datetime
from typing import Optional

from src.db.models.base import get_session
from src.db.models.thread import ChatThread
from src.db.models.message import ChatMessage
from src.logger import get_logger

logger = get_logger(__name__)


def create_thread(title: str = "New Chat") -> dict:
    """Create a new chat thread."""
    logger.info(f"Creating new thread: {title}")
    
    with get_session() as session:
        thread = ChatThread(title=title)
        session.add(thread)
        session.flush()
        return thread.to_dict()


def get_thread(thread_id: str) -> Optional[dict]:
    """Get a thread by ID."""
    with get_session() as session:
        thread = session.query(ChatThread).filter_by(id=thread_id).first()
        return thread.to_dict() if thread else None


def list_threads(limit: int = 50) -> list[dict]:
    """List all threads ordered by last update."""
    with get_session() as session:
        threads = (
            session.query(ChatThread)
            .order_by(ChatThread.updated_at.desc())
            .limit(limit)
            .all()
        )
        return [t.to_dict() for t in threads]


def update_thread_title(thread_id: str, title: str) -> Optional[dict]:
    """Update thread title."""
    logger.info(f"Updating thread {thread_id} title to: {title}")
    
    with get_session() as session:
        thread = session.query(ChatThread).filter_by(id=thread_id).first()
        if not thread:
            return None
        thread.title = title
        thread.updated_at = datetime.utcnow()
        session.flush()
        return thread.to_dict()


def delete_thread(thread_id: str) -> bool:
    """Delete a thread and all its messages."""
    logger.info(f"Deleting thread {thread_id}")
    
    with get_session() as session:
        thread = session.query(ChatThread).filter_by(id=thread_id).first()
        if not thread:
            return False
        session.delete(thread)
        return True


def add_message(
    thread_id: str,
    role: str,
    content: str,
    route: Optional[str] = None
) -> dict:
    """Add a message to a thread."""
    logger.debug(f"Adding {role} message to thread {thread_id}")
    
    with get_session() as session:
        message = ChatMessage(
            thread_id=thread_id,
            role=role,
            content=content,
            route=route
        )
        session.add(message)
        
        thread = session.query(ChatThread).filter_by(id=thread_id).first()
        if thread:
            thread.updated_at = datetime.utcnow()
        
        session.flush()
        return message.to_dict()


def get_messages(thread_id: str, limit: int = 100) -> list[dict]:
    """Get messages for a thread."""
    with get_session() as session:
        messages = (
            session.query(ChatMessage)
            .filter_by(thread_id=thread_id)
            .order_by(ChatMessage.created_at.asc())
            .limit(limit)
            .all()
        )
        return [m.to_dict() for m in messages]
