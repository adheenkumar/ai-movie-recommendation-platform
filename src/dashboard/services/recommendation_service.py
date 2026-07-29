"""
Dashboard recommendation service.
"""

from __future__ import annotations

from pyspark.sql import SparkSession

from src.llm.recommendation_chat import RecommendationChat
from src.recommendation.hybrid import HybridRecommender
from src.recommendation.models import RecommendationResult
from src.utils.paths import GOLD_DATA_DIR
from collections.abc import Callable
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RecommendationService:
    """
    Service layer used by the Streamlit dashboard.
    """

    def __init__(
        self,
        spark: SparkSession,
        progress_callback: Callable[[str], None] | None = None,
    ) -> None:
        self.spark = spark

        def progress(message: str) -> None:
            if progress_callback:
                progress_callback(message)

        logger.info("Initializing Hybrid Recommendation Engine.")

        progress(
            "⚡ Initializing Hybrid Recommendation Engine..."
        )
        self.hybrid = HybridRecommender(spark)

        logger.info("Initializing AI Chat Service.")

        progress("🤖 Initializing AI Chat Service...")
        self.chat = RecommendationChat(spark)

        progress("✅ Recommendation services initialized.")

        logger.info(
            "Recommendation services initialized successfully."
        )

    def recommend_by_movie(
        self,
        movie_title: str,
        top_n: int = 10,
    ) -> list[RecommendationResult]:
        """
        Recommend movies using a seed movie.
        """

        logger.info(
            "Generating movie recommendations for '%s'.",
            movie_title,
        )

        try:
            return self.hybrid.recommend(
                movie_title=movie_title,
                top_n=top_n,
            )

        except Exception:
            logger.exception(
                "Failed to generate movie recommendations."
            )
            raise

    def recommend_by_query(
        self,
        query: str,
        top_n: int = 10,
    ) -> tuple[str, list[RecommendationResult]]:
        """
        Recommend movies using a natural language query.
        """

        logger.info(
            "Generating recommendations for query: '%s'.",
            query,
        )

        try:
            recommendations = self.hybrid.recommend(
                semantic_query=query,
                top_n=top_n,
            )

            explanation = self.chat.explain(
                query=query,
                recommendations=recommendations,
            )

            return explanation, recommendations

        except Exception:
            logger.exception(
                "Failed to generate recommendations for query."
            )
            raise

    def get_movie_metrics(self):
        dataframe = (
            self.spark.read
            .parquet(str(GOLD_DATA_DIR / "movie_metrics.parquet"))
            .toPandas()
        )

        dataframe.rename(
            columns={
                "movieId": "movie_id",
                "releaseYear": "release_year",
                "ratingCount": "rating_count",
                "averageRating": "average_rating",
                "weightedRating": "weighted_rating",
                "popularityScore": "popularity_score",
            },
            inplace=True,
        )

        return dataframe

    def get_genre_metrics(self):
        """
        Load genre metrics from the Gold layer.
        """

        dataframe = (
            self.spark.read
            .parquet(str(GOLD_DATA_DIR / "genre_metrics.parquet"))
            .toPandas()
        )

        dataframe.rename(
            columns={
                "averageRating": "average_rating",
                "movieCount": "movie_count",
                "genreName": "genre",
            },
            inplace=True,
        )

        return dataframe

    def get_user_preferences(self):
        """
        Load user preferences from the Gold layer.
        """

        dataframe = (
            self.spark.read
            .parquet(str(GOLD_DATA_DIR / "user_preferences.parquet"))
            .toPandas()
        )

        dataframe.rename(
            columns={
                "userId": "user_id",
                "favoriteGenre": "favorite_genre",
                "movieCount": "movie_count",
            },
            inplace=True,
        )

        return dataframe