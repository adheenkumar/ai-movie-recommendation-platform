"""
Charts component for the analytics dashboard.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


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
            by="weightedRating",
            ascending=False,
        )
        .head(10)
    )

    st.dataframe(
        top_movies[
            [
                "title",
                "weightedRating",
                "averageRating",
                "ratingCount",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "title": "Movie",
            "weightedRating": st.column_config.NumberColumn(
                "Weighted Rating",
                format="%.2f",
            ),
            "averageRating": st.column_config.NumberColumn(
                "Average Rating",
                format="%.2f",
            ),
            "ratingCount": "Ratings",
        },
    )


def render_genre_ratings(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render average rating by genre.
    """

    st.subheader("🎭 Average Rating by Genre")

    # Sort so highest-rated genre appears at the top.
    dataframe = dataframe.sort_values(
        by="averageRating",
        ascending=True,
    )

    figure, axis = plt.subplots(
        figsize=(10, 7),
    )

    axis.barh(
        dataframe["genreName"],
        dataframe["averageRating"],
        height=0.5,
    )

    axis.set_xlabel("Average Rating")
    axis.set_ylabel("Genre")

    # MovieLens ratings use a 0–5 scale.
    axis.set_xlim(0, 5)

    # Display rating value beside each bar.
    for index, rating in enumerate(
        dataframe["averageRating"]
    ):
        axis.text(
            rating + 0.03,
            index,
            f"{rating:.2f}",
            va="center",
        )

    figure.tight_layout()

    st.pyplot(
        figure,
        use_container_width=True,
    )

    plt.close(figure)

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
            by="ratingCount",
            ascending=False,
        )
        .head(10)
    )

    st.dataframe(
        top_movies[
            [
                "title",
                "ratingCount",
                "averageRating",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "title": "Movie",
            "ratingCount": "Ratings",
            "averageRating": st.column_config.NumberColumn(
                "Average Rating",
                format="%.2f",
            ),
        },
    )


def render_user_preferences(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render aggregated user preference statistics.
    """

    st.subheader("👤 User Preference Summary")

    if dataframe.empty:
        st.info("No user preference data available.")
        return

    # ---------------------------------------------------------
    # KPI calculations
    # ---------------------------------------------------------

    total_users = len(dataframe)

    average_movies_rated = dataframe["moviesRated"].mean()

    average_rating_given = dataframe["averageRatingGiven"].mean()

    most_active_user_row = dataframe.loc[
        dataframe["moviesRated"].idxmax()
    ]

    most_active_user = int(
        most_active_user_row["userId"]
    )

    most_active_user_ratings = int(
        most_active_user_row["moviesRated"]
    )

    favorite_genre = (
        dataframe["favoriteGenre"]
        .dropna()
        .value_counts()
        .idxmax()
    )

    # ---------------------------------------------------------
    # KPI cards
    # ---------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Users",
        f"{total_users:,}",
    )

    col2.metric(
        "🎬 Avg Movies Rated",
        f"{average_movies_rated:.1f}",
    )

    col3.metric(
        "⭐ Avg Rating Given",
        f"{average_rating_given:.2f}",
    )

    col4.metric(
        "🎭 Top Favorite Genre",
        favorite_genre,
    )

    # ---------------------------------------------------------
    # Additional insight
    # ---------------------------------------------------------

    st.caption(
        f"Most active user: User {most_active_user} "
        f"with {most_active_user_ratings:,} ratings."
    )
