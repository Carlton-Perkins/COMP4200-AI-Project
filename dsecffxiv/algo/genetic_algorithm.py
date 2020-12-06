"""Interface and implimentations for a Genetic Algorithm."""


from typing import Dict, Union

from dsecffxiv.algo.crossover import Crossover, Default_Crossover
from dsecffxiv.algo.generation import generate_new_population
from dsecffxiv.algo.mutation import Default_Mutation, Mutation
from dsecffxiv.algo.score import Default_Score, Score
from dsecffxiv.algo.selection import Default_Selection, Selection
from dsecffxiv.algo.types.population import Population


class GeneticAlgorithm():
    """Basic Genetic Algorithm."""

    def __init__(self, config: Dict):
        """Initialize with a config."""
        self.config: Dict = config

        self.selection_func: Selection = Default_Selection
        self.mutation_func: Mutation = Default_Mutation
        self.crossover_func: Crossover = Default_Crossover
        self.score_func: Score = Default_Score

        self.population: Union[Population, None] = None

    def step(self):
        """Preform one generation of the GA."""
        # Init population
        if self.population is None:
            self.population = generate_new_population(
                self.config['population_size'],
                self.config['domain'],
                self.config['individual_size'])

        # Score population
        self.population.sort(key=self.score_func, reverse=True)

        # Cull population down to size
        self.population = self.population[slice(
            0, self.config['population_size'])]

        # Selection
        children = list()
        for _ in range(self.config['selection_size']):
            left = self.selection_func(
                self.population, self.config['tournament_size'])
            right = self.selection_func(
                self.population, self.config['tournament_size'])

            new_left, new_right = self.crossover_func((left, right), 2)

            self.mutation_func(
                new_left, self.config['mutation_chance'], self.config['domain'])
            self.mutation_func(
                new_right, self.config['mutation_chance'], self.config['domain'])

            children.append(new_left)
            children.append(new_right)
        self.population = self.population + children
