"""
Recommendation feature dataset generation.
"""

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from src.utils.logger import get_logger
from src.utils.paths import (
    GOLD_DATA_DIR,
    SILVER_DATA_DIR,
)

logger = get_logger(__name__)


def build_recommendation_features(
    spark: SparkSession,
) -> DataFrame:
    """
    Build a feature dataset for semantic search and recommendation.
    """

    logger.info(
        "Reading Gold movie metrics."
    )

    movie_metrics = spark.read.parquet(
        str(
            GOLD_DATA_DIR /
            "movie_metrics.parquet"
        )
    )

    logger.info(
        "Reading Silver tags."
    )

    tags = spark.read.parquet(
        str(
            SILVER_DATA_DIR /
            "tags.parquet"
        )
    )

    logger.info(
        "Aggregating movie tags."
    )

    tag_features = (
        tags
        .groupBy("movieId")
        .agg(
            F.concat_ws(
                ", ",
                F.array_sort(
                    F.collect_set("tag")
                ),
            ).alias("tags")
        )
    )

    logger.info(
        "Joining movie metrics with tags."
    )

    features = (
        movie_metrics
        .join(
            tag_features,
            on="movieId",
            how="left",
        )
    )

    features = features.fillna(
        {
            "tags": "No tags available"
        }
    )

    # Convert MovieLens genre separator into readable text
    genres_text = F.regexp_replace(
        F.col("genres"),
        "\\|",
        ", ",
    )

    logger.info(
        "Generating content text."
    )

    features = features.withColumn(
        "contentText",
        F.concat_ws(
            ". ",
            F.concat(
                F.lit("Title: "),
                F.col("title"),
            ),
            F.concat(
                F.lit("Genres: "),
                genres_text,
            ),
            F.concat(
                F.lit("Tags: "),
                F.col("tags"),
            ),
            F.concat(
                F.lit("Average Rating: "),
                F.round(
                    F.col("averageRating"),
                    2,
                ).cast("string"),
            ),
            F.concat(
                F.lit("Weighted Rating: "),
                F.round(
                    F.col("weightedRating"),
                    2,
                ).cast("string"),
            ),
            F.concat(
                F.lit("Popularity Score: "),
                F.round(
                    F.col("popularityScore"),
                    4,
                ).cast("string"),
            ),
        ),
    )

    features = features.select(
        "movieId",
        "title",
        "releaseYear",
        "genres",
        "ratingCount",
        "averageRating",
        "weightedRating",
        "popularityScore",
        "tags",
        "contentText",
    )

    logger.info(
        "Recommendation features generated: %d rows",
        features.count(),
    )

    return features


def write_recommendation_features(
    dataframe: DataFrame,
) -> None:
    """
    Write recommendation features to the Gold layer.
    """

    output = (
        GOLD_DATA_DIR /
        "recommendation_features.parquet"
    )

    (
        dataframe.write
        .mode("overwrite")
        .parquet(
            str(output)
        )
    )

    logger.info(
        "Recommendation features written: %s",
        output,
    )