"""
Utility functions for preparing movie text for semantic embeddings.
"""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from src.config.constants import (
    AVERAGE_RATING,COMBINED_TEXT,GENRES,GENRES_TEXT,MOVIE_ID,
    TITLE, RELEASE_YEAR, RATING_COUNT, POPULARITY_SCORE, WEIGHTED_RATING,
)


def prepare_movie_text(df: DataFrame) -> DataFrame:
    """
    Build a semantic text representation for each movie.

    Parameters
    ----------
    df : DataFrame
        Gold movie metrics DataFrame.

    Returns
    -------
    DataFrame:
        DataFrame containing movie metadata and combined text.
    """

    genres = F.regexp_replace(F.col(GENRES), r"\|", ", ")

    return (
        df.withColumn(GENRES_TEXT, genres)
        .withColumn(
            COMBINED_TEXT,
            F.concat_ws(
                ". ",
                F.col(TITLE),
                F.concat(F.lit("Genres: "), F.col(GENRES_TEXT)),
                F.concat(
                    F.lit("Average rating: "),
                    F.round(F.col(AVERAGE_RATING), 1).cast("string"),
                ),
            ),
        )
        .select(
            MOVIE_ID,
            TITLE,
            RELEASE_YEAR,
            GENRES,
            RATING_COUNT,
            AVERAGE_RATING,
            WEIGHTED_RATING,
            POPULARITY_SCORE,
            COMBINED_TEXT,
        )
    )