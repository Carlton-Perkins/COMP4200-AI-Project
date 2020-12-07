"""Scoring utilities."""

from typing import Any

from dsecffxiv.algo.types import Individual
from dsecffxiv.sim_resources.State import State

Score = Any
# Score = Callable[[Individual], int]


def score_individual(indiv: Individual) -> int:
    """Score a given individual."""
    max_score = 0
    # Select start values
    for each_start in range(0, len(indiv.value) - 1):
        score = 0
        for each in range(each_start, len(indiv.value) - 1):
            if indiv.value[each] + 1 == indiv.value[each+1]:
                score = score + 1
            else:
                break
        if score > max_score:
            max_score = score
    return max_score


def score_craft(individual):
    craft_state = State()
    step_list = individual.value
    score = 0
    # DEBUG
    # print(step_list)
    for step in range(0, len(step_list)):
        try:
            craft_state.update_success(step_list[step][1])  # Get bundled success value
            craft_state.update_condition(step_list[step][2])  # Get bundled material value
            craft_state = step_list[step][0].execute(craft_state)
            craft_state.step()
            score = craft_state.evaluate()
            if score != 0:  # The craft broke, we ran out of CP, or we've completed the craft
                print("Craft Parameters:\n{}\nScore: {}\n".format(craft_state, score))
                return score
        except:
            print("Step: {}\n{}".format(step, step_list[step]))
    return score


Default_Score = score_craft
