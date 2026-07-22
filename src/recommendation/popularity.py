"""
Popularity-based recommendation engine.
"""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from src.recommendation.config import (
    DEFAULT_TOP_N,
    MINIMUM_VOTES,
)
from src.recommendation.models import (
    MovieRecommendation,
    RecommendationResult,
)
from src.utils.logger import get_logger
from src.utils.paths import GOLD_DATA_DIR

logger = get_logger(__name__)

RECOMMENDATION_FEATURES_PATH = GOLD_DATA_DIR / "recommendation_features.parquet"


def _load_features(spark: SparkSession) -> DataFrame:
    """
    Load recommendation feature dataset.
    """

    logger.info(
        "Loading recommendation features from %s",
        RECOMMENDATION_FEATURES_PATH,
    )

    return spark.read.parquet(str(RECOMMENDATION_FEATURES_PATH))


def _filter_movies(
    movies: DataFrame,
    minimum_votes: int,
) -> DataFrame:
    """
    Filter movies that do not meet the
    minimum vote threshold.
    """

    logger.info(
        "Filtering movies with ratingCount >= %d",
        minimum_votes,
    )

    return movies.filter(F.col("ratingCount") >= minimum_votes)


def _rank_movies(
    movies: DataFrame,
    top_n: int,
) -> DataFrame:
    """
    Rank movies using weighted rating,
    popularity score and rating count.
    """

    logger.info(
        "Selecting top %d popular movies.",
        top_n,
    )

    return movies.orderBy(
        F.desc("weightedRating"),
        F.desc("popularityScore"),
        F.desc("ratingCount"),
    ).limit(top_n)


def _build_recommendation(
    row,
) -> RecommendationResult:
    """
    Convert Spark row into RecommendationResult.
    """

    movie = MovieRecommendation(
        movie_id=int(row.movieId),
        title=row.title,
        release_year=int(row.releaseYear),
        genres=row.genres,
        rating_count=int(row.ratingCount),
        average_rating=float(row.averageRating),
        weighted_rating=float(row.weightedRating),
        popularity_score=float(row.popularityScore),
    )

    return RecommendationResult(
        recommendation=movie,
        score=float(row.popularityScore),
        source="popularity",
    )


def get_top_movies(
    spark: SparkSession,
    top_n: int = DEFAULT_TOP_N,
    minimum_votes: int = MINIMUM_VOTES,
) -> list[RecommendationResult]:
    """
    Return the highest-ranked movies based on
    popularity and weighted rating.

    Parameters
    ----------
    spark:
        Active Spark session.

    top_n:
        Number of movies to return.

    minimum_votes:
        Minimum number of ratings required.

    Returns
    -------
    list[RecommendationResult]
    """

    logger.info("Starting popularity recommendation.")

    movies = _load_features(spark)

    movies = _filter_movies(
        movies,
        minimum_votes,
    )

    movies = _rank_movies(
        movies,
        top_n,
    )

    recommendations = [_build_recommendation(row) for row in movies.collect()]

    logger.info(
        "Popularity recommendation completed. Returned %d movies.",
        len(recommendations),
    )

    return recommendations
