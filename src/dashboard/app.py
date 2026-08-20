"""
Main entry point for the Streamlit dashboard.
"""

from __future__ import annotations

import streamlit as st

from src.dashboard.components.sidebar import render as render_sidebar
from src.dashboard.views import (
    analytics,
    home,
    recommendations,
)
from src.dashboard.services.recommendation_service import (
    RecommendationService,
)
from src.spark_jobs.spark_session import create_spark_session
from src.utils.logger import get_logger

logger = get_logger(__name__)

@st.cache_resource
def get_recommendation_service() -> RecommendationService:

    logger.info(
        "Initializing recommendation service."
    )

    if "startup_complete" not in st.session_state:

        with st.status(
                "🚀 Starting AI Movie Recommendation Platform...",
                expanded=True,
        ) as status:

            try:
                status.write("⚡ Creating Spark Session...")

                spark = create_spark_session(
                    app_name="Movie Recommendation Dashboard",
                )

                status.write("📦 Loading Dashboard Services...")

                service = RecommendationService(
                    spark=spark,
                    progress_callback=status.write,
                )

                status.update(
                    label="✅ Platform Ready!",
                    state="complete",
                    expanded=False,
                )

                st.session_state.startup_complete = True

                return service

            except Exception:

                logger.exception(
                    "Dashboard initialization failed."
                )

                status.update(
                    label="❌ Startup Failed",
                    state="error",
                )

                raise

def main() -> None:
    """
    Run the Streamlit dashboard.
    """

    logger.info(
        "Starting Streamlit dashboard."
    )

    st.set_page_config(
        page_title="AI Movie Recommendation Platform",
        page_icon="🎬",
        layout="wide",
    )

    service = get_recommendation_service()

    page = render_sidebar()

    if page == "home":
        home.render()

    elif page == "recommendations":
        recommendations.render(service)

    elif page == "analytics":
        analytics.render(service)


if __name__ == "__main__":
    main()
