from src.ingestion.validator import validate_csv
from src.utils.paths import RAW_DATA_DIR

movies = validate_csv(
    RAW_DATA_DIR / "movies.csv",
    [
        "movieId",
        "title",
        "genres",
    ],
)

print(movies.head())
