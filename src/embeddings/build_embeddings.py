"""
Generate sentence embeddings for movies.
"""

from __future__ import annotations

import logging

import numpy as np

from src.embeddings.embedding_model import get_embedding_model
from src.embeddings.embedding_utils import prepare_movie_text
from src.spark_jobs.spark_session import create_spark_session
from src.utils.paths import GOLD_DATA_DIR
from src.vector_store.faiss_index import build_faiss_index
from src.vector_store.persistence import (
    save_index,
    save_metadata,
)
from src.config.constants import (
    COMBINED_TEXT, GENRES, MOVIE_ID, TITLE, RATING_COUNT,
    AVERAGE_RATING, WEIGHTED_RATING, POPULARITY_SCORE, RELEASE_YEAR,
)

logger = logging.getLogger(__name__)


def build_movie_embeddings() -> tuple[np.ndarray, list[dict]]:
    """
    Generate embeddings for all movies.

    Returns
    -------
    tuple
        (embedding_matrix, metadata)
    """

    spark = create_spark_session("Movie Embeddings")

    try:
        logger.info("Reading Gold movie metrics...")

        df = spark.read.parquet(str(GOLD_DATA_DIR / "movie_metrics.parquet"))

        df = prepare_movie_text(df)

        rows = df.collect()

        texts = [row[COMBINED_TEXT] for row in rows]

        if not texts:
            raise ValueError("No movies found to generate embeddings.")

        metadata = [
            {
                MOVIE_ID: row[MOVIE_ID],
                TITLE: row[TITLE],
                GENRES: row[GENRES],
                RATING_COUNT: row[RATING_COUNT],
                AVERAGE_RATING: row[AVERAGE_RATING],
                WEIGHTED_RATING: row[WEIGHTED_RATING],
                POPULARITY_SCORE: row[POPULARITY_SCORE],
                RELEASE_YEAR: row[RELEASE_YEAR],
            }
            for row in rows
        ]

        logger.info("Encoding %d movies...", len(texts))

        model = get_embedding_model()

        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
        ).astype(np.float32)

        logger.info("Building FAISS index...")

        index = build_faiss_index(embeddings)

        logger.info("Persisting vector store...")

        save_index(index)

        save_metadata(metadata)

        logger.info("FAISS index saved successfully.")

        logger.info(
            "Embedding generation completed | movies=%d | dimensions=%d",
            embeddings.shape[0],
            embeddings.shape[1],
        )

    finally:
        spark.stop()

    return embeddings, metadata
