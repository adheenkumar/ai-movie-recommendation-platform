"""
Semantic recommendation service.
"""

from __future__ import annotations

from src.recommendation.models import (
    RecommendationResult,
    MovieRecommendation,
)
from src.recommendation.query_intent import (
    extract_preferred_genres,
)
from src.vector_store.search import SemanticSearch
from src.utils.logger import get_logger


logger = get_logger(__name__)


class SemanticRecommender:
    """
    Semantic recommendation using FAISS with
    genre-aware reranking.
    """

    def __init__(self) -> None:
        self.search = SemanticSearch()

    def recommend(
        self,
        query: str,
        top_k: int = 20,
    ) -> list[RecommendationResult]:
        """
        Generate semantic recommendations and rerank
        candidates using detected genre preferences.
        """

        logger.info(
            "Generating semantic recommendations for '%s'.",
            query,
        )

        # ----------------------------------------------
        # Detect genre preferences
        # ----------------------------------------------

        preferred_genres = extract_preferred_genres(
            query
        )

        logger.info(
            "Detected preferred genres: %s",
            sorted(preferred_genres),
        )

        # ----------------------------------------------
        # Retrieve a larger candidate pool
        # ----------------------------------------------

        candidate_count = max(
            top_k * 3,
            30,
        )

        search_results = self.search.search(
            query=query,
            top_k=candidate_count,
        )

        logger.info(
            "Semantic search returned %d candidates.",
            len(search_results),
        )

        recommendations: list[RecommendationResult] = []

        # ----------------------------------------------
        # Genre-aware reranking
        # ----------------------------------------------

        for result in search_results:

            movie_genres = {
                genre.strip()
                for genre in result.genres.split("|")
                if genre.strip()
            }

            genre_matches = (
                preferred_genres & movie_genres
            )

            if preferred_genres:

                genre_match_ratio = (
                    len(genre_matches)
                    / len(preferred_genres)
                )

            else:

                genre_match_ratio = 0.0

            # Semantic relevance remains the main signal.
            # Genre matching provides a structured bonus.
            reranked_score = (
                0.75 * result.similarity_score
                + 0.25 * genre_match_ratio
            )

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
                    score=reranked_score,
                    source="semantic",
                )
            )

        # ----------------------------------------------
        # Sort by reranked score
        # ----------------------------------------------

        recommendations.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        # ----------------------------------------------
        # Return requested number
        # ----------------------------------------------

        recommendations = recommendations[
            :top_k
        ]

        logger.info(
            "Generated %d genre-aware semantic recommendations.",
            len(recommendations),
        )

        return recommendations
