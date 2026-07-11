"""
Generic dataset ingestion utility.

This module validates raw CSV datasets, generates data
quality metrics, and writes them to the Bronze layer
in Parquet format.
"""

from collections.abc import Sequence

from src.ingestion.quality_report import (
    generate_quality_report,
    log_quality_report,
)
from src.ingestion.validator import validate_csv
from src.utils.logger import get_logger
from src.utils.paths import BRONZE_DATA_DIR, RAW_DATA_DIR

logger = get_logger(__name__)


def ingest_dataset(
    dataset_name: str,
    required_columns: Sequence[str],
) -> None:
    """
    Ingest a raw CSV dataset into the Bronze layer.

    The ingestion process performs the following steps:

    1. Resolve source and destination paths.
    2. Validate the source CSV file.
    3. Generate data quality metrics.
    4. Log the data quality summary.
    5. Write the dataset to Bronze Parquet storage.

    Args:
        dataset_name: Dataset name without the file extension.
        required_columns: Columns required in the source dataset.
    """

    input_path = RAW_DATA_DIR / f"{dataset_name}.csv"
    output_path = BRONZE_DATA_DIR / f"{dataset_name}.parquet"

    logger.info(
        "Starting ingestion for dataset: %s",
        dataset_name,
    )

    dataframe = validate_csv(
        file_path=input_path,
        required_columns=list(required_columns),
    )

    quality_report = generate_quality_report(
        dataset_name=dataset_name,
        dataframe=dataframe,
    )

    log_quality_report(quality_report)

    dataframe.to_parquet(
        output_path,
        index=False,
    )

    logger.info(
        "Dataset %s written to Bronze layer: %s",
        dataset_name,
        output_path,
    )