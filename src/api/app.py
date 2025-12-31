import os

from flask import Flask
from flask_cors import CORS

from src.logger import get_logger

logger = get_logger(__name__)


def init_database():
    """Initialize database schema if needed."""
    try:
        from src.db.schema import init_schema
        init_schema()
        logger.info("Database schema initialized")
    except Exception as e:
        logger.warning(f"Schema init skipped or failed: {e}")


def create_app():
    """Flask application factory."""
    app = Flask(__name__)
    
    CORS(app)
    
    if os.getenv("AUTO_INIT_DB", "true").lower() == "true":
        init_database()
    
    from src.api.routes.health import health_bp
    from src.api.routes.agent import agent_bp
    from src.api.routes.threads import threads_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(agent_bp, url_prefix='/api')
    app.register_blueprint(threads_bp, url_prefix='/api')
    
    logger.info("Flask app created with routes: /health, /api/query, /api/threads")
    
    return app
