"""
Recommendation data models.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MovieRecommendation:
    """
    Represents a recommended movie.
    """

    movie_id: int
    title: str
    release_year: int
    genres: str
    rating_count: int
    average_rating: float
    weighted_rating: float
    popularity_score: float


@dataclass(slots=True)
class RecommendationResult:
    """
    Recommendation together with its algorithm score.
    """

    recommendation: MovieRecommendation
    score: float
    source: str
