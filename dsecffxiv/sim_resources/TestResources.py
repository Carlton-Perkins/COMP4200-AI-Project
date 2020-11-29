import random
import dsecffxiv.sim_resources.ActionClasses as action


class TestResources:
    __SEQUENCE_LENGTH = 50
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

    @staticmethod
    def generate_material_conditions():
        conditions = [0]  # First state is always normal
        for i in range(1, TestResources.__SEQUENCE_LENGTH):
            conditions.append(random.randint(0, 4))
        return conditions

    @staticmethod
    def generate_success_values():
        values = []
        for i in range(0, TestResources.__SEQUENCE_LENGTH):
            values.append(random.randint(0, 100))
        return values

    @staticmethod
    def get_random_action(state):
        if state.step_number == 0:
            return TestResources.first_step_actions[random.randint(0, 1)]
        elif state.material_condition == "good":  # Good condition
            i = random.randrange(0, len(TestResources.good_condition_actions))
            # Prudent Touch cannot be used while Waste Not buff is active
            if state.waste_not > 0 and i == TestResources.good_condition_actions.index(action.PrudentTouch):
                while i == TestResources.good_condition_actions.index(action.PrudentTouch):
                    i = random.randrange(0, len(TestResources.good_condition_actions))
            return TestResources.good_condition_actions[random.randrange(0, len(TestResources.good_condition_actions))]
        i = random.randrange(0, len(TestResources.actions))
        # Prudent Touch cannot be used while Waste Not buff is active
        if state.waste_not > 0 and i == TestResources.actions.index(action.PrudentTouch):
            while i == TestResources.actions.index(action.PrudentTouch):
                i = random.randrange(0, len(TestResources.actions))
        return TestResources.actions[random.randrange(0, len(TestResources.actions))]
