"""
Semantic search result model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SearchResult:
    """
    Represents a semantic search result.
    """

    movie_id: int
    title: str
    release_year: int
    genres: str
    rating_count: int
    average_rating: float
    weighted_rating: float
    popularity_score: float
    similarity_score: float
