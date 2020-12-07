"""Utilities for producing statistics about a genetic run."""

from typing import Any, Callable, List

from matplotlib import pyplot as plt
from tqdm import tqdm

from dsecffxiv.algo.score import Score
from dsecffxiv.algo.types import Population
from dsecffxiv.algo.types.individual import Individual


def show_stats(input_population_history: List[Population], score_function: Callable[[Individual], int]) -> None:
    """Show some stats about the population to the user."""
    stat_min = list()
    stat_max = list()
    stat_avg = list()

    for generation_pop in tqdm(input_population_history, desc='Generating Stats'):
        stat_min.append(score_function(generation_pop[-1]))
        stat_max.append(score_function(generation_pop[0]))
        avg = 0.0
        for pop in generation_pop:
            avg += score_function(pop)
        avg /= len(generation_pop)
        stat_avg.append(avg)

    stat_generation_min = list(range(0, len(stat_min)))
    stat_generation_max = list(range(0, len(stat_max)))
    stat_generation_avg = list(range(0, len(stat_avg)))

    plt.plot(stat_generation_min, stat_min, label='Min Score')
    plt.plot(stat_generation_max, stat_max, label='Max Score')
    plt.plot(stat_generation_avg, stat_avg, label='Avg Score')

    plt.xlabel('Generation')
    plt.ylabel('Score')

    plt.title('Min/Max/Avg Score vs Generation')
    plt.legend()
    plt.show()


def print_individual_score_mapping(_population: Population, _scoring_function: Score) -> None:
    """Given a population, score and print the pop->Score mapping."""
    for each in _population:
        print("{0} -> {1}".format(str(each), _scoring_function(each)))


def print_leaderboard(_population: Population, _scoring_function: Score, size=5) -> None:
    """Print top n scoring individuals from the population."""
    print_individual_score_mapping(
        _population[slice(0, size)], _scoring_function)


def show_p_stats(times: List[Any]) -> None:
    """Generate and show performance stats."""
    size = list(range(0, len(times)))
    plt.plot(size, times, label='Time per generation')

    plt.legend()
    plt.show()
