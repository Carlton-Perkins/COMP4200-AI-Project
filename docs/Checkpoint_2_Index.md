# Checkpoint 2 Index

## Relevant files in repository

### Shannon Conneilly: dsecffxiv/sim_resources directory

- State.py: Contains class representing the craft state.
Initializes variables to the values they would have at the start of a craft, as well as methods to update the state on each step. Includes evaluation function.
- ActionClasses.py: Contains class definitions for every crafting action. Every action inherits from a base Action class, which defines constants used in all calculations as well as the formulae for calculating increases in progress and quality. Each action implements the static method execute(state), which takes a state as an argument, updates it in the same way the action would, and returns the updated state. All of the methods are static so that we do not need to spin up instances of the classes just to update the state.
- TestResources.py: Crafting-specific helper functions to set up consistent individual environments across a population. Contains functions for generating sequences of material conditions and success rolls. Also contains functionality for choosing a random *valid* action.
(Note: contributed to generation.py and score.py in order to integrate state and state transition representations into genetic algorithm)

### Carlton Perkins: dsecffxiv/[algo/tests] directory

- gen_alg_runner.py: A resumable cli/REPL interface to monitor and run the genetic algorithm.
- multi_runner.py: A single-shot exe that will run a bunch of GA's with the given parameters in multiprocessing mode.
- algo/crossover.py: Interface / methods for crossing over individuals.
- algo/generation.py: Helper methods for generation of generations.
- algo/genetic_algorithm.py: Class interface for the complete genetic algorithm.
- algo/mutation.py: Helper methods for mutation of individuals.
- algo/score.py: Interface/Methods for scoring individuals.
- algo/selection.py: Methods for selecting individuals from a population. Includes Tournament and more.
- algo/stats.py: Helper methods for graphing, and profiling a populations history.
- algo/types/domain.py: Interface for a domain of individuals.
- algo/types/individual.py: Interface for individuals inside a population.
- algo/types/population.py: Interface/type alias for a container of individuals.
- tests/long_increasing_numbers.py: Toy problem to test the effectiveness of the genetic algorithm backend.
- utils/chance.py: Helpers for working with probability.
