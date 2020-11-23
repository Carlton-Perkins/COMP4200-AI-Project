class State:

    CONDITIONS = ["normal", "good", "pliant", "centered", "sturdy"]

    def __init__(self):
        self.cp = 572
        self.progress = 0
        self.quality = 0
        self.durability = 50
        self.material_condition = State.CONDITIONS[0]
        self.step = 0
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

    def update_condition(self, index):
        self.material_condition = State.CONDITIONS[index]

    def step(self):
        # Decrements buffs and increments step counter.
        self.step += 1
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
