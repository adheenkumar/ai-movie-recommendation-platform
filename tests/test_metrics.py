"""
Tests for Gold business metrics.
"""

from src.gold.metrics import weighted_rating


def test_weighted_rating_many_votes() -> None:
    """Movie with many votes should stay close to its rating."""

    result = weighted_rating(
        average_rating=4.8,
        vote_count=1000,
        global_average=3.8,
        minimum_votes=50,
    )

    assert round(result, 2) == 4.75


def test_weighted_rating_few_votes() -> None:
    """Movie with few votes should move toward the global average."""

    result = weighted_rating(
        average_rating=5.0,
        vote_count=2,
        global_average=3.8,
        minimum_votes=50,
    )

    assert round(result, 2) == 3.85


def test_zero_votes_returns_global_average() -> None:
    """Zero votes should return the global average."""

    result = weighted_rating(
        average_rating=5.0,
        vote_count=0,
        global_average=3.8,
    )

    assert result == 3.8
