"""
Centralized logging configuration.

This module provides a reusable logger for the entire application.
"""

from pathlib import Path
import logging

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Logs directory
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "application.log"


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured Logger instance.
    """

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File output
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger