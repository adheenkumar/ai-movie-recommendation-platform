import pandas as pd

from src.utils.paths import BRONZE_DATA_DIR

df = pd.read_parquet(
    BRONZE_DATA_DIR / "movies.parquet"
)

print(df.head())

print()

print(df.info())