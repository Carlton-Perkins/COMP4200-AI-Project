"""Scoring utilities."""

from typing import Any

from dsecffxiv.algo.types import Individual

Score = Any
# Score = Callable[[Individual], int]


def score_individual(indiv: Individual) -> int:
    """Score a given individual."""
    max_score = 0
    # Select start values
    for each_start in range(0, len(indiv.value) - 1):
        score = 0
        for each in range(each_start, len(indiv.value) - 1):
            if indiv.value[each] + 1 == indiv.value[each+1]:
                score = score + 1
            else:
                break
        if score > max_score:
            max_score = score
    return max_score


Default_Score = score_individual
