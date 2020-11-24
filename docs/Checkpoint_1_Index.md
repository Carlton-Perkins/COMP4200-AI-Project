# Checkpoint 1 Index

## Relevant files in repository

### Shannon Conneilly: dsecffxiv/sim_resources directory

- State.py: Contains class representing the craft state.
Initializes variables to the values they would have at the start of a craft, as well as methods to update the state on each step.
- ActionClasses.py: Contains class definitions for every crafting action. Every action inherits from a base Action class, which defines constants used in all calculations as well as the formulae for calculating increases in progress and quality. Each action implements the static method execute(state), which takes a state as an argument, updates it in the same way the action would, and returns the updated state. All of the methods are static so that we do not need to spin up instances of the classes just to update the state.

### Carlton Perkins: dsecffxiv/[algo/tests] directory

- gen_alg_runner.py: A resumable cli/REPL interface to monitor and run the genetic algorithm.
- algo/individual.py: Interface for individuals inside a population
- algo/population.py: Interface/type alias for a container of individuals
- tests/long_increasing_numbers.py: Toy problem to test the effectiveness of the genetic algorithm backend
- algo/genalg.py.disabled: Deprecated first pass on the GA implementation
