"""
Home page for the AI Movie Recommendation Platform.
"""

from __future__ import annotations

import streamlit as st


def render() -> None:
    """
    Render the home page.
    """

    st.title("🎬 AI Movie Recommendation Platform")

    st.markdown(
        """
        Welcome to the **AI Movie Recommendation Platform**.

        This project demonstrates an end-to-end recommendation system built
        using modern Data Engineering, Machine Learning, and Generative AI
        technologies.
        """
    )

    st.divider()

    st.subheader("Project Features")

    col1, col2 = st.columns(2)

    with col1:
        st.success("Hybrid Recommendation Engine")
        st.success("Semantic Search (FAISS)")
        st.success("Sentence Transformers")
        st.success("PySpark Data Pipeline")

    with col2:
        st.success("LLM Explanations (Ollama)")
        st.success("Bronze / Silver / Gold Architecture")
        st.success("Data Quality Validation")
        st.success("Interactive Dashboard")

    st.divider()

    st.subheader("Technology Stack")

    st.markdown(
        """
        - PySpark
        - Python
        - Streamlit
        - FAISS
        - Sentence Transformers
        - Ollama
        """
    )

    st.divider()

    st.info(
        "Use the sidebar to explore recommendations and analytics."
    )
