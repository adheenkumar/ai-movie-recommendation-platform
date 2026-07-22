"""
Business metrics used in the Gold layer.
"""

from __future__ import annotations


def weighted_rating(
    average_rating: float,
    vote_count: int,
    global_average: float,
    minimum_votes: int = 50,
) -> float:
    """
    Compute IMDb-style weighted rating.

    Args:
        average_rating:
            Average movie rating.

        vote_count:
            Number of ratings.

        global_average:
            Global average rating across all movies.

        minimum_votes:
            Minimum vote threshold.

    Returns:
        Weighted rating.
    """

    if vote_count <= 0:
        return global_average

    return (vote_count / (vote_count + minimum_votes)) * average_rating + (
        minimum_votes / (vote_count + minimum_votes)
    ) * global_average
