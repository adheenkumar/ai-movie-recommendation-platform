"""
Centralized Spark session configuration.

This module provides a reusable SparkSession factory
for the project's PySpark ETL jobs.
"""

from pyspark.sql import SparkSession

from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_spark_session(
    app_name: str,
) -> SparkSession:
    """
    Create and return a configured Spark session.

    Args:
        app_name: Name of the Spark application.

    Returns:
        Configured SparkSession instance.
    """

    logger.info(
        "Creating Spark session: %s",
        app_name,
    )

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config(
            "spark.sql.session.timeZone",
            "UTC",
        )
        .config(
            "spark.sql.parquet.compression.codec",
            "snappy",
        )
        .config(
            "spark.sql.shuffle.partitions",
            "4",
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    logger.info(
        "Spark session created successfully | "
        "version=%s | app=%s",
        spark.version,
        app_name,
    )

    return spark