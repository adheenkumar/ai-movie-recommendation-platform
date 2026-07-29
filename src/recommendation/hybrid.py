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
from src.recommendation.semantic_recommender import SemanticRecommender

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
        self.semantic = SemanticRecommender()

        logger.info("Hybrid recommender initialized successfully.")

    def recommend(
        self,
        movie_title: str | None = None,
        semantic_query: str | None = None,
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

        content_results = []
        collaborative_results = []

        if movie_title:
            content_results = self.content.recommend(
                movie_title,
                top_n,
            )

            collaborative_results = self.collaborative.recommend(
                movie_title,
                top_n,
            )

        popularity_results = get_top_movies(
            self.spark,
            top_n=top_n,
        )

        semantic_results = []

        if semantic_query:
            semantic_results = self.semantic.recommend(
                query=semantic_query,
                top_k=top_n,
            )

        recommendations = rank_recommendations(
            content=content_results,
            collaborative=collaborative_results,
            popularity=popularity_results,
            semantic=semantic_results,
        )

        recommendations = recommendations[:top_n]

        if movie_title:
            logger.info(
                "Generating hybrid recommendations using movie title '%s'.",
                movie_title,
            )
        elif semantic_query:
            logger.info(
                "Generating hybrid recommendations using semantic query '%s'.",
                semantic_query,
            )
        else:
            logger.info("Generating popularity-based recommendations.")

        return recommendations
