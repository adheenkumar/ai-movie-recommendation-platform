"""
Analytics page for the AI Movie Recommendation Platform.
"""

from __future__ import annotations

import streamlit as st

from src.dashboard.components.charts import (
    render_genre_ratings,
    render_popular_movies,
    render_top_rated_movies,
    render_user_preferences,
)
from src.dashboard.services.recommendation_service import (
    RecommendationService,
)


def render(
    service: RecommendationService,
) -> None:
    """
    Render the analytics page.
    """

    st.title("📊 Analytics")

    st.markdown(
        """
        Explore insights generated from the Gold layer.
        """
    )

    movie_metrics = service.get_movie_metrics()

    genre_metrics = service.get_genre_metrics()

    user_preferences = service.get_user_preferences()

    render_top_rated_movies(movie_metrics)

    st.divider()

    render_popular_movies(movie_metrics)

    st.divider()

    render_genre_ratings(genre_metrics)

    st.divider()

    render_user_preferences(user_preferences)
