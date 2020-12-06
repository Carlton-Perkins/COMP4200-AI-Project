"""Crossover Functions."""

from random import randint
from typing import Any, Tuple

from dsecffxiv.algo.types import Individual

Crossover = Any
# Crossover = Callable[[
#     Tuple[Individual, Individual], Dict], Tuple[Individual, Individual]]


def crossover_n_point(parents: Tuple[Individual, Individual], crossover_points: int) -> Tuple[Individual, Individual]:
    """Splice together two parents to make two children using n point crossover."""
    _left, _right = parents
    size = len(_left.value)
    points = list()
    for _ in range(crossover_points):
        new_point = randint(0, size)
        while new_point in points:
            new_point = randint(0, size)
        points.append(new_point)
    points.sort()

    _new_left, _new_right = list(), list()
    pick_direction = False

    for i in range(size):
        if i in points:
            pick_direction = not pick_direction

        if pick_direction:
            _new_left.append(_left.value[i])
            _new_right.append(_right.value[i])
        else:
            _new_left.append(_right.value[i])
            _new_right.append(_left.value[i])

    return (Individual(_new_left), Individual(_new_right))


Default_Crossover = crossover_n_point
