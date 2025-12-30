"""SQLAlchemy base configuration and engine setup."""

from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

from src.config import DATABASE_URL
from src.logger import get_logger

logger = get_logger(__name__)

db_url = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")

engine = create_engine(
    db_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
ScopedSession = scoped_session(SessionLocal)

Base = declarative_base()


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_extensions():
    """Initialize PostgreSQL extensions."""
    logger.info("Initializing pgvector extension...")
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    logger.info("pgvector extension ready")
