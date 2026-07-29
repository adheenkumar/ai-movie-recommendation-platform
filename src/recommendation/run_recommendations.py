"""
Command-line interface for the recommendation engines.
"""

from __future__ import annotations

import argparse
import time

from src.recommendation.config import DEFAULT_TOP_N
from src.recommendation.content_based import ContentBasedRecommender
from src.recommendation.collaborative import CollaborativeRecommender
from src.recommendation.hybrid import HybridRecommender
from src.recommendation.models import RecommendationResult
from src.recommendation.popularity import get_top_movies
from src.spark_jobs.spark_session import create_spark_session
from src.utils.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------


def print_results(
    recommendations: list[RecommendationResult],
) -> None:
    """
    Display recommendations.
    """

    if not recommendations:
        print("\nNo recommendations found.")
        return

    print()

    for rank, result in enumerate(recommendations, start=1):

        movie = result.recommendation

        genres = movie.genres.replace("|", ", ")

        print(f"{rank:>2}. {movie.title}")
        print(f"    Movie ID         : {movie.movie_id}")
        print(f"    Genres          : {genres}")
        print(f"    Average Rating  : {movie.average_rating:.2f}")
        print(f"    Rating Count    : {movie.rating_count}")
        print(f"    Weighted Rating : {movie.weighted_rating:.2f}")
        print(f"    Popularity      : {movie.popularity_score:.4f}")
        print(f"    Score           : {result.score:.4f}")
        print(f"    Source          : {result.source}")
        print()


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """
    Build command-line argument parser.
    """

    parser = argparse.ArgumentParser(description="Movie Recommendation Engine")

    parser.add_argument(
        "--mode",
        choices=[
            "popularity",
            "content",
            "collaborative",
            "hybrid",
        ],
        default="hybrid",
        help="Recommendation algorithm.",
    )

    parser.add_argument(
        "--movie",
        default="Toy Story (1995)",
        help="Movie title for recommendations.",
    )

    parser.add_argument(
        "--top",
        type=int,
        default=DEFAULT_TOP_N,
        help="Number of recommendations.",
    )

    parser.add_argument(
        "--semantic-query",
        default=None,
        help="Natural language query for semantic recommendations.",
    )

    return parser


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------


def main() -> None:

    parser = build_parser()
    args = parser.parse_args()

    logger.info(
        "Starting recommendation engine (%s).",
        args.mode,
    )

    start_time = time.perf_counter()

    spark = create_spark_session("Movie Recommendation")

    try:

        recommenders = {
            "popularity": lambda: get_top_movies(
                spark,
                top_n=args.top,
            ),
            "content": lambda: ContentBasedRecommender(spark).recommend(
                args.movie,
                top_n=args.top,
            ),
            "collaborative": lambda: CollaborativeRecommender(spark).recommend(
                args.movie,
                top_n=args.top,
            ),
            "hybrid": lambda: HybridRecommender(spark).recommend(
                args.movie,
                semantic_query=args.semantic_query,
                top_n=args.top,
            ),
        }

        recommendations = recommenders[args.mode]()

        print_results(recommendations)

        elapsed = time.perf_counter() - start_time

        logger.info(
            "Recommendation completed in %.2f seconds.",
            elapsed,
        )

        print(f"\nCompleted in {elapsed:.2f} seconds.")

    except KeyboardInterrupt:

        logger.warning("Recommendation cancelled by user.")

    except ValueError as exc:

        logger.error("%s", exc)

        print(f"\nError: {exc}")

    except Exception:

        logger.exception("Unexpected error while generating recommendations.")

        raise

    finally:

        spark.stop()

        logger.info("Spark session stopped.")


if __name__ == "__main__":
    main()
