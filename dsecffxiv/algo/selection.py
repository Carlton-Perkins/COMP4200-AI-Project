"""Methods for selection in a GA."""

from random import randint
from typing import Any

from dsecffxiv.algo.types import Individual, Population

Selection = Any
# Selection = Callable[[Individual, Dict], Individual]


def selection_tournament(_population: Population, tournament_size: int) -> Individual:
    """Tournament select an individual from the population."""
    size = len(_population)-1
    tournament_leader = size

    # Cheeky optimization here, assuming the population is already sorted, the best scoring indiv
    # will always be the smallest index
    for _ in range(tournament_size):
        # ? Should we allow duplicates in the selection pool?
        tournament_leader = min(tournament_leader, randint(0, size))

    return _population[tournament_leader]


Default_Selection = selection_tournament
