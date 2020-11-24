import math

# TODO: Implement skill failure handling, pliant proc handling


class Action:

    __CRAFTSMANSHIP = 2689
    __CONTROL = 2872
    __RLEVEL = 511
    __CLEVEL = 420
    __RCRAFTS = 2620
    __RCONTROL = 2540
    __MAX_PROGRESS = 11126
    __MAX_QUALITY = 82400

    @staticmethod
    def execute(state):
        pass

    @staticmethod
    def __calc_progress(state, efficiency):
        # Source:  https://docs.google.com/document/d/1Da48dDVPB7N4ignxGeo0UeJ_6R0kQRqzLUH-TkpSQRc/edit
        p1 = Action.__CRAFTSMANSHIP * 21 / 100 + 2
        p2 = p1 * (Action.__CRAFTSMANSHIP + 10000) / (2620 + 10000)
        p3 = p2 * 80 / 100
        modifier = 100
        if state.muscle_memory > 0:
            modifier += 100
            state.muscle_memory = 0
        if state.veneration > 0:
            modifier += 50
        return math.floor(math.floor(p3) * (efficiency * modifier / 100)), state

    @staticmethod
    def __calc_quality(state, efficiency):
        # Source:  https://docs.google.com/document/d/1Da48dDVPB7N4ignxGeo0UeJ_6R0kQRqzLUH-TkpSQRc/edit
        f_iq = Action.__CONTROL + Action.__CONTROL * ((state.iq_stacks - 1 if state.iq_stacks > 0 else 0) * 20 / 100)
        q1 = f_iq * 35 / 100 + 35
        q2 = q1 * (f_iq + 1000) / (Action.__RCONTROL + 10000)
        q3 = q2 * 60 / 100
        modifier = 100
        if state.great_strides > 0:
            modifier += 100
            state.great_strides = 0
        if state.innovation > 0:
            modifier += 50
        if 0 < state.iq_stacks < 11:
            state.iq_stacks += 1
        return math.floor(
            math.floor(q3 * 150 if state.material_condition == "good" else 100)
            * (efficiency * modifier / 100)), state


class BasicSynthesis(Action):

    @staticmethod
    def execute(state):
        progress, state = BasicSynthesis.__calc_progress(state, 120)
        progress += state.progress
        if progress > BasicSynthesis.__MAX_PROGRESS:
            progress = BasicSynthesis.__MAX_PROGRESS
            if state.final_appraisal > 0:
                # Check whether the buff falls off after you've "consumed" it; assuming yes for now
                state.final_appraisal = 0
                progress -= 1  # leave craft 1 progress off from completion
        state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3  # TODO: test this to double check whether the loss is 2 or 3
        state.durability -= durability_loss
        return state


class RapidSynthesis(Action):

    @staticmethod
    def execute(state):
        progress, state = RapidSynthesis.__calc_progress(state, 500)
        progress += state.progress
        if progress > RapidSynthesis.__MAX_PROGRESS:
            progress = RapidSynthesis.__MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        return state


class CarefulSynthesis(Action):

    @staticmethod
    def execute(state):
        progress, state = CarefulSynthesis.__calc_progress(state, 150)
        progress += state.progress
        if progress > CarefulSynthesis.__MAX_PROGRESS:
            progress = CarefulSynthesis.__MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 7
        return state


class Groundwork(Action):

    @staticmethod
    def execute(state):
        # Double check whether efficiency penalty only applies if the craft will be broken
        durability_loss = 20
        efficiency = 300
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 5
        if state.durability < durability_loss:
            efficiency = 150
        progress, state = Groundwork.__calc_progress(state, efficiency)
        progress += state.progress
        if progress > Groundwork.__MAX_PROGRESS:
            progress = Groundwork.__MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        state.cp -= 18
        return state


class IntensiveSynthesis(Action):

    @staticmethod
    def execute(state):
        progress, state = IntensiveSynthesis.__calc_progress(state, 300)
        progress += state.progress
        if progress > IntensiveSynthesis.__MAX_PROGRESS:
            progress = IntensiveSynthesis.__MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 6
        return state


