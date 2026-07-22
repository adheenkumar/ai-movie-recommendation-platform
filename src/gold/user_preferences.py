"""
Gold user preference analytics.
"""

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import Window
from pyspark.sql import functions as F

from src.utils.logger import get_logger
from src.utils.paths import (
    GOLD_DATA_DIR,
    SILVER_DATA_DIR,
)

logger = get_logger(__name__)


def build_user_preferences(
    spark: SparkSession,
) -> DataFrame:

    logger.info("Reading Silver datasets.")

    movies = spark.read.parquet(str(SILVER_DATA_DIR / "movies.parquet"))

    ratings = spark.read.parquet(str(SILVER_DATA_DIR / "ratings.parquet"))

    ratings = ratings.join(
        movies.select(
            "movieId",
            "genres",
        ),
        on="movieId",
        how="left",
    )

    user_stats = ratings.groupBy("userId").agg(
        F.count("*").alias("moviesRated"),
        F.round(
            F.avg("rating"),
            3,
        ).alias("averageRatingGiven"),
        F.min("rating").alias("minimumRating"),
        F.max("rating").alias("maximumRating"),
        F.round(
            F.variance("rating"),
            3,
        ).alias("ratingVariance"),
    )

    genres = ratings.withColumn(
        "genre",
        F.split(
            "genres",
            "\\|",
        ),
    )

    genres = genres.select(
        "userId",
        F.explode("genre").alias("genreName"),
    )

    genre_counts = genres.groupBy(
        "userId",
        "genreName",
    ).count()

    window = Window.partitionBy("userId").orderBy(
        F.desc("count"),
        F.asc("genreName"),
    )

    favorite_genre = (
        genre_counts.withColumn(
            "rank",
            F.row_number().over(window),
        )
        .filter(F.col("rank") == 1)
        .select(
            "userId",
            F.col("genreName").alias("favoriteGenre"),
        )
    )

    preferences = user_stats.join(
        favorite_genre,
        on="userId",
        how="left",
    ).orderBy("userId")

    logger.info(
        "User preferences generated: %d rows",
        preferences.count(),
    )

    return preferences


def write_user_preferences(
    dataframe: DataFrame,
):

    output = GOLD_DATA_DIR / "user_preferences.parquet"

    (dataframe.write.mode("overwrite").parquet(str(output)))

    logger.info(
        "User preferences written: %s",
        output,
    )
