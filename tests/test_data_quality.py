"""
Tests for reusable PySpark data quality validation.
"""

import pytest
from pyspark.sql import SparkSession

from src.spark_jobs.data_quality import (
    validate_non_empty_string,
    validate_numeric_range,
    validate_required_columns,
    validate_unique_key,
)
from src.spark_jobs.spark_session import create_spark_session


@pytest.fixture(scope="module")
def spark() -> SparkSession:
    """Create a Spark session for quality tests."""

    spark_session = create_spark_session(
        "Data Quality Tests"
    )

    yield spark_session

    spark_session.stop()


def test_required_columns_reject_nulls(
    spark: SparkSession,
) -> None:
    """Verify required fields reject null values."""

    dataframe = spark.createDataFrame(
        [
            (1, "Movie A"),
            (2, None),
        ],
        "movieId long, title string",
    )

    with pytest.raises(
        ValueError,
        match="Required column validation failed",
    ):
        validate_required_columns(
            dataset_name="movies",
            dataframe=dataframe,
            required_columns=[
                "movieId",
                "title",
            ],
        )


def test_unique_key_rejects_duplicates(
    spark: SparkSession,
) -> None:
    """Verify duplicate keys fail validation."""

    dataframe = spark.createDataFrame(
        [
            (1, "Movie A"),
            (1, "Movie B"),
        ],
        "movieId long, title string",
    )

    with pytest.raises(
        ValueError,
        match="Unique key validation failed",
    ):
        validate_unique_key(
            dataset_name="movies",
            dataframe=dataframe,
            key_columns=[
                "movieId",
            ],
        )


def test_numeric_range_rejects_invalid_values(
    spark: SparkSession,
) -> None:
    """Verify out-of-range numeric values fail."""

    dataframe = spark.createDataFrame(
        [
            (4.5,),
            (6.0,),
        ],
        "rating double",
    )

    with pytest.raises(
        ValueError,
        match="Numeric range validation failed",
    ):
        validate_numeric_range(
            dataset_name="ratings",
            dataframe=dataframe,
            column_name="rating",
            minimum=0.5,
            maximum=5.0,
        )


def test_non_empty_string_rejects_blank_values(
    spark: SparkSession,
) -> None:
    """Verify blank strings fail validation."""

    dataframe = spark.createDataFrame(
        [
            ("sci-fi",),
            ("   ",),
        ],
        "tag string",
    )

    with pytest.raises(
        ValueError,
        match="Non-empty string validation failed",
    ):
        validate_non_empty_string(
            dataset_name="tags",
            dataframe=dataframe,
            column_name="tag",
        )