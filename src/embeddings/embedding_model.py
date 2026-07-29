"""
Sentence Transformer model wrapper.

Provides a singleton interface for loading and using the
Sentence Transformer embedding model.
"""

from __future__ import annotations

import logging
from functools import lru_cache

from sentence_transformers import SentenceTransformer

from src.utils.paths import SENTENCE_MODEL_DIR

logger = logging.getLogger(__name__)

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load and cache the Sentence Transformer model.

    Returns
    -------
    SentenceTransformer
        Cached model instance.
    """
    logger.info("Loading Sentence Transformer model: %s", MODEL_NAME)

    model = SentenceTransformer(
        MODEL_NAME,
        cache_folder=str(SENTENCE_MODEL_DIR),
    )

    logger.info("Sentence Transformer loaded successfully.")

    return model