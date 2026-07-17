"""
Gold genre analytics.
"""

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from src.utils.logger import get_logger
from src.utils.paths import GOLD_DATA_DIR

logger = get_logger(__name__)

def build_genre_metrics(
    spark: SparkSession,
) -> DataFrame:

    logger.info(
        "Reading movie metrics."
    )

    movies = spark.read.parquet(
        str(
            GOLD_DATA_DIR /
            "movie_metrics.parquet"
        )
    )

    movies = (
        movies
        .withColumn(
            "genre",
            F.split(F.col("genres"), "\\|"),
        )
        .withColumn(
            "genreName",
            F.explode("genre"),
        )
        .drop("genre")
    )

    genre_metrics = (
        movies
        .groupBy("genreName")
        .agg(
            F.countDistinct(
                "movieId"
            ).alias("movieCount"),

            F.round(
                F.avg(
                    "averageRating"
                ),
                3,
            ).alias(
                "averageRating"
            ),

            F.round(
                F.avg(
                    "weightedRating"
                ),
                3,
            ).alias(
                "averageWeightedRating"
            ),

            F.round(
                F.avg(
                    "popularityScore"
                ),
                4,
            ).alias(
                "averagePopularity"
            ),
        )
    )

    genre_metrics = (
        genre_metrics
        .orderBy(
            F.desc(
                "averageWeightedRating"
            )
        )
    )

    logger.info(
        "Genre metrics generated: %d rows",
        genre_metrics.count(),
    )

    return genre_metrics

def write_genre_metrics(
    dataframe: DataFrame,
):

    output = (
        GOLD_DATA_DIR
        /
        "genre_metrics.parquet"
    )

    (
        dataframe.write
        .mode("overwrite")
        .parquet(
            str(output)
        )
    )

    logger.info(
        "Genre metrics written: %s",
        output,
    )