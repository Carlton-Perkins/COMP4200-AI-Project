"""Methods for mutation operations in a GA."""
from typing import Any

from dsecffxiv.algo.generation import new_value_from_domain
from dsecffxiv.algo.types import Domain, Individual
from dsecffxiv.utils.chance import chance

Mutation = Any
# Mutation = Callable[[Individual, Dict], Individual]


def mutate_each(_indiv: Individual, percent_chance: float, domain: Domain):
    """Iterate over all values in the indiv and possibly mutate them."""
    for i in range(len(_indiv.value)):
        if chance(percent_chance):
            _indiv.value[i] = new_value_from_domain(domain)


Default_Mutation = mutate_each
