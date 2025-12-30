from sqlalchemy import text

from src.retrievers.base import BaseRetriever, EmbeddingFunction
from src.db.models.base import engine
from src.logger import get_logger

logger = get_logger(__name__)


class OrgsRetriever(BaseRetriever):
    """Retriever for clinical_organizations table."""
    
    def __init__(self, embed_fn: EmbeddingFunction):
        super().__init__(embed_fn)
    
    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Search clinical organizations by semantic similarity."""
        logger.info(f"Searching clinical_organizations: query='{query[:50]}...', limit={limit}")
        query_embedding = self.embed_fn(query)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    id,
                    name,
                    org_type,
                    specialty,
                    description,
                    city,
                    state,
                    ai_use_cases,
                    1 - (embedding <=> CAST(:vec AS vector)) AS similarity
                FROM clinical_organizations
                ORDER BY embedding <=> CAST(:vec AS vector)
                LIMIT :limit
            """), {"vec": query_embedding, "limit": limit})
            
            results = [dict(row._mapping) for row in result]
            logger.info(f"Found {len(results)} clinical organizations")
            return results
