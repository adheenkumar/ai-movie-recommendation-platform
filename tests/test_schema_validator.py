"""
Tests for Silver schema validation.
"""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    LongType,
    StringType,
    StructField,
    StructType,
)

from src.spark_jobs.schema_validator import validate_schema
from src.spark_jobs.spark_session import create_spark_session


@pytest.fixture(scope="module")
def spark() -> SparkSession:
    """Create a Spark session for schema tests."""

    spark_session = create_spark_session(
        "Schema Validator Tests"
    )

    yield spark_session

    spark_session.stop()


def test_validate_schema_passes(
    spark: SparkSession,
) -> None:
    """Verify matching schemas pass validation."""

    dataframe = spark.createDataFrame(
        [
            (1, "Movie A"),
        ],
        "movieId long, title string",
    )

    expected_schema = StructType(
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
        ]
    )

    validate_schema(
        dataset_name="test_movies",
        dataframe=dataframe,
        expected_schema=expected_schema,
    )


def test_validate_schema_rejects_type_mismatch(
    spark: SparkSession,
) -> None:
    """Verify type mismatches fail validation."""

    dataframe = spark.createDataFrame(
        [
            ("1", "Movie A"),
        ],
        "movieId string, title string",
    )

    expected_schema = StructType(
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
        ]
    )

    with pytest.raises(
        ValueError,
        match="Schema type mismatch",
    ):
        validate_schema(
            dataset_name="test_movies",
            dataframe=dataframe,
            expected_schema=expected_schema,
        )