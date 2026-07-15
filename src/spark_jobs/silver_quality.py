"""
Dataset-specific Silver data quality rules.

This module applies business-level validation rules to
the transformed MovieLens Silver datasets.
"""

from pyspark.sql import DataFrame

from src.spark_jobs.data_quality import (
    validate_non_empty_string,
    validate_numeric_range,
    validate_required_columns,
    validate_unique_key,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def validate_movies_quality(
    dataframe: DataFrame,
) -> None:
    """Validate the Silver movies dataset."""

    validate_required_columns(
        dataset_name="movies",
        dataframe=dataframe,
        required_columns=[
            "movieId",
            "title",
        ],
    )

    validate_unique_key(
        dataset_name="movies",
        dataframe=dataframe,
        key_columns=[
            "movieId",
        ],
    )

    validate_non_empty_string(
        dataset_name="movies",
        dataframe=dataframe,
        column_name="title",
    )

    logger.info(
        "Silver quality validation passed | dataset=movies"
    )


def validate_ratings_quality(
    dataframe: DataFrame,
) -> None:
    """Validate the Silver ratings dataset."""

    validate_required_columns(
        dataset_name="ratings",
        dataframe=dataframe,
        required_columns=[
            "userId",
            "movieId",
            "rating",
            "sourceTimestamp",
            "ratingTimestamp",
        ],
    )

    validate_numeric_range(
        dataset_name="ratings",
        dataframe=dataframe,
        column_name="rating",
        minimum=0.5,
        maximum=5.0,
    )

    validate_unique_key(
        dataset_name="ratings",
        dataframe=dataframe,
        key_columns=[
            "userId",
            "movieId",
            "sourceTimestamp",
        ],
    )

    logger.info(
        "Silver quality validation passed | dataset=ratings"
    )


def validate_tags_quality(
    dataframe: DataFrame,
) -> None:
    """Validate the Silver tags dataset."""

    validate_required_columns(
        dataset_name="tags",
        dataframe=dataframe,
        required_columns=[
            "userId",
            "movieId",
            "tag",
            "sourceTimestamp",
            "tagTimestamp",
        ],
    )

    validate_non_empty_string(
        dataset_name="tags",
        dataframe=dataframe,
        column_name="tag",
    )

    validate_unique_key(
        dataset_name="tags",
        dataframe=dataframe,
        key_columns=[
            "userId",
            "movieId",
            "tag",
            "sourceTimestamp",
        ],
    )

    logger.info(
        "Silver quality validation passed | dataset=tags"
    )


def validate_links_quality(
    dataframe: DataFrame,
) -> None:
    """Validate the Silver links dataset."""

    validate_required_columns(
        dataset_name="links",
        dataframe=dataframe,
        required_columns=[
            "movieId",
            "imdbId",
        ],
    )

    validate_unique_key(
        dataset_name="links",
        dataframe=dataframe,
        key_columns=[
            "movieId",
        ],
    )

    logger.info(
        "Silver quality validation passed | dataset=links"
    )