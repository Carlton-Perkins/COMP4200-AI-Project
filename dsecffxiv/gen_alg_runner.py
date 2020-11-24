"""Runable shell to faclitate the genetic algorithm."""

import sys

import cmd2


class GenAlgShell(cmd2.Cmd):
    """A REPL CLI for a genetic algorithm."""

    def __init__(self):
        super().__init__()

    def do_step(self, number=1):
        """Run one or number generations of the algorithm."""

    def do_run(self):
        """Run algorithm until converge."""

    def do_leaderboard(self, count=5):
        """Print the leaderboard for scores."""

    def do_stats(self):
        """Print the stats for the current run."""


if __name__ == "__main__":
    cli = GenAlgShell()
    sys.exit(cli.cmdloop())
