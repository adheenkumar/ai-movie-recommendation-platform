"""
Dashboard recommendation service.
"""

from __future__ import annotations
import pandas as pd
from pyspark.sql import SparkSession
from collections.abc import Callable
from src.llm.recommendation_chat import (
    RecommendationChat,
)
from src.recommendation.hybrid import (
    HybridRecommender,
)
from src.recommendation.models import (
    RecommendationResult,
)
from src.recommendation.movie_search import (
    MovieSearch,
)
from src.utils.paths import GOLD_DATA_DIR
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
        self.progress_callback = progress_callback

        # ----------------------------------------------
        # Hybrid Recommendation Engine
        # ----------------------------------------------

        self._update_progress(
            "🧠 Initializing Hybrid Recommendation Engine..."
        )

        logger.info(
            "Initializing Hybrid Recommendation Engine."
        )

        self.hybrid = HybridRecommender(
            spark
        )

        # ----------------------------------------------
        # Smart Movie Search
        # ----------------------------------------------

        self._update_progress(
            "🔎 Initializing Smart Movie Search..."
        )

        logger.info(
            "Initializing Movie Search."
        )

        available_titles = (
            self.hybrid
            .content
            .get_available_titles()
        )

        self.movie_search = MovieSearch(
            available_titles
        )

        logger.info(
            "Movie Search initialized with %d recommendable movies.",
            len(available_titles),
        )

        # ----------------------------------------------
        # AI Chat Service
        # ----------------------------------------------

        self._update_progress(
            "🤖 Initializing AI Assistant..."
        )

        logger.info(
            "Initializing AI Chat Service."
        )

        self.chat = RecommendationChat(
            spark
        )

        # ----------------------------------------------
        # Complete
        # ----------------------------------------------

        self._update_progress(
            "✅ Recommendation Services Ready."
        )

        logger.info(
            "Recommendation services initialized successfully."
        )

    def _update_progress(
            self,
            message: str,
    ) -> None:
        """
        Send initialization status to the dashboard.
        """

        if self.progress_callback is not None:
            self.progress_callback(message)

    # --------------------------------------------------
    # Movie Recommendation
    # --------------------------------------------------

    def recommend_by_movie(
        self,
        movie_title: str,
        top_n: int = 10,
    ) -> tuple[
        list[RecommendationResult] | None,
        list[str],
    ]:
        """
        Recommend movies using a seed movie.

        Returns
        -------
        tuple
            If the title resolves:

                (recommendations, [])

            If suggestions are required:

                (None, suggestions)
        """

        logger.info(
            "Generating movie recommendations "
            "for '%s'.",
            movie_title,
        )

        try:

            resolved_title, suggestions = (
                self.movie_search.resolve_title(
                    movie_title
                )
            )

            # ------------------------------------------
            # Movie not resolved
            # ------------------------------------------

            if resolved_title is None:

                if suggestions:

                    logger.info(
                        "Movie '%s' was not resolved. "
                        "Returning %d suggestions.",
                        movie_title,
                        len(suggestions),
                    )

                else:

                    logger.warning(
                        "No matching movie found for '%s'.",
                        movie_title,
                    )

                return None, suggestions

            # ------------------------------------------
            # Generate Recommendations
            # ------------------------------------------

            logger.info(
                "Resolved '%s' to '%s'.",
                movie_title,
                resolved_title,
            )

            recommendations = (
                self.hybrid.recommend(
                    movie_title=resolved_title,
                    top_n=top_n,
                )
            )

            logger.info(
                "Generated %d recommendations "
                "for '%s'.",
                len(recommendations),
                resolved_title,
            )

            return recommendations, []

        except Exception:

            logger.exception(
                "Failed to generate movie "
                "recommendations for '%s'.",
                movie_title,
            )

            raise

    # --------------------------------------------------
    # Natural Language Recommendation
    # --------------------------------------------------

    def recommend_by_query(
            self,
            query: str,
            top_n: int = 10,
    ) -> tuple[
        str,
        list[RecommendationResult],
    ]:
        """
        Recommend movies using a natural-language
        semantic query.
        """

        logger.info(
            "Generating AI recommendations "
            "for query '%s'.",
            query,
        )

        try:

            recommendations = (
                self.hybrid.recommend(
                    semantic_query=query,
                    top_n=top_n,
                )
            )

            explanation = (
                self.chat.explain(
                    query=query,
                    recommendations=recommendations,
                )
            )

            logger.info(
                "AI recommendation completed "
                "successfully with %d results.",
                len(recommendations),
            )

            return (
                explanation,
                recommendations,
            )

        except Exception:

            logger.exception(
                "Failed to generate AI "
                "recommendations for query '%s'.",
                query,
            )

            raise

    def get_movie_metrics(self) -> pd.DataFrame:
        """
        Load movie metrics from the Gold layer.
        """
        try:
            dataframe = self.spark.read.parquet(
                str(GOLD_DATA_DIR / "movie_metrics.parquet")
            )

            return dataframe.toPandas()

        except Exception:
            logger.exception(
                "Failed to load movie metrics."
            )
            raise

    def get_genre_metrics(self) -> pd.DataFrame:
        """
        Load genre metrics from the Gold layer.
        """
        try:
            dataframe = self.spark.read.parquet(
                str(GOLD_DATA_DIR / "genre_metrics.parquet")
            )

            return dataframe.toPandas()

        except Exception:
            logger.exception(
                "Failed to load genre metrics."
            )
            raise

    def get_user_preferences(self) -> pd.DataFrame:
        """
        Load user preference metrics from the Gold layer.
        """
        try:
            dataframe = self.spark.read.parquet(
                str(GOLD_DATA_DIR / "user_preferences.parquet")
            )

            return dataframe.toPandas()

        except Exception:
            logger.exception(
                "Failed to load user preferences."
            )
            raise
