"""
Tests for Silver-layer PySpark transformations.
"""

import pytest
from pyspark.sql import SparkSession

from src.spark_jobs.silver_transformations import (
    transform_links,
    transform_movies,
    transform_ratings,
    transform_tags,
)
from src.spark_jobs.spark_session import create_spark_session


@pytest.fixture(scope="module")
def spark() -> SparkSession:
    """Create a Spark session for transformation tests."""

    spark_session = create_spark_session("Silver Transformation Tests")

    yield spark_session

    spark_session.stop()


def test_transform_movies(
    spark: SparkSession,
) -> None:
    """Verify movies Silver transformations."""

    dataframe = spark.createDataFrame(
        [
            (1, " Toy Story (1995) ", "Adventure|Animation"),
            (2, "Movie Without Genres (2000)", "(no genres listed)"),
            (2, "Movie Without Genres (2000)", "(no genres listed)"),
        ],
        [
            "movieId",
            "title",
            "genres",
        ],
    )

    result = transform_movies(dataframe)

    rows = {row["movieId"]: row for row in result.collect()}

    assert result.count() == 2
    assert rows[1]["title"] == "Toy Story (1995)"
    assert rows[1]["releaseYear"] == 1995
    assert rows[2]["genres"] is None


def test_transform_ratings(
    spark: SparkSession,
) -> None:
    """Verify ratings Silver transformations."""

    dataframe = spark.createDataFrame(
        [
            (1, 10, 4.5, 964982703),
            (1, 11, 6.0, 964982704),
        ],
        [
            "userId",
            "movieId",
            "rating",
            "timestamp",
        ],
    )

    result = transform_ratings(dataframe)

    rows = result.collect()

    assert len(rows) == 1
    assert rows[0]["rating"] == 4.5
    assert rows[0]["ratingTimestamp"] is not None


def test_transform_tags(
    spark: SparkSession,
) -> None:
    """Verify tags Silver transformations."""

    dataframe = spark.createDataFrame(
        [
            (1, 10, " Sci-Fi ", 964982703),
            (1, 11, "   ", 964982704),
        ],
        [
            "userId",
            "movieId",
            "tag",
            "timestamp",
        ],
    )

    result = transform_tags(dataframe)

    rows = result.collect()

    assert len(rows) == 1
    assert rows[0]["tag"] == "sci-fi"
    assert rows[0]["tagTimestamp"] is not None


def test_transform_links(
    spark: SparkSession,
) -> None:
    """Verify links Silver transformations."""

    dataframe = spark.createDataFrame(
        [
            (1, 114709, 862.0),
            (2, 113497, None),
        ],
        "movieId long, imdbId long, tmdbId double",
    )

    result = transform_links(dataframe)

    rows = {row["movieId"]: row for row in result.collect()}

    assert rows[1]["tmdbId"] == 862
    assert rows[2]["tmdbId"] is None
    assert result.schema["tmdbId"].dataType.typeName() == "long"
