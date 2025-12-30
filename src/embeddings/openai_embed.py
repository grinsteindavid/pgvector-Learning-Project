from openai import OpenAI
from src.config import OPENAI_API_KEY, EMBEDDING_MODEL
from src.logger import get_logger

logger = get_logger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text: str) -> list[float]:
    """Get embedding vector for a single text."""
    logger.debug(f"Getting embedding for text: '{text[:50]}...'")
    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        logger.debug(f"Embedding received: {len(response.data[0].embedding)} dimensions")
        return response.data[0].embedding
    except Exception as e:
        logger.exception(f"Failed to get embedding: {e}")
        raise


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Get embeddings for multiple texts in one API call."""
    logger.info(f"Getting batch embeddings for {len(texts)} texts")
    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts
        )
        logger.info(f"Batch embeddings received: {len(response.data)} vectors")
        return [item.embedding for item in response.data]
    except Exception as e:
        logger.exception(f"Failed to get batch embeddings: {e}")
        raise