class MuscleMemory(Action):

    @staticmethod
    def execute(state):
        progress, state = MuscleMemory.__calc_progress(state, 300)
        # This can only be used on the first turn, with 0 progress. No need for completion checking
        # (but we will need to make sure we ONLY use this on the first turn)
        state.progress = progress
        state.muscle_memory = 5
        state.cp -= 6
        state.durability -= 10
        return state


class BrandoftheElements(Action):
    # This one works weird with another buff so we have to modify progress calculation

    @staticmethod
    def execute(state):
        progress, state = BrandoftheElements.__calc_progress(state, 100)
        progress += state.progress
        if progress > BrandoftheElements.__MAX_PROGRESS:
            progress = BrandoftheElements.__MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 6
        return state

    @staticmethod
    def __calc_progress(state, efficiency):
        # Source:  https://docs.google.com/document/d/1Da48dDVPB7N4ignxGeo0UeJ_6R0kQRqzLUH-TkpSQRc/edit
        p1 = BrandoftheElements.__CRAFTSMANSHIP * 21 / 100 + 2
        p2 = p1 * (BrandoftheElements.__CRAFTSMANSHIP + 10000) / (2620 + 10000)
        p3 = p2 * 80 / 100
        modifier = 100
        if state.muscle_memory > 0:
            modifier += 100
            state.muscle_memory = 0
        if state.veneration > 0:
            modifier += 50
        f_efficiency = efficiency * modifier / 100
        if state.name_elements > 0:
            f_efficiency = f_efficiency + 2 * math.ceil((1 - state.progress / BrandoftheElements.__MAX_PROGRESS) * 100)
        return math.floor(math.floor(p3) * f_efficiency), state


class NameoftheElements(Action):

    @staticmethod
    def execute(state):
        state.name_elements = 3
        state.cp -= 30
        return state


class Veneration(Action):

    @staticmethod
    def execute(state):
        state.veneration = 4
        state.cp -= 18
        return state


class FinalAppraisal(Action):

    @staticmethod
    def execute(state):
        state.final_appraisal = 5
        state.cp -= 1
        return state


class DelicateSynthesis(Action):

    @staticmethod
    def execute(state):
        progress, state = DelicateSynthesis.__calc_progress(state, 100)
        quality, state = DelicateSynthesis.__calc_quality(state, 100)
        progress += state.progress
        if progress > DelicateSynthesis.__MAX_PROGRESS:
            progress = DelicateSynthesis.__MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        if quality > DelicateSynthesis.__MAX_QUALITY:
            quality = DelicateSynthesis.__MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 32
        return state


class BasicTouch(Action):

    @staticmethod
    def execute(state):
        quality, state = BasicTouch.__calc_quality(state, 100)
        quality += state.quality
        if quality > BasicTouch.__MAX_QUALITY:
            quality = BasicTouch.__MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 18
        return state


class HastyTouch(Action):

    @staticmethod
    def execute(state):
        quality, state = HastyTouch.__calc_quality(state, 100)
        quality += state.quality
        if quality > HastyTouch.__MAX_QUALITY:
            quality = HastyTouch.__MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        return state


class StandardTouch(Action):

    @staticmethod
    def execute(state):
        quality, state = StandardTouch.__calc_quality(state, 125)
        quality += state.quality
        if quality > StandardTouch.__MAX_QUALITY:
            quality = StandardTouch.__MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 32
        return state


class PreparatoryTouch(Action):

    @staticmethod
    def execute(state):
        quality, state = PreparatoryTouch.__calc_quality(state, 200)
        quality += state.quality
        if quality > PreparatoryTouch.__MAX_QUALITY:
            quality = PreparatoryTouch.__MAX_QUALITY
        state.quality = quality
        durability_loss = 20
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 10
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        state.cp -= 40
        if 0 < state.iq_stacks < 11:
            state.iq_stacks += 1
        return state


class PreciseTouch(Action):

    @staticmethod
    def execute(state):
        quality, state = PreciseTouch.__calc_quality(state, 150)
        quality += state.quality
        if quality > PreciseTouch.__MAX_QUALITY:
            quality = PreciseTouch.__MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 18
        if 0 < state.iq_stacks < 11:
            state.iq_stacks += 1
        return state


