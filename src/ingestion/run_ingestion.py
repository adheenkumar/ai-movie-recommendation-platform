"""
Ingestion pipeline orchestrator.

Runs all MovieLens dataset ingestion tasks.
"""

from collections.abc import Callable

from src.ingestion.ingest_links import ingest_links
from src.ingestion.ingest_movies import ingest_movies
from src.ingestion.ingest_ratings import ingest_ratings
from src.ingestion.ingest_tags import ingest_tags
from src.utils.logger import get_logger

logger = get_logger(__name__)


INGESTION_TASKS: list[tuple[str, Callable[[], None]]] = [
    ("movies", ingest_movies),
    ("ratings", ingest_ratings),
    ("tags", ingest_tags),
    ("links", ingest_links),
]


def run_ingestion() -> None:
    """Run all dataset ingestion tasks."""

    logger.info("Starting ingestion pipeline")

    for dataset_name, ingestion_task in INGESTION_TASKS:
        logger.info(
            "Running ingestion task: %s",
            dataset_name,
        )

        ingestion_task()

        logger.info(
            "Ingestion task completed: %s",
            dataset_name,
        )

    logger.info("Ingestion pipeline completed successfully")


if __name__ == "__main__":
    run_ingestion()