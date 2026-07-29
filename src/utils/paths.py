"""
Centralized project paths.

This module defines commonly used project directories.
"""

from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data directories
DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
BRONZE_DATA_DIR = DATA_DIR / "bronze"
SILVER_DATA_DIR = DATA_DIR / "silver"
GOLD_DATA_DIR = DATA_DIR / "gold"

# Other project directories
LOGS_DIR = PROJECT_ROOT / "logs"
MODELS_DIR = PROJECT_ROOT / "models"
DOCS_DIR = PROJECT_ROOT / "docs"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Create directories if they don't exist
for directory in [
    RAW_DATA_DIR,
    BRONZE_DATA_DIR,
    SILVER_DATA_DIR,
    GOLD_DATA_DIR,
    LOGS_DIR,
    MODELS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

MODEL_DIR = PROJECT_ROOT / "models"

SENTENCE_MODEL_DIR = MODEL_DIR / "sentence_transformer"

FAISS_MODEL_DIR = MODEL_DIR / "faiss"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
SENTENCE_MODEL_DIR.mkdir(parents=True, exist_ok=True)
FAISS_MODEL_DIR.mkdir(parents=True, exist_ok=True)
