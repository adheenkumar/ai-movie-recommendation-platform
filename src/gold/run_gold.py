"""
Gold layer pipeline.
"""

from src.gold.movie_metrics import (
    build_movie_metrics,
    write_movie_metrics,
)
from src.gold.genre_metrics import (
    build_genre_metrics,
    write_genre_metrics,
)
from src.gold.user_preferences import (
    build_user_preferences,
    write_user_preferences,
)
from src.gold.recommendation_features import (
    build_recommendation_features,
    write_recommendation_features,
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

        genre_metrics = (
            build_genre_metrics(
                spark
            )
        )

        write_genre_metrics(
            genre_metrics
        )

        user_preferences = (
            build_user_preferences(
                spark
            )
        )

        write_user_preferences(
            user_preferences
        )

        recommendation_features = (
            build_recommendation_features(
                spark
            )
        )

        write_recommendation_features(
            recommendation_features
        )

    finally:
        spark.stop()

    logger.info(
        "Gold pipeline completed."
    )


if __name__ == "__main__":
    run_gold()