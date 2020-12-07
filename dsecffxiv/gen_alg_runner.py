"""Runnable shell to facilitate the genetic algorithm."""

# import gc
import sys
from time import time_ns
from typing import Any, Dict, List

import cmd2
from cmd2.decorators import with_argument_list
from tqdm import tqdm

from dsecffxiv.algo.genetic_algorithm import (GeneticAlgorithm,
                                              ThreadedGeneticAlgorithm)
from dsecffxiv.algo.stats import print_leaderboard, show_p_stats, show_stats
from dsecffxiv.algo.types.population import Population


class GenAlgShell(cmd2.Cmd):
    """A REPL CLI for a genetic algorithm."""

    def __init__(self):
        """Construct a CLI."""
        super().__init__()

        # Remove the builtin configs
        self.remove_settable('allow_style')
        self.remove_settable('always_show_hint')
        # self.remove_settable('debug')
        self.remove_settable('echo')
        self.remove_settable('editor')
        self.remove_settable('feedback_to_output')
        self.remove_settable('quiet')
        self.remove_settable('timing')
        self.remove_settable('max_completion_items')

        # GenAlg Config
        self.population_size = 500
        self.generation_limit = 1000
        self.individual_size = 50
        self.selection_size = 100
        self.tournament_size = 50
        self.mutation_chance = 0.01
        self.auto_domain = True
        self.replace_pop = False

        self.add_settable(cmd2.Settable('population_size', int,
                                        'Number of individuals in the population', onchange_cb=self.bind_config))
        self.add_settable(cmd2.Settable('generation_limit',
                                        int, 'Hard generation limit for simulations', onchange_cb=self.bind_config))
        self.add_settable(cmd2.Settable('individual_size', int,
                                        'The length the individuals list of actions should be', onchange_cb=self.bind_config))
        self.add_settable(cmd2.Settable('selection_size', int,
                                        'How many pairs should be generated during selection', onchange_cb=self.bind_config))
        self.add_settable(cmd2.Settable('tournament_size', int,
                                        'How many individuals should be considered in a tournament selection', onchange_cb=self.bind_config))
        self.add_settable(cmd2.Settable('mutation_chance',
                                        float, 'How likely a mutation should be', onchange_cb=self.bind_config))
        self.add_settable(cmd2.Settable('auto_domain',
                                        float, 'Should we use the size to generate the domain', onchange_cb=self.bind_config))
        self.add_settable(cmd2.Settable('replace_pop',
                                        float, 'Should we replace the current population all with children', onchange_cb=self.bind_config))

        self.genetic_algorithm: GeneticAlgorithm = None
        self.population_history: List[Population] = list()
        self.profile_times: List[Any] = list()

    def assemble_config(self) -> Dict:
        """Construct a config dict from the member values."""
        config = dict()
        config['population_size'] = self.population_size
        config['generation_limit'] = self.generation_limit
        config['individual_size'] = self.individual_size
        config['selection_size'] = self.selection_size
        config['tournament_size'] = self.tournament_size
        config['mutation_chance'] = self.mutation_chance
        config['replace_pop'] = self.replace_pop
        config['domain'] = list(
            range(1, self.individual_size + 1)) if self.auto_domain else None  # make domain more generic

        return config

    def bind_config(self, _name, _old, _new):
        """Pass through our config down to the GA."""
        if self.genetic_algorithm is None:
            self.genetic_algorithm = ThreadedGeneticAlgorithm(
                self.assemble_config())
        else:
            self.genetic_algorithm.config = self.assemble_config()

    def do_run(self, args):
        """Run algorithm until converge."""

    def do_stats(self, _args):
        """Print the stats for the current run."""
        show_stats(self.population_history, self.genetic_algorithm.score_func)

    def do_pstats(self, _args):
        """Profile stats."""
        show_p_stats(self.profile_times)

    # def do_gc(self, _opts):
    #     """Manually run garbage collection."""
    #     print("GC: ", gc.isenabled())
    #     gc.collect(0)

    def do_reset(self, _args):
        """Reset the current run."""
        self.genetic_algorithm = None
        self.population_history = list()

    @with_argument_list
    def do_leaderboard(self, args):
        """Print the leaderboard for scores."""
        length = args[0] if len(args) == 1 else 5

        print_leaderboard(self.genetic_algorithm.population,
                          self.genetic_algorithm.score_func, length)

    @with_argument_list
    def do_step(self, args):
        """Run one or number generations of the algorithm."""
        # Argument validation, default to 1
        if len(args) == 1:
            steps = int(args[0])
        else:
            steps = 1

        # Init GeneticAlgorithm if not already
        if self.genetic_algorithm is None:
            self.genetic_algorithm = ThreadedGeneticAlgorithm(
                self.assemble_config())

        # Run n steps
        for _ in tqdm(range(steps), desc='Simulating', unit='Generations'):
            start_time = time_ns()
            self.genetic_algorithm.step()
            end_time = time_ns()
            self.population_history.append(self.genetic_algorithm.population)
            self.profile_times.append(end_time - start_time)


if __name__ == "__main__":
    cli = GenAlgShell()
    sys.exit(cli.cmdloop())
