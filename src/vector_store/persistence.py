"""
Save and load FAISS indices.
"""

from __future__ import annotations

import logging
import pickle

import faiss

from src.utils.paths import FAISS_MODEL_DIR

logger = logging.getLogger(__name__)

INDEX_PATH = FAISS_MODEL_DIR / "movie_index.faiss"
METADATA_PATH = FAISS_MODEL_DIR / "metadata.pkl"


def save_index(index: faiss.Index) -> None:
    """
    Save FAISS index to disk.
    """

    logger.info("Saving FAISS index...")

    faiss.write_index(index, str(INDEX_PATH))


def load_index() -> faiss.Index:
    """
    Load FAISS index.
    """

    logger.info("Loading FAISS index...")

    return faiss.read_index(str(INDEX_PATH))


def save_metadata(metadata: list[dict]) -> None:
    """
    Save movie metadata.
    """

    logger.info("Saving metadata...")

    with open(METADATA_PATH, "wb") as file:
        pickle.dump(metadata, file)


def load_metadata() -> list[dict]:
    """
    Load movie metadata.
    """


    with open(METADATA_PATH, "rb") as file:
        return pickle.load(file)