"""
Query intent utilities for semantic movie recommendations.
"""

from __future__ import annotations


GENRE_ALIASES = {
    "action": "Action",
    "adventure": "Adventure",
    "animation": "Animation",
    "animated": "Animation",
    "children": "Children",
    "kids": "Children",
    "family": "Children",
    "comedy": "Comedy",
    "funny": "Comedy",
    "crime": "Crime",
    "documentary": "Documentary",
    "drama": "Drama",
    "fantasy": "Fantasy",
    "film noir": "Film-Noir",
    "noir": "Film-Noir",
    "horror": "Horror",
    "imax": "IMAX",
    "musical": "Musical",
    "mystery": "Mystery",
    "romance": "Romance",
    "romantic": "Romance",
    "sci-fi": "Sci-Fi",
    "science fiction": "Sci-Fi",
    "scifi": "Sci-Fi",
    "thriller": "Thriller",
    "war": "War",
    "western": "Western",
}


def extract_preferred_genres(
    query: str,
) -> set[str]:
    """
    Extract MovieLens genre preferences from a
    natural-language query.
    """

    normalized_query = query.lower().strip()

    preferred_genres: set[str] = set()

    for phrase, genre in GENRE_ALIASES.items():

        if phrase in normalized_query:
            preferred_genres.add(genre)

    return preferred_genres