class PatientTouch(Action):
    # Unsure whether to handle failure condition in this class or in the test; maybe have failure function?

    @staticmethod
    def execute(state):
        quality, state = PatientTouch.__calc_quality(state, 100)
        quality += state.quality
        if quality > PatientTouch.__MAX_QUALITY:
            quality = PatientTouch.__MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 6
        if 0 < state.iq_stacks < 11:
            state.iq_stacks = (state.iq_stacks - 1) * 2  # quality function increased stacks by 1
            if state.iq_stacks > 11:
                state.iq_stacks = 11
        return state


class PrudentTouch(Action):

    @staticmethod
    def execute(state):
        quality, state = PrudentTouch.__calc_quality(state, 100)
        quality += state.quality
        if quality > PrudentTouch.__MAX_QUALITY:
            quality = PrudentTouch.__MAX_QUALITY
        state.quality = quality
        durability_loss = 5
        if state.material_condition == "sturdy":  # cannot be used while waste not is active
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 25
        return state


class Reflect(Action):

    @staticmethod
    def execute(state):
        quality, state = Reflect.__calc_quality(state, 100)
        # This can only be used on the first turn, with 0 quality. No need for over-cap checking
        # (but we will need to make sure we ONLY use this on the first turn)
        state.quality = quality
        state.iq_stacks = 3
        state.durability -= 10
        state.cp -= 24
        return state


class ByregotsBlessing(Action):

    @staticmethod
    def execute(state):
        quality, state = ByregotsBlessing.__calc_quality(state, 100 + 20 * (state.iq_stacks - 1))
        state.iq_stacks = 0
        quality += state.quality
        if quality > ByregotsBlessing.__MAX_QUALITY:
            quality = ByregotsBlessing.__MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 24
        return state


class GreatStrides(Action):

    @staticmethod
    def execute(state):
        state.great_strides = 3
        state.cp -= 32
        return state


class Innovation(Action):

    @staticmethod
    def execute(state):
        state.innovation = 4
        state.cp -= 18
        return state


class InnerQuiet(Action):

    @staticmethod
    def execute(state):
        state.iq_stacks = 1
        state.cp -= 18
        return state


class Observe(Action):

    @staticmethod
    def execute(state):
        state.observe = 1
        state.cp -= 7
        return state


class FocusedSynthesis(Action):

    @staticmethod
    def execute(state):
        progress, state = FocusedSynthesis.__calc_progress(state, 200)
        progress += state.progress
        if progress > FocusedSynthesis.__MAX_PROGRESS:
            progress = FocusedSynthesis.__MAX_PROGRESS
            if state.final_appraisal > 0:
                # Check whether the buff falls off after you've "consumed" it; assuming yes for now
                state.final_appraisal = 0
                progress -= 1  # leave craft 1 progress off from completion
        state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 5
        return state


class FocusedTouch(Action):

    @staticmethod
    def execute(state):
        quality, state = FocusedTouch.__calc_quality(state, 150)
        quality += state.quality
        if quality > FocusedTouch.__MAX_QUALITY:
            quality = FocusedTouch.__MAX_QUALITY
        state.quality = quality
        durability_loss = 5
        if state.material_condition == "sturdy":  # cannot be used while waste not is active
            durability_loss = 3
        state.durability -= durability_loss
        state.cp -= 18
        return state


class TricksoftheTrade(Action):

    @staticmethod
    def execute(state):
        state.cp += 20
        return state


class WasteNot(Action):

    @staticmethod
    def execute(state):
        state.waste_not = 4
        state.cp -= 56
        return state


class WasteNot2(Action):

    @staticmethod
    def execute(state):
        state.waste_not = 8
        state.cp -= 98
        return state


class MastersMend(Action):

    @staticmethod
    def execute(state):
        state.durability += 30
        if state.durability > 50:
            state.durability = 50
        state.cp -= 88
        return state


class Manipulation(Action):

    @staticmethod
    def execute(state):
        state.manipulation = 8
        state.cp -= 96
        return state
