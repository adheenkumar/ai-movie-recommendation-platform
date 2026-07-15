"""
Silver-layer transformation functions.

This module contains dataset-specific PySpark transformations
for converting Bronze MovieLens data into standardized,
validated Silver datasets.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def transform_movies(
    dataframe: DataFrame,
) -> DataFrame:
    """
    Transform the Bronze movie's dataset.

    Args:
        dataframe: Bronze movies DataFrame.

    Returns:
        Standardized Silver movies DataFrame.
    """

    transformed = (
        dataframe
        .select(
            F.col("movieId").cast("long").alias("movieId"),
            F.trim(F.col("title")).alias("title"),
            F.trim(F.col("genres")).alias("genres"),
        )
        .withColumn(
            "releaseYear",
            F.regexp_extract(
                F.col("title"),
                r"\((\d{4})\)$",
                1,
            ).cast("int"),
        )
        .withColumn(
            "genres",
            F.when(
                F.col("genres") == "(no genres listed)",
                F.lit(None).cast("string"),
            ).otherwise(F.col("genres")),
        )
        .dropDuplicates(["movieId"])
    )

    return transformed


def transform_ratings(
    dataframe: DataFrame,
) -> DataFrame:
    """
    Transform the Bronze rating's dataset.

    Args:
        dataframe: Bronze ratings DataFrame.

    Returns:
        Standardized Silver ratings DataFrame.
    """

    transformed = (
        dataframe
        .select(
            F.col("userId").cast("long").alias("userId"),
            F.col("movieId").cast("long").alias("movieId"),
            F.col("rating").cast("double").alias("rating"),
            F.col("timestamp").cast("long").alias(
                "sourceTimestamp"
            ),
        )
        .filter(
            F.col("rating").between(0.5, 5.0)
        )
        .withColumn(
            "ratingTimestamp",
            F.to_timestamp(
                F.from_unixtime(
                    F.col("sourceTimestamp")
                )
            ),
        )
        .dropDuplicates(
            [
                "userId",
                "movieId",
                "sourceTimestamp",
            ]
        )
    )

    return transformed


def transform_tags(
    dataframe: DataFrame,
) -> DataFrame:
    """
    Transform the Bronze tag's dataset.

    Args:
        dataframe: Bronze tags DataFrame.

    Returns:
        Standardized Silver tags DataFrame.
    """

    transformed = (
        dataframe
        .select(
            F.col("userId").cast("long").alias("userId"),
            F.col("movieId").cast("long").alias("movieId"),
            F.lower(
                F.trim(F.col("tag"))
            ).alias("tag"),
            F.col("timestamp").cast("long").alias(
                "sourceTimestamp"
            ),
        )
        .filter(
            F.col("tag").isNotNull()
            & (F.length(F.col("tag")) > 0)
        )
        .withColumn(
            "tagTimestamp",
            F.to_timestamp(
                F.from_unixtime(
                    F.col("sourceTimestamp")
                )
            ),
        )
        .dropDuplicates(
            [
                "userId",
                "movieId",
                "tag",
                "sourceTimestamp",
            ]
        )
    )

    return transformed


def transform_links(
    dataframe: DataFrame,
) -> DataFrame:
    """
    Transform the Bronze links dataset.

    Args:
        dataframe: Bronze links DataFrame.

    Returns:
        Standardized Silver links DataFrame.
    """

    transformed = (
        dataframe
        .select(
            F.col("movieId").cast("long").alias("movieId"),
            F.col("imdbId").cast("long").alias("imdbId"),
            F.col("tmdbId").cast("long").alias("tmdbId"),
        )
        .dropDuplicates(["movieId"])
    )

    return transformed