"""
Dataset quality profiling utilities.

This module generates basic data quality metrics for
pandas DataFrames during ingestion.
"""

from typing import Any

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def generate_quality_report(
    dataset_name: str,
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Generate data quality metrics for a DataFrame.

    Args:
        dataset_name: Name of the dataset.
        dataframe: DataFrame to profile.

    Returns:
        Dictionary containing data quality metrics.
    """

    null_counts = dataframe.isna().sum().to_dict()

    report = {
        "dataset": dataset_name,
        "row_count": len(dataframe),
        "column_count": len(dataframe.columns),
        "duplicate_rows": int(dataframe.duplicated().sum()),
        "total_null_values": int(dataframe.isna().sum().sum()),
        "null_counts": {
            column: int(count)
            for column, count in null_counts.items()
        },
        "data_types": {
            column: str(dtype)
            for column, dtype in dataframe.dtypes.items()
        },
    }

    logger.info(
        "Quality report generated for dataset: %s",
        dataset_name,
    )

    return report


def log_quality_report(
    report: dict[str, Any],
) -> None:
    """
    Log a summarized data quality report.

    Args:
        report: Data quality report dictionary.
    """

    logger.info(
        "Quality summary | dataset=%s | rows=%s | "
        "columns=%s | duplicates=%s | nulls=%s",
        report["dataset"],
        report["row_count"],
        report["column_count"],
        report["duplicate_rows"],
        report["total_null_values"],
    )