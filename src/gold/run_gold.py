"""
Gold layer pipeline.
"""

from src.gold.movie_metrics import (
    build_movie_metrics,
    write_movie_metrics,
)
from src.spark_jobs.spark_session import (
    create_spark_session,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def run_gold() -> None:
    """
    Run the Gold layer.
    """

    logger.info(
        "Starting Gold pipeline."
    )

    spark = create_spark_session(
        "Movie Recommendation Gold"
    )

    try:
        movie_metrics = build_movie_metrics(
            spark
        )

        write_movie_metrics(
            movie_metrics
        )

    finally:
        spark.stop()

    logger.info(
        "Gold pipeline completed."
    )


if __name__ == "__main__":
    run_gold()