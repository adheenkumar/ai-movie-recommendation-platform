from src.recommendation.movie_search import MovieSearch
from src.spark_jobs.spark_session import create_spark_session
from src.dashboard.services.recommendation_service import (
    RecommendationService,
)

spark = create_spark_session(
    app_name="Movie Search Test",
)

search = MovieSearch(spark)

tests = [
    "Toy Story (1995)",
    "Toy",
    "Monsters Inc",
    "Batman",
]

for movie in tests:

    resolved, suggestions = search.resolve_title(movie)

    print("\n--------------------------------")

    print(f"Input: {movie}")

    print(f"Resolved: {resolved}")

    print("Suggestions:")

    for suggestion in suggestions:
        print(f"  - {suggestion}")

service = RecommendationService(spark)

recommendations, suggestions = (
    service.recommend_by_movie("Monsters Inc")
)

print("\nService Result")

print(recommendations)

print(suggestions)
