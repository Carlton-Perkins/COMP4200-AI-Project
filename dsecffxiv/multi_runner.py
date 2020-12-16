"""Executable to run many GA's a the same time a report result."""

from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any, Callable, Dict, List

from matplotlib import pyplot as plt
from tqdm import tqdm

from dsecffxiv.algo.genetic_algorithm import ThreadedGeneticAlgorithm
from dsecffxiv.algo.score import Default_Score, score_individual
from dsecffxiv.algo.stats import show_stats
from dsecffxiv.algo.types import Individual
from dsecffxiv.algo.types.population import Population

GEN_LIMIT = 2500
JOB_COUNT = 500
WORKER_LIMIT = 32
MAX_SCORE_LEN_CAP = 50


def assemble_config() -> Dict:
    """Construct a config dict from the member values."""
    config: Dict[Any, Any] = dict()
    config['population_size'] = 500
    config['generation_limit'] = 1000
    config['individual_size'] = 50
    config['selection_size'] = 100
    config['tournament_size'] = 50
    config['mutation_chance'] = 0.01
    config['domain'] = list(range(1, 50 + 1))
    config['replace_pop'] = False

    return config


def do_stat_math(input_population_history: List[Population], score_function: Callable[[Individual], int] = Default_Score):
    """Show some stats about the population to the user."""
    stat_min = list()
    stat_max = list()
    stat_avg = list()
    max_pop = None

    for generation_pop in tqdm(input_population_history, desc='Generating Stats'):
        if max_pop is None:
            max_pop = generation_pop[0]
        else:
            max_pop = max(max_pop, generation_pop[0], key=score_function)

        stat_min.append(score_function(generation_pop[-1]))
        stat_max.append(score_function(generation_pop[0]))
        avg = 0.0
        for _pop in generation_pop:
            avg += score_function(_pop)
        avg /= len(generation_pop)
        stat_avg.append(avg)

    stat_generation_min = list(range(0, len(stat_min)))
    stat_generation_max = list(range(0, len(stat_max)))
    stat_generation_avg = list(range(0, len(stat_avg)))

    return ((stat_generation_min, stat_min), (stat_generation_max, stat_max), (stat_generation_avg, stat_avg), max_pop)


def do_run() -> List[Population]:
    """Do multithreaded run of GA."""
    ga = ThreadedGeneticAlgorithm(assemble_config())
    pop_history = list()
    max_score = 0
    max_score_len = 0
    for _ in range(GEN_LIMIT):
        ga.step()
        new_max_score = max(Default_Score(ga.population[0]), max_score)
        if new_max_score == max_score:
            max_score_len += 1
        else:
            max_score = new_max_score
            max_score_len = 0

        pop_history.append(ga.population)

        if max_score_len > MAX_SCORE_LEN_CAP:
            break
    return pop_history


if __name__ == '__main__':
    pop_history_collection = list()
    with ProcessPoolExecutor(WORKER_LIMIT) as tp:
        futures = {tp.submit(
            do_run): i for i in range(JOB_COUNT)}

        for future in tqdm(as_completed(futures)):
            pop = future.result()
            pop_history_collection.append(pop)

    with ProcessPoolExecutor(WORKER_LIMIT) as tp:
        res = tp.map(
            do_stat_math, pop_history_collection)
        max_pop = None
        for r in tqdm(res):
            (min_g, min_v), (max_g, max_v), (avg_g, avg_v), m_pop = r

            if max_pop is None:
                max_pop = m_pop
            else:
                max_pop = max(max_pop, m_pop, key=Default_Score)

            # plt.plot(min_g, min_v, '-', label='Min Score')
            plt.plot(max_g, max_v, '-.', label='Max Score')
            # plt.plot(avg_g, avg_v, ':', label='Avg Score')

    print("{0} => {1}".format(str(max_pop), Default_Score(max_pop)))

    plt.xlabel('Generation')
    plt.ylabel('Score')

    plt.title('Min/Max/Avg Score vs Generation')
    # plt.legend()
    plt.show()
