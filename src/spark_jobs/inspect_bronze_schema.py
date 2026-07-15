"""
Bronze schema inspection utility.

This module displays Spark-inferred schemas for the
Bronze MovieLens Parquet datasets.
"""

from src.spark_jobs.spark_session import create_spark_session
from src.utils.logger import get_logger
from src.utils.paths import BRONZE_DATA_DIR

logger = get_logger(__name__)


DATASETS = [
    "movies",
    "ratings",
    "tags",
    "links",
]


def inspect_bronze_schemas() -> None:
    """Inspect schemas for all Bronze datasets."""

    spark = create_spark_session(
        "Bronze Schema Inspection"
    )

    try:
        for dataset_name in DATASETS:
            input_path = (
                BRONZE_DATA_DIR
                / f"{dataset_name}.parquet"
            )

            logger.info(
                "Inspecting Bronze schema: %s",
                dataset_name,
            )

            dataframe = spark.read.parquet(
                str(input_path)
            )

            print(
                f"\n===== {dataset_name.upper()} ====="
            )

            dataframe.printSchema()

    finally:
        spark.stop()


if __name__ == "__main__":
    inspect_bronze_schemas()