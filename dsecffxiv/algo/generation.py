"""Utility methods for creating new populations."""

from random import randint
from math import ceil

from dsecffxiv.algo.types import Domain, Individual, Population
from dsecffxiv.sim_resources import TestResources, ActionClasses


def generate_new_individual(domain: Domain, size: int, material_conditions, success_rolls) -> Individual:
    """Generate a random new Individual of the give size and domain."""
    indiv = list()  # List of action from domain
    # We get to manage heuristics based on buff/CP states in here, because we can't access actual states
    waste_not = 0
    inner_quiet = False
    name_elements = 0
    veneration = 0
    great_strides = 0
    innovation = 0
    manipulation = 0
    cp = 572
    durability = 50
    for i in range(0, size):
        random_action = TestResources.get_random_action(i, material_conditions[i], waste_not, inner_quiet,
                                                        name_elements, veneration, great_strides, innovation,
                                                        manipulation, cp, durability)
        if random_action is ActionClasses.WasteNot:  # Track turns to avoid using Prudent Touch while it is invalid
            waste_not = 5  # Extra turn because of decrement
        elif random_action is ActionClasses.WasteNot2:
            waste_not = 9  # Extra turn because of decrement
        elif (random_action is ActionClasses.Reflect) or (random_action is ActionClasses.InnerQuiet):
            inner_quiet = True  # Can't use Inner Quiet when you already have stacks (and shouldn't anyway)
        elif random_action is ActionClasses.ByregotsBlessing:
            inner_quiet = False  # Consumes Inner Quiet stacks
        elif random_action is ActionClasses.NameoftheElements:
            name_elements = 4  # Extra turn because of decrement
        elif random_action is ActionClasses.Veneration:
            veneration = 5  # Extra turn because of decrement
        elif random_action is ActionClasses.GreatStrides:
            great_strides = 4  # Extra turn because of decrement
        elif random_action is ActionClasses.Innovation:
            innovation = 5  # Extra turn because of decrement
        elif random_action is ActionClasses.Manipulation:
            manipulation = 6  # Extra turn because of decrement
        elif random_action is ActionClasses.MastersMend:
            durability += 30
            if durability > 50:
                durability = 50
        if material_conditions[i] == "pliant":
            cp -= ceil(random_action.CP_COST / 2)
        else:
            cp -= random_action.CP_COST
        if material_conditions[i] == "sturdy" and waste_not > 0:
            durability -= ceil(random_action.DURABILITY_COST / 4)
        elif material_conditions[i] == "sturdy" or waste_not > 0:
            durability -= ceil(random_action.DURABILITY_COST / 2)
        else:
            durability -= random_action.DURABILITY_COST
        # The only way to keep the sorting method is to bundle all of these into a tuple
        indiv.append((random_action, success_rolls[i], material_conditions[i]))
        if waste_not > 0:
            waste_not -= 1
        if name_elements > 0:
            name_elements -= 1
        if veneration > 0:
            veneration -= 1
        if great_strides > 0:
            great_strides -= 1
        if innovation > 0:
            innovation -= 1
        if manipulation > 0:
            manipulation -= 1
            durability += 5
            if durability > 50:
                durability = 50
    return Individual(indiv)


def generate_new_population(population_size: int, domain: Domain, size: int, material_conditions, success_rolls)\
        -> Population:
    """Generate a new population give a population size, domain, and individual size."""
    new_population = list()
    for _ in range(0, population_size):
        new_population.append(
            generate_new_individual(domain, size, material_conditions, success_rolls))
    return new_population


def new_value_from_domain(domain: Domain):
    """Generate a new key value randomly from the domain."""
    return domain[randint(0, len(domain)-1)]
