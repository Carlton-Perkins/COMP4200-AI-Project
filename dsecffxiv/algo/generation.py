"""Utility methods for creating new populations."""

from random import randint

from dsecffxiv.algo.types import Domain, Individual, Population


def generate_new_individual(domain: Domain, size: int) -> Individual:
    """Generate a random new Individual of the give size and domain."""
    indiv = list()  # List of action from domain
    for _ in range(0, size):
        indiv.append(new_value_from_domain(domain))
    return Individual(indiv)


def generate_new_population(population_size: int, domain: Domain, size: int) -> Population:
    """Generate a new population give a population size, domain, and individual size."""
    new_population = list()
    for _ in range(0, population_size):
        new_population.append(
            generate_new_individual(domain, size))
    return new_population


def new_value_from_domain(domain: Domain):
    """Generate a new key value randomly from the domain."""
    return domain[randint(0, len(domain)-1)]
