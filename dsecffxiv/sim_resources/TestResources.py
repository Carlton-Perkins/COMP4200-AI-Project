import random
import dsecffxiv.sim_resources.ActionClasses as action


# Contains support functions for generating test environment and handling action selection.

# Arrays containing actions, organized by availability based on state
first_step_actions = [action.MuscleMemory, action.Reflect]
good_condition_actions = [action.BasicSynthesis, action.RapidSynthesis, action.CarefulSynthesis, action.Groundwork,
                          action.IntensiveSynthesis, action.BrandoftheElements, action.NameoftheElements,
                          action.Veneration, action.FinalAppraisal, action.DelicateSynthesis, action.BasicTouch,
                          action.HastyTouch, action.StandardTouch, action.PreparatoryTouch, action.PreciseTouch,
                          action.PatientTouch, action.PrudentTouch, action.ByregotsBlessing, action.GreatStrides,
                          action.Innovation, action.InnerQuiet, action.Observe, action.FocusedSynthesis,
                          action.FocusedTouch, action.TricksoftheTrade, action.WasteNot, action.WasteNot2,
                          action.MastersMend, action.Manipulation]
actions = [action.BasicSynthesis, action.RapidSynthesis, action.CarefulSynthesis, action.Groundwork,
           action.BrandoftheElements, action.NameoftheElements, action.Veneration, action.FinalAppraisal,
           action.DelicateSynthesis, action.BasicTouch, action.HastyTouch, action.StandardTouch,
           action.PreparatoryTouch, action.PatientTouch, action.PrudentTouch, action.ByregotsBlessing,
           action.GreatStrides, action.Innovation, action.InnerQuiet, action.Observe, action.FocusedSynthesis,
           action.FocusedTouch, action.WasteNot, action.WasteNot2, action.MastersMend, action.Manipulation]


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


def get_random_action(state):
    # Gets a random valid action based on the state.
    # (Will add CP checks if necessary, but that would be a lot of extra calculation.)
    if state.step_number == 0:  # Opening actions should always be used and can only be used now
        return first_step_actions[random.randint(0, 1)]
    elif state.material_condition == "good":  # Good condition has exclusive actions
        i = random.randrange(0, len(good_condition_actions))
        # Prudent Touch cannot be used while Waste Not buff is active
        if state.waste_not > 0 and i == good_condition_actions.index(action.PrudentTouch):
            while i == good_condition_actions.index(action.PrudentTouch):
                i = random.randrange(0, len(good_condition_actions))
        return good_condition_actions[random.randrange(0, len(good_condition_actions))]
    i = random.randrange(0, len(actions))
    # Prudent Touch cannot be used while Waste Not buff is active
    if state.waste_not > 0 and i == actions.index(action.PrudentTouch):
        while i == actions.index(action.PrudentTouch):
            i = random.randrange(0, len(actions))
    return actions[random.randrange(0, len(actions))]
