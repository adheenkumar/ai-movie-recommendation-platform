from src.spark_jobs.spark_session import create_spark_session
from src.utils.paths import GOLD_DATA_DIR

spark = create_spark_session("Inspect Users")

df = spark.read.parquet(str(GOLD_DATA_DIR / "user_preferences.parquet"))

df.printSchema()

df.show(
    20,
    False,
)

spark.stop()
