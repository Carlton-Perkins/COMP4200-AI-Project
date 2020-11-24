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


from itertools import islice
from random import randint, uniform
from typing import Any, List, Tuple

import matplotlib.pyplot as plt
from tqdm import tqdm

from dsecffxiv.algo.individual import Individual
from dsecffxiv.algo.population import Population


def generate_new_individual(domain: List[Any], size: int) -> Individual:
    indiv = list()  # List of action from domain
    for _ in range(0, size):
        indiv.append(new_value_from_domain(domain))
    return Individual(indiv)


def generate_new_population(population_size: int, domain: List[Any], size: int) -> Population:
    new_population = list()
    for _ in range(0, population_size):
        new_population.append(
            generate_new_individual(domain, size))
    return new_population


def new_value_from_domain(domain: List[Any]):
    return domain[randint(0, len(domain)-1)]


def mutate_individual(indiv: Individual, domain: List[Any]) -> None:
    mutate_position = randint(0, len(indiv.value)-1)
    indiv.value[mutate_position] = new_value_from_domain(domain)


def sort_population_by_score(population: Population) -> Population:
    population.sort(key=score_individual, reverse=True)
    return population


def select_individuals(population: Population, select_pairs: int) -> List[Tuple[Individual, Individual]]:
    iterator = iter(population)
    result_collection = list()
    for _ in range(0, select_pairs):
        select_slice = islice(iterator, 2)
        result_collection.append((next(select_slice), next(select_slice)))
    return result_collection


def crossover_individuals(selection: List[Tuple[Individual, Individual]]) -> Population:
    result_collection = list()
    for each in selection:
        new_left, new_right = crossover_individual_pairs(each[0], each[1])
        result_collection.append(new_left)
        result_collection.append(new_right)
    return result_collection


def crossover_individual_pairs(left: Individual, right: Individual) -> Tuple[Individual, Individual]:
    left_slice_point = (len(left.value)//2)
    left_first = left.value[slice(0, left_slice_point)]
    left_last = left.value[slice(left_slice_point, len(left.value))]

    right_slice_point = (len(right.value)//2)
    right_first = right.value[slice(0, right_slice_point)]
    right_last = right.value[slice(right_slice_point, len(right.value))]

    new_left = Individual(left_first + right_last)
    new_right = Individual(right_first + left_last)
    return (new_left, new_right)


def score_individual(indiv: Individual) -> int:
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


def print_individual_score_mapping(population: Population) -> None:
    for each in population:
        print("{0} -> {1}".format(str(each), score_individual(each)))


def cull_population(population: Population, size: int):
    population = population[slice(0, size)]
    return population


if __name__ == "__main__":
    POPULATION_SIZE = 500
    GENERATION_LIMIT = 100000
    SIZE = 100
    DOMAIN = list(range(1, SIZE+1))
    SELECTION_PAIR_SIZE = 50
    MUTATION_CHANCE = 0.35

    # Generation initial population
    population = generate_new_population(POPULATION_SIZE, DOMAIN, SIZE)

    # Historical Stats
    population_history = list()

    # print_individual_score_mapping(population)

    try:
        for generation in tqdm(range(0, GENERATION_LIMIT + 1), unit='Generation', desc='Simulating'):
            sorted_population = sort_population_by_score(population)
            culled_population = cull_population(
                sorted_population, POPULATION_SIZE)

            population_history.append(culled_population)

            selected_population = select_individuals(
                culled_population, SELECTION_PAIR_SIZE)
            # for each in selected_population:
            #     print("Selected: {0} {1}".format(str(each[0]), str(each[1])))
            # print("GEN: {0}".format(generation))
            # print_individual_score_mapping(sorted_population[slice(0, 5)])
            crossed_over_population = crossover_individuals(
                selected_population)
            # for each in crossed_over_population:
            # print("Crossover: {0}".format(str(each)))

            for each_indiv in crossed_over_population:
                if uniform(0, 1) < MUTATION_CHANCE:
                    # print("Mutated: {0}".format(str(each)))
                    mutate_individual(each_indiv, DOMAIN)
                    # print("Mutated Into: {0}".format(str(each)))

            population = culled_population + crossed_over_population
    except KeyboardInterrupt:
        pass

    stat_min = list()
    stat_max = list()

    for generation_pop in tqdm(population_history, desc='Generating Stats'):
        stat_min.append(score_individual(generation_pop[-1]))
        stat_max.append(score_individual(generation_pop[0]))

    stat_generation_max = list(range(0, len(stat_max)))
    stat_generation_min = list(range(0, len(stat_min)))

    plt.plot(stat_generation_max, stat_max)
    plt.plot(stat_generation_min, stat_min)
    plt.show()
    # for each in crossed_over_population:
    #     print("Crossover: {0}".format(str(each)))
