from src.db.connection import get_connection
from src.embeddings.openai_embed import get_embedding


def search_organizations(query: str, limit: int = 5) -> list[dict]:
    """
    Semantic search for clinical organizations.
    Uses cosine distance (<=>) for similarity.
    """
    query_embedding = get_embedding(query)
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    name,
                    org_type,
                    specialty,
                    description,
                    city,
                    state,
                    ai_use_cases,
                    1 - (embedding <=> %s::vector) AS similarity
                FROM clinical_organizations
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (query_embedding, query_embedding, limit))
            return cur.fetchall()


def search_tools(query: str, limit: int = 5) -> list[dict]:
    """
    Semantic search for clinical tools.
    Uses cosine distance (<=>) for similarity.
    """
    query_embedding = get_embedding(query)
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    name,
                    category,
                    description,
                    target_users,
                    problem_solved,
                    1 - (embedding <=> %s::vector) AS similarity
                FROM clinical_tools
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (query_embedding, query_embedding, limit))
            return cur.fetchall()


def search_all(query: str, limit: int = 3) -> dict:
    """Search both organizations and tools."""
    return {
        "organizations": search_organizations(query, limit),
        "tools": search_tools(query, limit)
    }
