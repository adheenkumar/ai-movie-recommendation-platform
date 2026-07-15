"""
Silver schema validation utilities.

This module validates transformed DataFrames against
expected Silver schema contracts.
"""

from pyspark.sql import DataFrame
from pyspark.sql.types import StructType

from src.utils.logger import get_logger

logger = get_logger(__name__)


def validate_schema(
    dataset_name: str,
    dataframe: DataFrame,
    expected_schema: StructType,
) -> None:
    """
    Validate DataFrame columns and data types.

    Args:
        dataset_name: Name of the dataset.
        dataframe: DataFrame to validate.
        expected_schema: Expected schema contract.

    Raises:
        ValueError: If columns or data types do not match.
    """

    actual_fields = {
        field.name: field.dataType
        for field in dataframe.schema.fields
    }

    expected_fields = {
        field.name: field.dataType
        for field in expected_schema.fields
    }

    actual_columns = list(actual_fields)
    expected_columns = list(expected_fields)

    if actual_columns != expected_columns:
        logger.error(
            "Schema column mismatch | "
            "dataset=%s | expected=%s | actual=%s",
            dataset_name,
            expected_columns,
            actual_columns,
        )

        raise ValueError(
            f"Schema column mismatch for {dataset_name}. "
            f"Expected {expected_columns}, "
            f"received {actual_columns}."
        )

    type_mismatches = {
        column: {
            "expected": str(expected_fields[column]),
            "actual": str(actual_fields[column]),
        }
        for column in expected_columns
        if actual_fields[column] != expected_fields[column]
    }

    if type_mismatches:
        logger.error(
            "Schema type mismatch | "
            "dataset=%s | mismatches=%s",
            dataset_name,
            type_mismatches,
        )

        raise ValueError(
            f"Schema type mismatch for {dataset_name}: "
            f"{type_mismatches}"
        )

    logger.info(
        "Schema validation passed | dataset=%s",
        dataset_name,
    )