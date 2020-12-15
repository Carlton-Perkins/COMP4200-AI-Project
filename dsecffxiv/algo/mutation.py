"""Methods for mutation operations in a GA."""
from typing import Any

from dsecffxiv.algo.generation import generate_new_individual
from dsecffxiv.algo.types import Domain, Individual
from dsecffxiv.utils.chance import chance
from dsecffxiv.sim_resources.TestResources import get_random_action

Mutation = Any
# Mutation = Callable[[Individual, Dict], Individual]


def mutate_each(_indiv: Individual, percent_chance: float, domain: Domain):
    """Iterate over all values in the indiv and possibly mutate them."""
    for i in range(len(_indiv.value)):
        if chance(percent_chance):
            success_roll = _indiv.value[i][1]
            material_condition = _indiv.value[i][2]
            random_action = get_random_action(i, material_condition, 0, False, 0, 0, 0, 0, 0, 570, 50)
            _indiv.value[i] = (random_action, success_roll, material_condition)


Default_Mutation = mutate_each
