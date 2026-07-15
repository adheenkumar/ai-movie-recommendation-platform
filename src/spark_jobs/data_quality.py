"""
Silver-layer data quality validation.

This module defines reusable PySpark data quality checks
for required fields, uniqueness, numeric ranges, and
dataset-specific business rules.
"""


from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.utils.logger import get_logger

logger = get_logger(__name__)


def count_nulls(
    dataframe: DataFrame,
    column_name: str,
) -> int:
    """
    Count null values in a DataFrame column.

    Args:
        dataframe: DataFrame to validate.
        column_name: Column to inspect.

    Returns:
        Number of null values.
    """

    return dataframe.filter(
        F.col(column_name).isNull()
    ).count()


def count_duplicate_keys(
    dataframe: DataFrame,
    key_columns: list[str],
) -> int:
    """
    Count duplicate key groups.

    Args:
        dataframe: DataFrame to validate.
        key_columns: Columns forming the uniqueness key.

    Returns:
        Number of duplicated key groups.
    """

    return (
        dataframe
        .groupBy(*key_columns)
        .count()
        .filter(
            F.col("count") > 1
        )
        .count()
    )


def validate_required_columns(
    dataset_name: str,
    dataframe: DataFrame,
    required_columns: list[str],
) -> None:
    """
    Validate required columns contain no null values.

    Args:
        dataset_name: Name of the dataset.
        dataframe: DataFrame to validate.
        required_columns: Columns that must not contain nulls.

    Raises:
        ValueError: If null values are found.
    """

    null_counts = {
        column_name: count_nulls(
            dataframe,
            column_name,
        )
        for column_name in required_columns
    }

    violations = {
        column_name: null_count
        for column_name, null_count
        in null_counts.items()
        if null_count > 0
    }

    if violations:
        logger.error(
            "Required column validation failed | "
            "dataset=%s | violations=%s",
            dataset_name,
            violations,
        )

        raise ValueError(
            f"Required column validation failed "
            f"for {dataset_name}: {violations}"
        )

    logger.info(
        "Required column validation passed | dataset=%s",
        dataset_name,
    )


def validate_unique_key(
    dataset_name: str,
    dataframe: DataFrame,
    key_columns: list[str],
) -> None:
    """
    Validate uniqueness for a dataset key.

    Args:
        dataset_name: Name of the dataset.
        dataframe: DataFrame to validate.
        key_columns: Columns forming the unique key.

    Raises:
        ValueError: If duplicate keys are found.
    """

    duplicate_count = count_duplicate_keys(
        dataframe,
        key_columns,
    )

    if duplicate_count > 0:
        logger.error(
            "Unique key validation failed | "
            "dataset=%s | keys=%s | duplicate_groups=%s",
            dataset_name,
            key_columns,
            duplicate_count,
        )

        raise ValueError(
            f"Unique key validation failed "
            f"for {dataset_name}: "
            f"{duplicate_count} duplicate groups"
        )

    logger.info(
        "Unique key validation passed | "
        "dataset=%s | keys=%s",
        dataset_name,
        key_columns,
    )


def validate_numeric_range(
    dataset_name: str,
    dataframe: DataFrame,
    column_name: str,
    minimum: float,
    maximum: float,
) -> None:
    """
    Validate that numeric values fall within a range.

    Args:
        dataset_name: Name of the dataset.
        dataframe: DataFrame to validate.
        column_name: Numeric column to inspect.
        minimum: Minimum allowed value.
        maximum: Maximum allowed value.

    Raises:
        ValueError: If out-of-range values are found.
    """

    violation_count = (
        dataframe
        .filter(
            ~F.col(column_name).between(
                minimum,
                maximum,
            )
        )
        .count()
    )

    if violation_count > 0:
        logger.error(
            "Numeric range validation failed | "
            "dataset=%s | column=%s | "
            "minimum=%s | maximum=%s | violations=%s",
            dataset_name,
            column_name,
            minimum,
            maximum,
            violation_count,
        )

        raise ValueError(
            f"Numeric range validation failed "
            f"for {dataset_name}.{column_name}: "
            f"{violation_count} violations"
        )

    logger.info(
        "Numeric range validation passed | "
        "dataset=%s | column=%s",
        dataset_name,
        column_name,
    )


def validate_non_empty_string(
    dataset_name: str,
    dataframe: DataFrame,
    column_name: str,
) -> None:
    """
    Validate that string values are not blank.

    Args:
        dataset_name: Name of the dataset.
        dataframe: DataFrame to validate.
        column_name: String column to inspect.

    Raises:
        ValueError: If blank strings are found.
    """

    violation_count = (
        dataframe
        .filter(
            F.col(column_name).isNotNull()
            & (
                F.length(
                    F.trim(F.col(column_name))
                )
                == 0
            )
        )
        .count()
    )

    if violation_count > 0:
        logger.error(
            "Non-empty string validation failed | "
            "dataset=%s | column=%s | violations=%s",
            dataset_name,
            column_name,
            violation_count,
        )

        raise ValueError(
            f"Non-empty string validation failed "
            f"for {dataset_name}.{column_name}: "
            f"{violation_count} violations"
        )

    logger.info(
        "Non-empty string validation passed | "
        "dataset=%s | column=%s",
        dataset_name,
        column_name,
    )