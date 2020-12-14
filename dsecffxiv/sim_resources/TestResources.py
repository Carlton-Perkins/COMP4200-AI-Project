import random
import dsecffxiv.sim_resources.ActionClasses as action


# Contains support functions for generating test environment and handling action selection.

# Arrays containing actions, organized by availability based on state and sorted by CP cost in each array
first_step_actions = [action.MuscleMemory, action.Reflect]
good_condition_actions = [action.TricksoftheTrade, action.RapidSynthesis, action.HastyTouch, action.BasicSynthesis,
                          action.FocusedSynthesis, action.IntensiveSynthesis, action.PatientTouch,
                          action.BrandoftheElements, action.CarefulSynthesis, action.Observe, action.Veneration,
                          action.Innovation, action.BasicTouch, action.PreciseTouch, action.FocusedTouch,
                          action.InnerQuiet, action.Groundwork, action.ByregotsBlessing, action.PrudentTouch,
                          action.NameoftheElements, action.DelicateSynthesis, action.StandardTouch, action.GreatStrides,
                          action.PreparatoryTouch, action.WasteNot, action.MastersMend, action.Manipulation,
                          action.WasteNot2, action.FinalAppraisal]
actions = [action.RapidSynthesis, action.HastyTouch, action.BasicSynthesis, action.FocusedSynthesis,
           action.PatientTouch, action.BrandoftheElements, action.CarefulSynthesis, action.Observe, action.Veneration,
           action.Innovation, action.BasicTouch, action.FocusedTouch, action.InnerQuiet, action.Groundwork,
           action.ByregotsBlessing, action.PrudentTouch, action.NameoftheElements, action.DelicateSynthesis,
           action.StandardTouch, action.GreatStrides, action.PreparatoryTouch, action.WasteNot, action.MastersMend,
           action.Manipulation, action.WasteNot2, action.FinalAppraisal]
low_durability_actions = [action.MastersMend, action.Manipulation]
observe_actions = [action.FocusedSynthesis, action.FocusedTouch]


def generate_material_conditions(sequence_length):
    # Probabilities sourced from:
    # https://docs.google.com/document/d/1Da48dDVPB7N4ignxGeo0UeJ_6R0kQRqzLUH-TkpSQRc/edit
    conditions = [0]  # First state is always normal
    for i in range(1, sequence_length):
        rand_val = random.randint(0, 99)
        if 0 <= rand_val <= 11:
            conditions.append(1)  # Good
        elif 12 <= rand_val <= 26:
            conditions.append(3)  # Centered
        elif 27 <= rand_val <= 38:
            conditions.append(2)  # Pliant
        elif 39 <= rand_val <= 53:
            conditions.append(4)  # Sturdy
        else:
            conditions.append(0)  # Normal
    return conditions


def generate_success_values(sequence_length):
    # Generates success chance values that are used to determine the success or failure of certain actions.
    values = []
    for i in range(0, sequence_length):
        values.append(random.randint(0, 99))
    return values


def get_random_action(step_number, material_condition, waste_not, inner_quiet, name_elements, veneration, great_strides,
                      innovation, manipulation, cp, durability):
    # Gets a random valid action based on the state.
    # Basically all heuristics are handled here.
    if step_number == 0:  # Opening actions should always be used and can only be used now
        return first_step_actions[random.randint(0, 1)]
    elif material_condition == "good":  # Good condition has exclusive actions
        i = random.randrange(0, len(good_condition_actions))
        # Prudent Touch cannot be used while Waste Not buff is active. Inner Quiet cannot be used while user has stacks.
        # Other buffs should not be used while they are already up.
        while (waste_not > 0 and i == good_condition_actions.index(action.PrudentTouch)) or \
                (inner_quiet and i == good_condition_actions.index(action.InnerQuiet)) or \
                (name_elements > 0 and i == good_condition_actions.index(action.NameoftheElements)) or \
                (veneration > 0 and i == good_condition_actions.index(action.Veneration)) or \
                (great_strides > 0 and i == good_condition_actions.index(action.GreatStrides)) or \
                (innovation > 0 and i == good_condition_actions.index(action.Innovation)) or \
                (manipulation > 0 and i == good_condition_actions.index(action.Manipulation)):
            i = random.randrange(0, len(good_condition_actions))
        return good_condition_actions[random.randrange(0, len(good_condition_actions))]
    i = random.randrange(0, len(actions))
    # Prudent Touch cannot be used while Waste Not buff is active. Inner Quiet cannot be used while user has stacks.
    # Other buffs should not be used while they are already up.
    while (waste_not > 0 and i == actions.index(action.PrudentTouch)) or \
            (inner_quiet and i == actions.index(action.InnerQuiet)) or \
            (name_elements > 0 and i == actions.index(action.NameoftheElements)) or \
            (veneration > 0 and i == actions.index(action.Veneration)) or \
            (great_strides > 0 and i == actions.index(action.GreatStrides)) or \
            (innovation > 0 and i == actions.index(action.Innovation)) or \
            (manipulation > 0 and i == actions.index(action.Manipulation)):
        i = random.randrange(0, len(actions))
    return actions[random.randrange(0, len(actions))]
