from src.spark_jobs.spark_session import create_spark_session
from src.utils.paths import GOLD_DATA_DIR

spark = create_spark_session("Inspect Recommendation Features")

df = spark.read.parquet(str(GOLD_DATA_DIR / "recommendation_features.parquet"))

df.printSchema()

df.select(
    "movieId",
    "title",
    "tags",
    "contentText",
).show(
    10,
    truncate=False,
)

spark.stop()
