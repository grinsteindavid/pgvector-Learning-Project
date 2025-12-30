"""Database schema initialization using SQLAlchemy."""

from sqlalchemy import text

from src.db.models.base import Base, engine, init_extensions
from src.db.models import (
    ClinicalOrganization,
    ClinicalTool,
    ChatThread,
    ChatMessage,
    LangGraphCheckpoint,
)
from src.logger import get_logger

logger = get_logger(__name__)


def init_schema():
    """Initialize database schema with pgvector extension."""
    logger.info("Initializing database schema...")
    
    try:
        init_extensions()
        
        logger.info("Creating tables from SQLAlchemy models...")
        Base.metadata.create_all(bind=engine)
        
        logger.info("Creating HNSW indexes for vector search...")
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_org_embedding 
                ON clinical_organizations 
                USING hnsw (embedding vector_cosine_ops)
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_tool_embedding 
                ON clinical_tools 
                USING hnsw (embedding vector_cosine_ops)
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_messages_thread 
                ON chat_messages(thread_id, created_at)
            """))
            conn.commit()
        
        logger.info("Schema initialized successfully.")
    except Exception as e:
        logger.exception(f"Failed to initialize schema: {e}")
        raise


def drop_tables():
    """Drop all tables (use with caution)."""
    logger.warning("Dropping all tables...")
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Tables dropped.")
    except Exception as e:
        logger.exception(f"Failed to drop tables: {e}")
        raise
