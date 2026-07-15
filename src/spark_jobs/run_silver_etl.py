"""
Silver ETL pipeline orchestrator.

Runs Bronze-to-Silver PySpark transformations,
schema validation, and data quality validation for
all MovieLens datasets.
"""

from collections.abc import Callable

from pyspark.sql import DataFrame
from pyspark.sql.types import StructType

from src.spark_jobs.schemas import (
    LINKS_SCHEMA,
    MOVIES_SCHEMA,
    RATINGS_SCHEMA,
    TAGS_SCHEMA,
)
from src.spark_jobs.silver_processor import (
    TransformationFunction,
    process_silver_dataset,
)
from src.spark_jobs.silver_quality import (
    validate_links_quality,
    validate_movies_quality,
    validate_ratings_quality,
    validate_tags_quality,
)
from src.spark_jobs.silver_transformations import (
    transform_links,
    transform_movies,
    transform_ratings,
    transform_tags,
)
from src.spark_jobs.spark_session import (
    create_spark_session,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


QualityValidationFunction = Callable[
    [DataFrame],
    None,
]


SilverTask = tuple[
    str,
    TransformationFunction,
    StructType,
    QualityValidationFunction,
]


SILVER_TASKS: list[SilverTask] = [
    (
        "movies",
        transform_movies,
        MOVIES_SCHEMA,
        validate_movies_quality,
    ),
    (
        "ratings",
        transform_ratings,
        RATINGS_SCHEMA,
        validate_ratings_quality,
    ),
    (
        "tags",
        transform_tags,
        TAGS_SCHEMA,
        validate_tags_quality,
    ),
    (
        "links",
        transform_links,
        LINKS_SCHEMA,
        validate_links_quality,
    ),
]


def run_silver_etl() -> None:
    """Run the complete Bronze-to-Silver ETL pipeline."""

    logger.info(
        "Starting Silver ETL pipeline"
    )

    spark = create_spark_session(
        "Movie Recommendation Silver ETL"
    )

    try:
        for (
            dataset_name,
            transformation,
            expected_schema,
            quality_validator,
        ) in SILVER_TASKS:
            logger.info(
                "Running Silver task: %s",
                dataset_name,
            )

            process_silver_dataset(
                spark=spark,
                dataset_name=dataset_name,
                transformation=transformation,
                expected_schema=expected_schema,
                quality_validator=quality_validator,
            )

            logger.info(
                "Silver task completed: %s",
                dataset_name,
            )

    finally:
        spark.stop()

    logger.info(
        "Silver ETL pipeline completed successfully"
    )


if __name__ == "__main__":
    run_silver_etl()