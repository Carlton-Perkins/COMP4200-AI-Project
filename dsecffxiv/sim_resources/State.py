# Class representing the state of a craft. Each craft parameter and buff is included as an attribute, as well as a value
# that is used to calculate whether certain actions succeed or fail.

class State:

    CONDITIONS = ["normal", "good", "pliant", "centered", "sturdy"]

    def __init__(self, success):
        # Success is an argument 0-99 that is used to determine the success of an action that can fail
        self.cp = 572
        self.progress = 0
        self.quality = 0
        self.durability = 50
        self.material_condition = State.CONDITIONS[0]
        self.step_number = 0
        self.iq_stacks = 0
        self.muscle_memory = 0
        self.name_elements = 0
        self.veneration = 0
        self.final_appraisal = 0
        self.great_strides = 0
        self.innovation = 0
        self.observe = 0
        self.waste_not = 0
        self.manipulation = 0
        self.success_val = success

    def update_condition(self, index):
        # Updates condition of craft by indexing array of conditions.
        self.material_condition = State.CONDITIONS[index]

    def update_success(self, val):
        # Updates value used to calculate success of stochastic actions.
        self.success_val = val

    def step(self):
        # Decrements buffs and increments step counter.
        self.step_number += 1
        if self.muscle_memory > 0:
            self.muscle_memory -= 1
        if self.name_elements > 0:
            self.name_elements -= 1
        if self.veneration > 0:
            self.veneration -= 1
        if self.final_appraisal > 0:
            self.final_appraisal -= 1
        if self.great_strides > 0:
            self.great_strides -= 1
        if self.innovation > 0:
            self.great_strides -= 1
        if self.observe > 0:
            self.observe -= 1
        if self.waste_not > 0:
            self.waste_not -= 1
        if self.manipulation > 0:
            self.manipulation -= 1
            self.durability += 5
            if self.durability > 50:
                self.durability = 50

    def evaluate(self):
        # Calculates score based on craft parameters.
        if self.cp < 0 or (self.durability <= 0 and self.progress < 11126):
            return -1  # these are invalid states
        if self.progress < 11126 or self.quality < 58000:
            return 0  # got to end of sequence with no reward, but craft isn't broken/invalid
        collectability = self.quality // 10  # Find skyward score for craft
        if 5800 <= collectability < 6500:
            return 0.1 * (collectability - 5800) + 175
        if 6500 <= collectability < 7700:
            return 0.45 * (collectability - 6500) + 370
        if collectability >= 7700:
            return 0.3 * (collectability - 7700) + 1100
        raise Exception("You forgot a case for state evaluation.\n\n{}".format(self))

    def __str__(self):
        # Returns string with each attribute of the state listed.
        state_string = "Step: {}\nProgress: {}\nQuality: {}\nDurability: {}\nCondition: {}\nCP: {}\nInner Quiet: {}\n" \
                       "Muscle Memory: {}\nName of the Elements: {}\nVeneration: {}\nFinal Appraisal: {}\n" \
                       "Great Strides: {}\nInnovation: {}\nObserve: {}\nWaste Not: {}\nManipulation: {}\n"\
            .format(self.step, self.progress, self.quality, self.durability, self.material_condition, self.cp,
                    self.iq_stacks, self.muscle_memory, self.name_elements, self.veneration, self.final_appraisal,
                    self.great_strides, self.innovation, self.observe, self.waste_not, self.manipulation)
        return state_string
