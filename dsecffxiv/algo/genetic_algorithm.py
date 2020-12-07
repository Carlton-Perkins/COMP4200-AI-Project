"""Interface and implimentations for a Genetic Algorithm."""


from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Tuple, Union

from dsecffxiv.algo.crossover import Crossover, Default_Crossover
from dsecffxiv.algo.generation import generate_new_population
from dsecffxiv.algo.mutation import Default_Mutation, Mutation
from dsecffxiv.algo.score import Default_Score, Score
from dsecffxiv.algo.selection import Default_Selection, Selection
from dsecffxiv.algo.types.individual import Individual
from dsecffxiv.algo.types.population import Population
from dsecffxiv.sim_resources.TestResources import generate_material_conditions, generate_success_values


class GeneticAlgorithm():
    """Basic Genetic Algorithm."""

    def __init__(self, config: Dict):
        """Initialize with a config."""
        self.config: Dict = config

        self.selection_func: Selection = Default_Selection
        self.mutation_func: Mutation = Default_Mutation
        self.crossover_func: Crossover = Default_Crossover
        self.score_func: Score = Default_Score

        self.material_conditions = generate_material_conditions(config['population_size'])
        self.success_rolls = generate_success_values(config['population_size'])

        self.population: Union[Population, None] = None

    def step(self):
        """Perform one generation of the GA."""
        # Init population
        if self.population is None:
            self.population = generate_new_population(
                self.config['population_size'],
                self.config['domain'],
                self.config['individual_size'],
                self.material_conditions,
                self.success_rolls)

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
        if self.config['replace_pop']:
            self.population = children
        else:
            self.population = self.population + children


class ThreadedGeneticAlgorithm(GeneticAlgorithm):
    """Basic Genetic Algorithm."""

    def __init__(self, config: Dict):
        """Initialize with a config."""
        super().__init__(config)

        self.thread_pool = ThreadPoolExecutor(64)

    def step(self):
        """Perform one generation of the GA."""
        # Init population
        if self.population is None:
            self.population = generate_new_population(
                self.config['population_size'],
                self.config['domain'],
                self.config['individual_size'],
                self.material_conditions,
                self.success_rolls)

            # Score init population
            self.population.sort(key=self.score_func, reverse=True)

        def do_selection_crossover_mutate() -> Tuple[Individual, Individual]:
            left = self.selection_func(
                self.population, self.config['tournament_size'])
            right = self.selection_func(
                self.population, self.config['tournament_size'])

            new_left, new_right = self.crossover_func((left, right), 2)

            self.mutation_func(
                new_left, self.config['mutation_chance'], self.config['domain'])
            self.mutation_func(
                new_right, self.config['mutation_chance'], self.config['domain'])

            return (new_left, new_right)

        # Selection
        children = list()
        # for _ in range(self.config['selection_size']):
        futures = {self.thread_pool.submit(
            do_selection_crossover_mutate): i for i in range(self.config['selection_size'])}

        for future in futures:
            new_left, new_right = future.result()
            children.append(new_left)
            children.append(new_right)
        if self.config['replace_pop']:
            self.population = children
        else:
            self.population = self.population + children

        # Score population
        self.population.sort(key=self.score_func, reverse=True)

        # Cull population down to size
        self.population = self.population[slice(
            0, self.config['population_size'])]
