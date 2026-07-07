"""
Movie ingestion pipeline.

Reads movies.csv, validates it, and stores it as Parquet
in the Bronze layer.
"""

from src.ingestion.validator import validate_csv
from src.utils.logger import get_logger
from src.utils.paths import BRONZE_DATA_DIR, RAW_DATA_DIR

logger = get_logger(__name__)


def ingest_movies() -> None:
    """Ingest movies dataset into Bronze layer."""

    movies_df = validate_csv(
        RAW_DATA_DIR / "movies.csv",
        [
            "movieId",
            "title",
            "genres",
        ],
    )

    output_path = BRONZE_DATA_DIR / "movies.parquet"

    movies_df.to_parquet(
        output_path,
        index=False,
    )

    logger.info(
        f"Bronze dataset created: {output_path}"
    )


if __name__ == "__main__":
    ingest_movies()
