"""Thread and message management for chat persistence."""

from typing import Optional
from uuid import UUID

from src.db.connection import get_connection
from src.logger import get_logger

logger = get_logger(__name__)


def create_thread(title: str = "New Chat") -> dict:
    """Create a new chat thread."""
    logger.info(f"Creating new thread: {title}")
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chat_threads (title)
                VALUES (%s)
                RETURNING id, title, created_at, updated_at
            """, (title,))
            row = cur.fetchone()
            conn.commit()
            
            return {
                "id": str(row["id"]),
                "title": row["title"],
                "created_at": row["created_at"].isoformat(),
                "updated_at": row["updated_at"].isoformat()
            }


def get_thread(thread_id: str) -> Optional[dict]:
    """Get a thread by ID."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, created_at, updated_at
                FROM chat_threads
                WHERE id = %s
            """, (thread_id,))
            row = cur.fetchone()
            
            if not row:
                return None
            
            return {
                "id": str(row["id"]),
                "title": row["title"],
                "created_at": row["created_at"].isoformat(),
                "updated_at": row["updated_at"].isoformat()
            }


def list_threads(limit: int = 50) -> list[dict]:
    """List all threads ordered by last update."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, created_at, updated_at
                FROM chat_threads
                ORDER BY updated_at DESC
                LIMIT %s
            """, (limit,))
            
            return [
                {
                    "id": str(row["id"]),
                    "title": row["title"],
                    "created_at": row["created_at"].isoformat(),
                    "updated_at": row["updated_at"].isoformat()
                }
                for row in cur.fetchall()
            ]


def update_thread_title(thread_id: str, title: str) -> Optional[dict]:
    """Update thread title."""
    logger.info(f"Updating thread {thread_id} title to: {title}")
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE chat_threads
                SET title = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING id, title, created_at, updated_at
            """, (title, thread_id))
            row = cur.fetchone()
            conn.commit()
            
            if not row:
                return None
            
            return {
                "id": str(row["id"]),
                "title": row["title"],
                "created_at": row["created_at"].isoformat(),
                "updated_at": row["updated_at"].isoformat()
            }


def delete_thread(thread_id: str) -> bool:
    """Delete a thread and all its messages."""
    logger.info(f"Deleting thread {thread_id}")
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM chat_threads
                WHERE id = %s
            """, (thread_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted


def add_message(
    thread_id: str,
    role: str,
    content: str,
    route: Optional[str] = None
) -> dict:
    """Add a message to a thread."""
    logger.debug(f"Adding {role} message to thread {thread_id}")
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chat_messages (thread_id, role, content, route)
                VALUES (%s, %s, %s, %s)
                RETURNING id, thread_id, role, content, route, created_at
            """, (thread_id, role, content, route))
            row = cur.fetchone()
            
            cur.execute("""
                UPDATE chat_threads SET updated_at = NOW() WHERE id = %s
            """, (thread_id,))
            
            conn.commit()
            
            return {
                "id": str(row["id"]),
                "thread_id": str(row["thread_id"]),
                "role": row["role"],
                "content": row["content"],
                "route": row["route"],
                "created_at": row["created_at"].isoformat()
            }


def get_messages(thread_id: str, limit: int = 100) -> list[dict]:
    """Get messages for a thread."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, thread_id, role, content, route, created_at
                FROM chat_messages
                WHERE thread_id = %s
                ORDER BY created_at ASC
                LIMIT %s
            """, (thread_id, limit))
            
            return [
                {
                    "id": str(row["id"]),
                    "thread_id": str(row["thread_id"]),
                    "role": row["role"],
                    "content": row["content"],
                    "route": row["route"],
                    "created_at": row["created_at"].isoformat()
                }
                for row in cur.fetchall()
            ]
