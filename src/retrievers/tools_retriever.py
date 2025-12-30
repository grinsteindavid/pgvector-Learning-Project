from sqlalchemy import text

from src.retrievers.base import BaseRetriever, EmbeddingFunction
from src.db.models.base import engine
from src.logger import get_logger

logger = get_logger(__name__)


class ToolsRetriever(BaseRetriever):
    """Retriever for clinical_tools table."""
    
    def __init__(self, embed_fn: EmbeddingFunction):
        super().__init__(embed_fn)
    
    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Search clinical tools by semantic similarity."""
        logger.info(f"Searching clinical_tools: query='{query[:50]}...', limit={limit}")
        query_embedding = self.embed_fn(query)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    id,
                    name,
                    category,
                    description,
                    target_users,
                    problem_solved,
                    1 - (embedding <=> CAST(:vec AS vector)) AS similarity
                FROM clinical_tools
                ORDER BY embedding <=> CAST(:vec AS vector)
                LIMIT :limit
            """), {"vec": query_embedding, "limit": limit})
            
            results = [dict(row._mapping) for row in result]
            logger.info(f"Found {len(results)} clinical tools")
            return results
