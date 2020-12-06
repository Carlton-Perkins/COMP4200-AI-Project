"""
Test program for the genetic algorithm.

Problem:
    Find the highest scoring list of numbers that is length SIZE, where your score is based on the
    longest increasing number chain.

    Score like the following:
    if SIZE = 5

    1 2 3 4 5 => Score 4
    1 2 3 5 4 => Score 2
    5 4 3 2 1 => Score 0
    5 4 1 2 3 => Score 2
    5 5 5 5 5 => Score 0

    The domain of each entry is 0..=SIZE.
"""

from tqdm import tqdm

from dsecffxiv.algo.crossover import crossover_n_point
from dsecffxiv.algo.generation import generate_new_population
from dsecffxiv.algo.mutation import mutate_each
from dsecffxiv.algo.score import score_individual
from dsecffxiv.algo.selection import selection_tournament
from dsecffxiv.algo.stats import show_stats
from dsecffxiv.algo.types import Domain, Population, cull_population


def sort_population_by_score(input_population: Population) -> None:
    """Sort the given population using the score, from highest to lowest."""
    input_population.sort(key=score_individual, reverse=True)


if __name__ == "__main__":
    POPULATION_SIZE = 500
    GENERATION_LIMIT = 1000
    SIZE = 50
    DOMAIN: Domain = list(range(1, SIZE+1))
    SELECTION_PAIR_SIZE = 100
    TOURNAMENT_SIZE = 50
    MUTATION_CHANCE = 0.01

    # Generation initial population
    population = generate_new_population(POPULATION_SIZE, DOMAIN, SIZE)

    # Historical Stats
    population_history = list()

    try:
        for generation in tqdm(range(0, GENERATION_LIMIT + 1), unit='Generation', desc='Simulating'):
            sort_population_by_score(population)
            population = cull_population(
                population, POPULATION_SIZE)

            population_history.append(population)

            children = list()
            for _ in range(SELECTION_PAIR_SIZE):
                left = selection_tournament(population, TOURNAMENT_SIZE)
                right = selection_tournament(population, TOURNAMENT_SIZE)

                new_left, new_right = crossover_n_point((left, right), 2)

                mutate_each(new_left, MUTATION_CHANCE, DOMAIN)
                mutate_each(new_right, MUTATION_CHANCE, DOMAIN)

                children.append(new_left)
                children.append(new_right)
            population = population + children
    except KeyboardInterrupt:
        pass

    # Show stats at the end of a run
    show_stats(population_history, score_individual)

    # for each in crossed_over_population:
    #     print("Crossover: {0}".format(str(each)))
