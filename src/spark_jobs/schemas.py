"""
Silver-layer PySpark schema contracts.

This module defines the expected output schemas for
standardized MovieLens Silver datasets.
"""

from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)


MOVIES_SCHEMA = StructType(
    [
        StructField(
            "movieId",
            LongType(),
            nullable=False,
        ),
        StructField(
            "title",
            StringType(),
            nullable=False,
        ),
        StructField(
            "genres",
            StringType(),
            nullable=True,
        ),
        StructField(
            "releaseYear",
            IntegerType(),
            nullable=True,
        ),
    ]
)


RATINGS_SCHEMA = StructType(
    [
        StructField(
            "userId",
            LongType(),
            nullable=False,
        ),
        StructField(
            "movieId",
            LongType(),
            nullable=False,
        ),
        StructField(
            "rating",
            DoubleType(),
            nullable=False,
        ),
        StructField(
            "sourceTimestamp",
            LongType(),
            nullable=False,
        ),
        StructField(
            "ratingTimestamp",
            TimestampType(),
            nullable=False,
        ),
    ]
)


TAGS_SCHEMA = StructType(
    [
        StructField(
            "userId",
            LongType(),
            nullable=False,
        ),
        StructField(
            "movieId",
            LongType(),
            nullable=False,
        ),
        StructField(
            "tag",
            StringType(),
            nullable=False,
        ),
        StructField(
            "sourceTimestamp",
            LongType(),
            nullable=False,
        ),
        StructField(
            "tagTimestamp",
            TimestampType(),
            nullable=False,
        ),
    ]
)


LINKS_SCHEMA = StructType(
    [
        StructField(
            "movieId",
            LongType(),
            nullable=False,
        ),
        StructField(
            "imdbId",
            LongType(),
            nullable=False,
        ),
        StructField(
            "tmdbId",
            LongType(),
            nullable=True,
        ),
    ]
)