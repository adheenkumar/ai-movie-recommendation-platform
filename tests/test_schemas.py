"""
Tests for Silver PySpark schema contracts.
"""

from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    TimestampType,
)

from src.spark_jobs.schemas import (
    LINKS_SCHEMA,
    MOVIES_SCHEMA,
    RATINGS_SCHEMA,
    TAGS_SCHEMA,
)


def test_movies_schema() -> None:
    """Verify the movies Silver schema contract."""

    assert MOVIES_SCHEMA["movieId"].dataType == LongType()
    assert MOVIES_SCHEMA["movieId"].nullable is False

    assert MOVIES_SCHEMA["title"].dataType == StringType()
    assert MOVIES_SCHEMA["title"].nullable is False

    assert MOVIES_SCHEMA["genres"].dataType == StringType()
    assert MOVIES_SCHEMA["genres"].nullable is True

    assert (
        MOVIES_SCHEMA["releaseYear"].dataType
        == IntegerType()
    )
    assert MOVIES_SCHEMA["releaseYear"].nullable is True


def test_ratings_schema() -> None:
    """Verify the ratings Silver schema contract."""

    assert RATINGS_SCHEMA["userId"].dataType == LongType()
    assert RATINGS_SCHEMA["movieId"].dataType == LongType()
    assert RATINGS_SCHEMA["rating"].dataType == DoubleType()

    assert (
        RATINGS_SCHEMA["sourceTimestamp"].dataType
        == LongType()
    )

    assert (
        RATINGS_SCHEMA["ratingTimestamp"].dataType
        == TimestampType()
    )


def test_tags_schema() -> None:
    """Verify the tags Silver schema contract."""

    assert TAGS_SCHEMA["userId"].dataType == LongType()
    assert TAGS_SCHEMA["movieId"].dataType == LongType()
    assert TAGS_SCHEMA["tag"].dataType == StringType()

    assert (
        TAGS_SCHEMA["sourceTimestamp"].dataType
        == LongType()
    )

    assert (
        TAGS_SCHEMA["tagTimestamp"].dataType
        == TimestampType()
    )


def test_links_schema() -> None:
    """Verify the links Silver schema contract."""

    assert LINKS_SCHEMA["movieId"].dataType == LongType()
    assert LINKS_SCHEMA["movieId"].nullable is False

    assert LINKS_SCHEMA["imdbId"].dataType == LongType()
    assert LINKS_SCHEMA["imdbId"].nullable is False

    assert LINKS_SCHEMA["tmdbId"].dataType == LongType()
    assert LINKS_SCHEMA["tmdbId"].nullable is True