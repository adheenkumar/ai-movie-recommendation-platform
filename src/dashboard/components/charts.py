"""
Charts component for the analytics dashboard.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def render_top_rated_movies(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render the highest rated movies.
    """

    st.subheader("⭐ Top Rated Movies")

    top_movies = (
        dataframe
        .sort_values(
            by="weighted_rating",
            ascending=False,
        )
        .head(10)
    )

    st.dataframe(
        top_movies[
            [
                "title",
                "weighted_rating",
                "average_rating",
                "rating_count",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

def render_genre_ratings(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render average rating by genre.
    """

    st.subheader("🎭 Average Rating by Genre")

    figure, axis = plt.subplots(
        figsize=(10, 5),
    )

    dataframe = dataframe.sort_values(
        by="average_rating",
        ascending=False,
    )

    axis.bar(
        dataframe["genre"],
        dataframe["average_rating"],
    )

    axis.set_ylabel("Average Rating")
    axis.tick_params(
        axis="x",
        rotation=45,
    )

    st.pyplot(figure)

def render_popular_movies(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render the most popular movies.
    """

    st.subheader("🔥 Most Popular Movies")

    top_movies = (
        dataframe
        .sort_values(
            by="rating_count",
            ascending=False,
        )
        .head(10)
    )

    st.dataframe(
        top_movies[
            [
                "title",
                "rating_count",
                "average_rating",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

def render_user_preferences(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render user preference statistics.
    """

    st.subheader("👤 User Preference Summary")

    st.metric(
        "Users",
        len(dataframe),
    )