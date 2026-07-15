"""
Silver dataset inspection utility.

Displays schemas, row counts, and sample records for
the generated Silver MovieLens datasets.
"""

from src.spark_jobs.spark_session import (
    create_spark_session,
)
from src.utils.paths import SILVER_DATA_DIR


DATASETS = [
    "movies",
    "ratings",
    "tags",
    "links",
]


def inspect_silver_data() -> None:
    """Inspect generated Silver datasets."""

    spark = create_spark_session(
        "Silver Data Inspection"
    )

    try:
        for dataset_name in DATASETS:
            input_path = (
                SILVER_DATA_DIR
                / f"{dataset_name}.parquet"
            )

            dataframe = spark.read.parquet(
                str(input_path)
            )

            print(
                f"\n===== {dataset_name.upper()} ====="
            )

            print(
                f"Row count: {dataframe.count():,}"
            )

            dataframe.printSchema()

            dataframe.show(
                5,
                truncate=False,
            )

    finally:
        spark.stop()


if __name__ == "__main__":
    inspect_silver_data()