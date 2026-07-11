"""
Generic dataset ingestion utility.

This module validates raw CSV datasets and writes them
to the Bronze layer in Parquet format.
"""

from collections.abc import Sequence

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

    Args:
        dataset_name: Dataset name without file extension.
        required_columns: Columns required in the source dataset.
    """

    input_path = RAW_DATA_DIR / f"{dataset_name}.csv"
    output_path = BRONZE_DATA_DIR / f"{dataset_name}.parquet"

    logger.info("Starting ingestion for dataset: %s", dataset_name)

    dataframe = validate_csv(
        file_path=input_path,
        required_columns=list(required_columns),
    )

    dataframe.to_parquet(
        output_path,
        index=False,
    )

    logger.info(
        "Dataset %s written to Bronze layer: %s",
        dataset_name,
        output_path,
    )