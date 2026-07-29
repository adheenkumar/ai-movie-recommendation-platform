"""
Semantic recommendation service.
"""

from __future__ import annotations

from src.recommendation.models import RecommendationResult, MovieRecommendation
from src.vector_store.search import SemanticSearch
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SemanticRecommender:
    """
    Semantic recommendation using FAISS.
    """

    def __init__(self) -> None:
        self.search = SemanticSearch()

    def recommend(
            self,
            query: str,
            top_k: int = 20,
    ) -> list[RecommendationResult]:

        logger.info(
            "Generating semantic recommendations for '%s'.",
            query,
        )

        search_results = self.search.search(
            query=query,
            top_k=top_k,
        )

        logger.info(
            "Semantic search returned %d candidates.",
            len(search_results),
        )

        recommendations: list[RecommendationResult] = []

        for result in search_results:
            movie = MovieRecommendation(
                movie_id=result.movie_id,
                title=result.title,
                release_year=result.release_year,
                genres=result.genres,
                rating_count=result.rating_count,
                average_rating=result.average_rating,
                weighted_rating=result.weighted_rating,
                popularity_score=result.popularity_score,
            )

            recommendations.append(
                RecommendationResult(
                    recommendation=movie,
                    score=result.similarity_score,
                    source="semantic",
                )
            )

        logger.info(
            "Generated %d semantic recommendations.",
            len(recommendations),
        )

        return recommendations