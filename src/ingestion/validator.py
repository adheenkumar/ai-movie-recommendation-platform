"""
Data validation utilities.
"""

from pathlib import Path

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def validate_csv(
    file_path: Path,
    required_columns: list[str],
) -> pd.DataFrame:
    """
    Validate and load a CSV file.

    Args:
        file_path: CSV file path
        required_columns: Required column names

    Returns:
        Validated pandas DataFrame

    Raises:
        FileNotFoundError
        ValueError
    """

    logger.info(f"Reading {file_path.name}")

    if not file_path.exists():
        logger.error(f"{file_path} not found.")
        raise FileNotFoundError(file_path)

    df = pd.read_csv(file_path)

    if df.empty:
        logger.error(f"{file_path.name} is empty.")
        raise ValueError("CSV file is empty.")

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        logger.error(
            f"Missing columns: {missing_columns}"
        )
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    logger.info(
        f"{file_path.name} loaded successfully "
        f"({len(df):,} rows)"
    )

    return df