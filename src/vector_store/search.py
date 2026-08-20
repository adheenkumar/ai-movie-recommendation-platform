"""
Semantic movie search using FAISS.
"""

from __future__ import annotations

import logging

import faiss
import numpy as np

from src.config.constants import (
    GENRES,MOVIE_ID,TITLE, RELEASE_YEAR, RATING_COUNT,
    AVERAGE_RATING, POPULARITY_SCORE, WEIGHTED_RATING,
)
from src.embeddings.embedding_model import get_embedding_model
from src.vector_store.persistence import (
    load_index,
    load_metadata,
)
from src.vector_store.search_result import SearchResult

logger = logging.getLogger(__name__)


class SemanticSearch:
    """
    FAISS semantic search service.
    """

    def __init__(self) -> None:
        logger.info("Loading FAISS index...")

        self.index: faiss.Index = load_index()
        self.metadata = load_metadata()

        self.model = get_embedding_model()

        logger.info(
            "Semantic search initialized | vectors=%d",
            self.index.ntotal,
        )

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[SearchResult]:
        """
        Perform semantic movie search.
        """

        logger.info("Searching for: %s", query)

        if not query.strip():
            raise ValueError("Query must not be empty.")

        if top_k < 1:
            raise ValueError("top_k must be greater than zero.")

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
        ).astype(np.float32)

        faiss.normalize_L2(embedding)

        scores, indices = self.index.search(
            embedding,
            top_k,
        )

        results: list[SearchResult] = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            movie = self.metadata[idx]

            results.append(
                SearchResult(
                    movie_id=movie[MOVIE_ID],
                    title=movie[TITLE],
                    release_year=movie[RELEASE_YEAR],
                    genres=movie[GENRES],
                    rating_count=movie[RATING_COUNT],
                    average_rating=movie[AVERAGE_RATING],
                    weighted_rating=movie[WEIGHTED_RATING],
                    popularity_score=movie[POPULARITY_SCORE],
                    similarity_score=float(score),
                )
            )

        return results
