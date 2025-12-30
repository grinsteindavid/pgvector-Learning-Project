import psycopg
from psycopg.rows import dict_row
from src.config import DATABASE_URL


def get_connection():
    """Get a new database connection."""
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def execute_query(query: str, params: tuple = None):
    """Execute a query and return results."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:
                return cur.fetchall()
            conn.commit()
            return None
