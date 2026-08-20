"""
Tests for natural-language query intent extraction.
"""

from src.recommendation.query_intent import (
    extract_preferred_genres,
)


def test_animation_query():

    genres = extract_preferred_genres(
        "Funny animated movies with toys"
    )

    assert "Animation" in genres
    assert "Comedy" in genres


def test_romantic_comedy_query():

    genres = extract_preferred_genres(
        "Romantic comedy movies"
    )

    assert genres == {
        "Romance",
        "Comedy",
    }


def test_science_fiction_query():

    genres = extract_preferred_genres(
        "Space adventure science fiction movies"
    )

    assert genres == {
        "Adventure",
        "Sci-Fi",
    }


def test_crime_thriller_query():

    genres = extract_preferred_genres(
        "Dark crime thriller"
    )

    assert genres == {
        "Crime",
        "Thriller",
    }


def test_query_without_genre():

    genres = extract_preferred_genres(
        "movies about robots taking over the world"
    )

    assert genres == set()
