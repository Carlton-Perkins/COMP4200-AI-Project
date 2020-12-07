"""Utility methods for creating new populations."""

from random import randint

from dsecffxiv.algo.types import Domain, Individual, Population
from dsecffxiv.sim_resources import TestResources, ActionClasses


def generate_new_individual(domain: Domain, size: int, material_conditions) -> Individual:
    """Generate a random new Individual of the give size and domain."""
    indiv = list()  # List of action from domain
    # Have to put Waste Not buff handling here, since there's no way to get a state
    waste_not = 0
    for i in range(0, size):
        random_action = TestResources.get_random_action(i, material_conditions[i], waste_not)
        if random_action is ActionClasses.WasteNot:  # Track turns to avoid using Prudent Touch while it is invalid
            waste_not = 5  # Extra turn because of decrement
        elif random_action is ActionClasses.WasteNot2:
            waste_not = 9
        indiv.append(random_action)
        if waste_not > 0:
            waste_not -= 1
    return Individual(indiv)


def generate_new_population(population_size: int, domain: Domain, size: int) -> Population:
    """Generate a new population give a population size, domain, and individual size."""
    new_population = list()
    material_conditions = TestResources.generate_material_conditions(size)
    success_values = TestResources.generate_success_values(size)
    for _ in range(0, population_size):
        new_population.append(
            generate_new_individual(domain, size, material_conditions))
    return new_population


def new_value_from_domain(domain: Domain):
    """Generate a new key value randomly from the domain."""
    return domain[randint(0, len(domain)-1)]
