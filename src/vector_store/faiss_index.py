"""
Utilities for building a FAISS vector index.
"""

from __future__ import annotations

import logging

import faiss
import numpy as np

logger = logging.getLogger(__name__)


def build_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    """
    Build a cosine similarity FAISS index.

    Parameters
    ----------
    embeddings : np.ndarray
        Embedding matrix of shape (N, D).

    Returns
    -------
    faiss.Index
        Searchable FAISS index.
    """

    logger.info("Normalizing embeddings...")

    embeddings = embeddings.astype("float32")

    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    logger.info("Creating FAISS index (dimension=%d)...", dimension)

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    logger.info("Indexed %d vectors.", index.ntotal)

    return index