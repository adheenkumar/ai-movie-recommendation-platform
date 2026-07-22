"""
Gold movie metrics generation.

Creates the primary Gold analytical dataset containing
movie-level rating metrics for downstream analytics and
recommendation models.
"""

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from src.utils.logger import get_logger
from src.utils.paths import GOLD_DATA_DIR, SILVER_DATA_DIR

logger = get_logger(__name__)

MINIMUM_VOTES = 50


def build_movie_metrics(
    spark: SparkSession,
) -> DataFrame:
    """
    Build the Gold movie metrics dataset.

    Args:
        spark:
            Active Spark session.

    Returns:
        Gold movie metrics DataFrame.
    """

    logger.info("Reading Silver datasets.")

    movies = spark.read.parquet(str(SILVER_DATA_DIR / "movies.parquet"))

    ratings = spark.read.parquet(str(SILVER_DATA_DIR / "ratings.parquet"))

    logger.info("Aggregating ratings.")

    rating_metrics = ratings.groupBy("movieId").agg(
        F.count("*").alias("ratingCount"),
        F.avg("rating").alias("averageRating"),
    )

    global_average = ratings.agg(F.avg("rating").alias("globalAverage")).first()[
        "globalAverage"
    ]

    logger.info(
        "Global average rating: %.4f",
        global_average,
    )

    logger.info("Joining movie metadata.")

    movie_metrics = movies.join(
        rating_metrics,
        on="movieId",
        how="left",
    ).fillna(
        {
            "ratingCount": 0,
            "averageRating": global_average,
        }
    )

    logger.info("Calculating weighted rating.")

    movie_metrics = movie_metrics.withColumn(
        "weightedRating",
        (
            (F.col("ratingCount") / (F.col("ratingCount") + F.lit(MINIMUM_VOTES)))
            * F.col("averageRating")
        )
        + (
            (F.lit(MINIMUM_VOTES) / (F.col("ratingCount") + F.lit(MINIMUM_VOTES)))
            * F.lit(global_average)
        ),
    )

    logger.info("Calculating popularity score.")

    maximum_votes = movie_metrics.agg(F.max("ratingCount").alias("maxVotes")).first()[
        "maxVotes"
    ]

    movie_metrics = movie_metrics.withColumn(
        "popularityScore",
        F.round(
            F.col("ratingCount") / F.lit(maximum_votes),
            4,
        ),
    )

    movie_metrics = movie_metrics.select(
        "movieId",
        "title",
        "releaseYear",
        "genres",
        "ratingCount",
        F.round(
            "averageRating",
            3,
        ).alias("averageRating"),
        F.round(
            "weightedRating",
            3,
        ).alias("weightedRating"),
        "popularityScore",
    )

    logger.info(
        "Movie metrics generated: %s rows",
        movie_metrics.count(),
    )

    return movie_metrics


def write_movie_metrics(
    dataframe: DataFrame,
) -> None:
    """
    Write the Gold movie metrics dataset.
    """

    output_path = GOLD_DATA_DIR / "movie_metrics.parquet"

    (dataframe.write.mode("overwrite").parquet(str(output_path)))

    logger.info(
        "Gold dataset written: %s",
        output_path,
    )
