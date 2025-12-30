from src.db.connection import get_connection
from src.logger import get_logger

logger = get_logger(__name__)


def init_schema():
    """Initialize database schema with pgvector extension."""
    logger.info("Initializing database schema...")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                logger.info("Creating pgvector extension...")
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                
                logger.info("Creating clinical_organizations table...")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS clinical_organizations (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        org_type VARCHAR(50) NOT NULL,
                        specialty VARCHAR(100),
                        description TEXT NOT NULL,
                        city VARCHAR(100),
                        state VARCHAR(50),
                        services JSONB DEFAULT '{}',
                        ai_use_cases TEXT[],
                        embedding vector(1536),
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    );
                """)
                
                logger.info("Creating clinical_tools table...")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS clinical_tools (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        category VARCHAR(100) NOT NULL,
                        description TEXT NOT NULL,
                        target_users TEXT[],
                        problem_solved TEXT,
                        embedding vector(1536),
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    );
                """)
                
                logger.info("Creating HNSW indexes...")
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_org_embedding 
                    ON clinical_organizations 
                    USING hnsw (embedding vector_cosine_ops);
                """)
                
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_tool_embedding 
                    ON clinical_tools 
                    USING hnsw (embedding vector_cosine_ops);
                """)
                
                conn.commit()
                logger.info("Schema initialized successfully.")
    except Exception as e:
        logger.exception(f"Failed to initialize schema: {e}")
        raise


def drop_tables():
    """Drop all tables (use with caution)."""
    logger.warning("Dropping all tables...")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS clinical_organizations CASCADE;")
                cur.execute("DROP TABLE IF EXISTS clinical_tools CASCADE;")
                conn.commit()
                logger.info("Tables dropped.")
    except Exception as e:
        logger.exception(f"Failed to drop tables: {e}")
        raise
