"""
Hybrid recommendation engine.
"""

from __future__ import annotations

from src.recommendation.config import DEFAULT_TOP_N
from src.recommendation.content_based import (
    ContentBasedRecommender,
)
from src.recommendation.collaborative import (
    CollaborativeRecommender,
)
from src.recommendation.models import RecommendationResult
from src.recommendation.popularity import get_top_movies
from src.recommendation.ranking import rank_recommendations
from src.utils.logger import get_logger

logger = get_logger(__name__)


class HybridRecommender:
    """
    Hybrid movie recommendation engine.

    Combines:
    - Content-based recommendations
    - Collaborative filtering recommendations
    - Popularity-based recommendations
    """

    def __init__(self, spark) -> None:
        """
        Initialize recommendation engines.
        """

        logger.info("Initializing hybrid recommender.")

        self.spark = spark

        self.content = ContentBasedRecommender(spark)
        self.collaborative = CollaborativeRecommender(spark)

        logger.info("Hybrid recommender initialized successfully.")

    def recommend(
        self,
        movie_title: str,
        top_n: int = DEFAULT_TOP_N,
    ) -> list[RecommendationResult]:
        """
        Generate hybrid recommendations.

        Parameters
        ----------
        movie_title:
            Movie title used as the recommendation seed.

        top_n:
            Number of recommendations to return.

        Returns
        -------
        list[RecommendationResult]
        """

        logger.info(
            "Generating hybrid recommendations for '%s'.",
            movie_title,
        )

        content_results = self.content.recommend(
            movie_title,
            top_n=top_n,
        )

        collaborative_results = self.collaborative.recommend(
            movie_title,
            top_n=top_n,
        )

        popularity_results = get_top_movies(
            self.spark,
            top_n=top_n,
        )

        recommendations = rank_recommendations(
            content=content_results,
            collaborative=collaborative_results,
            popularity=popularity_results,
        )

        recommendations = recommendations[:top_n]

        logger.info(
            "Generated %d hybrid recommendations.",
            len(recommendations),
        )

        return recommendations
