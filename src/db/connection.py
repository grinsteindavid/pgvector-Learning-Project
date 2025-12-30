import psycopg
from psycopg.rows import dict_row
from src.config import DATABASE_URL
from src.logger import get_logger

logger = get_logger(__name__)


def get_connection():
    """Get a new database connection."""
    logger.debug(f"Connecting to database")
    try:
        conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        logger.debug("Database connection established")
        return conn
    except Exception as e:
        logger.exception(f"Failed to connect to database: {e}")
        raise


def execute_query(query: str, params: tuple = None):
    """Execute a query and return results."""
    logger.debug(f"Executing query: {query[:100]}...")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if cur.description:
                    results = cur.fetchall()
                    logger.debug(f"Query returned {len(results)} rows")
                    return results
                conn.commit()
                logger.debug("Query committed successfully")
                return None
    except Exception as e:
        logger.exception(f"Query execution failed: {e}")
        raise
