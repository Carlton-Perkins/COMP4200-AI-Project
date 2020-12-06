"""
Population.

    Where population is a list of Individuals.
"""

from typing import List

from dsecffxiv.algo.types import Individual

Population = List[Individual]


def cull_population(input_population: Population, size: int):
    """Slice the population down to a given size."""
    new_population = input_population[slice(0, size)]
    return new_population
