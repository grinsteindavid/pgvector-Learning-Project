import logging
import os
import sys
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent / "logs"
_app_logger_initialized = False


def setup_app_logger(
    name: str = "clinical_ai",
    level: int = logging.INFO
) -> logging.Logger:
    """
    Configure logger with BOTH file (timestamped) and console output.
    Creates a new log file each time the app runs.
    Use this for the main LangGraph application entry point.
    """
    global _app_logger_initialized
    
    LOGS_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"agent_run_{timestamp}.log"
    
    root_logger = logging.getLogger()
    
    if _app_logger_initialized:
        return logging.getLogger(name)
    
    root_logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    _app_logger_initialized = True
    
    logger = logging.getLogger(name)
    logger.info(f"Log file created: {log_file}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a module.
    If app logger is initialized, logs go to both file and console.
    Otherwise, logs go to console only.
    """
    return logging.getLogger(name)
