"""
Reusable Bronze-to-Silver dataset processor.

This module reads Bronze Parquet datasets, applies
PySpark transformations, validates output schemas and
data quality, and writes standardized Silver datasets.
"""

from collections.abc import Callable

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType

from src.spark_jobs.schema_validator import validate_schema
from src.utils.logger import get_logger
from src.utils.paths import (
    BRONZE_DATA_DIR,
    SILVER_DATA_DIR,
)

logger = get_logger(__name__)


TransformationFunction = Callable[
    [DataFrame],
    DataFrame,
]


QualityValidationFunction = Callable[
    [DataFrame],
    None,
]


def process_silver_dataset(
    spark: SparkSession,
    dataset_name: str,
    transformation: TransformationFunction,
    expected_schema: StructType,
    quality_validator: QualityValidationFunction,
) -> None:
    """
    Process one Bronze dataset into the Silver layer.

    Args:
        spark: Active Spark session.
        dataset_name: Dataset name without file extension.
        transformation: PySpark transformation function.
        expected_schema: Expected Silver schema contract.
        quality_validator: Dataset data quality validator.
    """

    input_path = (
        BRONZE_DATA_DIR
        / f"{dataset_name}.parquet"
    )

    output_path = (
        SILVER_DATA_DIR
        / f"{dataset_name}.parquet"
    )

    logger.info(
        "Starting Silver processing: %s",
        dataset_name,
    )

    bronze_dataframe = spark.read.parquet(
        str(input_path)
    )

    bronze_row_count = bronze_dataframe.count()

    logger.info(
        "Bronze dataset loaded | dataset=%s | rows=%s",
        dataset_name,
        bronze_row_count,
    )

    silver_dataframe = transformation(
        bronze_dataframe
    )

    validate_schema(
        dataset_name=dataset_name,
        dataframe=silver_dataframe,
        expected_schema=expected_schema,
    )

    quality_validator(
        silver_dataframe
    )

    silver_row_count = silver_dataframe.count()

    logger.info(
        "Silver transformation completed | "
        "dataset=%s | bronze_rows=%s | silver_rows=%s",
        dataset_name,
        bronze_row_count,
        silver_row_count,
    )

    (
        silver_dataframe
        .write
        .mode("overwrite")
        .parquet(str(output_path))
    )

    logger.info(
        "Silver dataset written | dataset=%s | path=%s",
        dataset_name,
        output_path,
    )