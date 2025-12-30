from src.db.connection import get_connection


def init_schema():
    """Initialize database schema with pgvector extension."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
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
            print("Schema initialized successfully.")


def drop_tables():
    """Drop all tables (use with caution)."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS clinical_organizations CASCADE;")
            cur.execute("DROP TABLE IF EXISTS clinical_tools CASCADE;")
            conn.commit()
            print("Tables dropped.")
