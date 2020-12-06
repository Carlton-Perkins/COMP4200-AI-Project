"""Runable shell to faclitate the genetic algorithm."""

# import gc
import sys
from typing import Dict

import cmd2
from cmd2.decorators import with_argument_list
from tqdm import tqdm

from dsecffxiv.algo.genetic_algorithm import GeneticAlgorithm
from dsecffxiv.algo.stats import print_leaderboard


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

        self.genetic_algorithm: GeneticAlgorithm = None

    def assemble_config(self) -> Dict:
        """Construct a config dict from the member values."""
        config = dict()
        config['population_size'] = self.population_size
        config['generation_limit'] = self.generation_limit
        config['individual_size'] = self.individual_size
        config['selection_size'] = self.selection_size
        config['tournament_size'] = self.tournament_size
        config['mutation_chance'] = self.mutation_chance
        config['domain'] = list(
            range(1, self.individual_size + 1)) if self.auto_domain else None  # make domain more generic

        return config

    def bind_config(self, _name, _old, _new):
        """Pass through our config down to the GA."""
        if self.genetic_algorithm is None:
            self.genetic_algorithm = GeneticAlgorithm(self.assemble_config())
        else:
            self.genetic_algorithm.config = self.assemble_config()

    @with_argument_list
    def do_step(self, arglist):
        """Run one or number generations of the algorithm."""
        # Argument validation, default to 1
        if len(arglist) == 1:
            steps = int(arglist[0])
        else:
            steps = 1

        # Init GeneticAlgorithm if not already
        if self.genetic_algorithm is None:
            self.genetic_algorithm = GeneticAlgorithm(self.assemble_config())

        # Run n steps
        for _ in tqdm(range(steps)):
            self.genetic_algorithm.step()

    def do_run(self):
        """Run algorithm until converge."""

    @with_argument_list
    def do_leaderboard(self, arglist):
        """Print the leaderboard for scores."""
        length = arglist[0] if len(arglist) == 1 else 5

        print_leaderboard(self.genetic_algorithm.population,
                          self.genetic_algorithm.score_func, length)

    def do_stats(self):
        """Print the stats for the current run."""

    # def do_gc(self, _opts):
    #     """Manually run garbage collection."""
    #     print("GC: ", gc.isenabled())
    #     gc.collect(0)


if __name__ == "__main__":
    cli = GenAlgShell()
    sys.exit(cli.cmdloop())
