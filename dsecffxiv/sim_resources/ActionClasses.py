import math

# Represents crafting actions as state transition calculations. Each action takes a state as an argument, updates it,
# and returns it. Equations for progress and quality were pulled from:
# https://docs.google.com/document/d/1Da48dDVPB7N4ignxGeo0UeJ_6R0kQRqzLUH-TkpSQRc/edit


class Action:

    _CRAFTSMANSHIP = 2689
    _CONTROL = 2872
    _RLEVEL = 511
    _CLEVEL = 420
    _RCRAFTS = 2620
    _RCONTROL = 2540
    _MAX_PROGRESS = 11126
    _MAX_QUALITY = 82400

    @staticmethod
    def execute(state):
        pass

    @staticmethod
    def _calc_progress(state, efficiency):
        # Source:  https://docs.google.com/document/d/1Da48dDVPB7N4ignxGeo0UeJ_6R0kQRqzLUH-TkpSQRc/edit
        p1 = Action._CRAFTSMANSHIP * 21 / 100 + 2
        p2 = p1 * (Action._CRAFTSMANSHIP + 10000) / (2620 + 10000)
        p3 = p2 * 80 / 100
        modifier = 100
        if state.muscle_memory > 0:
            modifier += 100
            state.muscle_memory = 0
        if state.veneration > 0:
            modifier += 50
        return math.floor(math.floor(p3) * (efficiency / 100 * modifier / 100)), state

    @staticmethod
    def _calc_quality(state, efficiency):
        # Source:  https://docs.google.com/document/d/1Da48dDVPB7N4ignxGeo0UeJ_6R0kQRqzLUH-TkpSQRc/edit
        f_iq = Action._CONTROL + Action._CONTROL * \
            ((state.iq_stacks - 1 if state.iq_stacks > 0 else 0) * 20 / 100)
        q1 = f_iq * 35 / 100 + 35
        q2 = q1 * (f_iq + 10000) / (Action._RCONTROL + 10000)
        q3 = q2 * 60 / 100
        modifier = 100
        if state.great_strides > 0:
            modifier += 100
            state.great_strides = 0
        if state.innovation > 0:
            modifier += 50
        if 0 < state.iq_stacks < 11:
            state.iq_stacks += 1
        if state.material_condition == "good":
            condition = 150
        else:
            condition = 100
        return math.floor(math.floor(q3 * condition / 100) * (efficiency / 100 * modifier / 100)), state

    def __str__(self) -> str:
        return __name__


class BasicSynthesis(Action):
    # Increases progress with efficiency of 120. Costs 10 durability and 0 CP.

    CP_COST = 0
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        progress, state = BasicSynthesis._calc_progress(state, 120)
        progress += state.progress
        if progress > BasicSynthesis._MAX_PROGRESS:
            progress = BasicSynthesis._MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1  # leave craft 1 progress off from completion
        state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        return state


class RapidSynthesis(Action):
    # Increases progress with efficiency of 500. Has a 50% success rate. Costs 10 durability and 0 CP.

    CP_COST = 0
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        success_threshold = 49
        if state.material_condition == "centered":
            success_threshold += 25
        if state.success_val <= success_threshold:
            progress, state = RapidSynthesis._calc_progress(state, 500)
            progress += state.progress
            if progress > RapidSynthesis._MAX_PROGRESS:
                progress = RapidSynthesis._MAX_PROGRESS
                if state.final_appraisal > 0:
                    state.final_appraisal = 0
                    progress -= 1
            state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        return state


class CarefulSynthesis(Action):
    # Increases progress with efficiency of 150. Costs 10 durability and 7 CP.

    CP_COST = 7
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        progress, state = CarefulSynthesis._calc_progress(state, 150)
        progress += state.progress
        if progress > CarefulSynthesis._MAX_PROGRESS:
            progress = CarefulSynthesis._MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        cp_loss = 7
        if state.material_condition == "pliant":
            cp_loss = 4
        state.cp -= cp_loss
        return state


class Groundwork(Action):
    # Increases progress with efficiency of 300. Costs 20 durability and 18 CP. If current durability is less than the
    # cost of the action, efficiency is reduced to 150.

    CP_COST = 18
    DURABILITY_COST = 20

    @staticmethod
    def execute(state):
        durability_loss = 20
        efficiency = 300
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 10
        if state.durability < durability_loss:
            efficiency = 150
        progress, state = Groundwork._calc_progress(state, efficiency)
        progress += state.progress
        if progress > Groundwork._MAX_PROGRESS:
            progress = Groundwork._MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        cp_loss = 18
        if state.material_condition == "pliant":
            cp_loss = 9
        state.cp -= cp_loss
        return state


class IntensiveSynthesis(Action):
    # Increases progress with efficiency of 300. Can only be used when Material Condition is Good. Costs 10 durability
    # and 6 CP.

    CP_COST = 6
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        progress, state = IntensiveSynthesis._calc_progress(state, 300)
        progress += state.progress
        if progress > IntensiveSynthesis._MAX_PROGRESS:
            progress = IntensiveSynthesis._MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        durability_loss = 10
        if state.waste_not > 0:  # Material condition must be Good; cannot be Sturdy
            durability_loss = 5
        state.durability -= durability_loss
        state.cp -= 6
        return state


class MuscleMemory(Action):
    # Increases progress with efficiency of 300. Applies buff that increases efficiency of next progress action by 100
    # if it is used within the next 5 turns. Costs 10 durability and 6 CP. Can only be used on the first turn.

    CP_COST = 6
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        progress, state = MuscleMemory._calc_progress(state, 300)
        # This can only be used on the first turn, with 0 progress. No need for completion checking
        # (but we will need to make sure we ONLY use this on the first turn)
        state.progress = progress
        state.muscle_memory = 6  # Extra turn because step function always decrements
        cp_loss = 6
        if state.material_condition == "pliant":
            cp_loss = 3
        state.cp -= cp_loss
        state.durability -= 10
        return state


class BrandoftheElements(Action):
    # Increases progress with an efficiency of 100. Costs 10 durability and 6 CP. If Name of the Elements is active,
    # progress efficiency scales based on remaining progress (more remaining progress = bigger progress bonus).

    CP_COST = 6
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        progress, state = BrandoftheElements._calc_progress(state, 100)
        progress += state.progress
        if progress > BrandoftheElements._MAX_PROGRESS:
            progress = BrandoftheElements._MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        cp_loss = 6
        if state.material_condition == "pliant":
            cp_loss = 3
        state.cp -= cp_loss
        return state

    @staticmethod
    def _calc_progress(state, efficiency):
        # Source:  https://docs.google.com/document/d/1Da48dDVPB7N4ignxGeo0UeJ_6R0kQRqzLUH-TkpSQRc/edit
        # This one works with another buff so we have to modify the progress calculation.
        p1 = BrandoftheElements._CRAFTSMANSHIP * 21 / 100 + 2
        p2 = p1 * (BrandoftheElements._CRAFTSMANSHIP + 10000) / (2620 + 10000)
        p3 = p2 * 80 / 100
        modifier = 100
        if state.muscle_memory > 0:
            modifier += 100
            state.muscle_memory = 0
        if state.veneration > 0:
            modifier += 50
        f_efficiency = efficiency / 100 * modifier / 100
        if state.name_elements > 0:
            f_efficiency = f_efficiency + 2 * \
                math.ceil(1 - state.progress /
                          BrandoftheElements._MAX_PROGRESS)
        return math.floor(math.floor(p3) * f_efficiency), state


class NameoftheElements(Action):
    # Applies buff that makes Brand of the Elements scale its progress efficiency based on progress remaining in the
    # craft. Costs 30 CP. Lasts 3 turns.

    CP_COST = 30
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.name_elements = 4  # Extra turn because step always decrements
        cp_loss = 30
        if state.material_condition == "pliant":
            cp_loss = 15
        state.cp -= cp_loss
        return state


class Veneration(Action):
    # Increases progress action efficiency by 50 for 4 steps. Costs 18 CP.

    CP_COST = 18
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.veneration = 5  # Extra turn because step always decrements
        cp_loss = 18
        if state.material_condition == "pliant":
            cp_loss = 9
        state.cp -= cp_loss
        return state


class FinalAppraisal(Action):
    # Leaves 1 progress remaining on a craft if it would have been completed for the next 5 turns. Falls off when craft
    # would have been completed. Costs 1 CP.

    CP_COST = 1
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.final_appraisal = 6  # Extra turn because step always decrements
        state.cp -= 1
        return state


class DelicateSynthesis(Action):
    # Increases progress and quality at the same time with an efficiency of 100. Costs 10 durability and 32 CP.

    CP_COST = 32
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        progress, state = DelicateSynthesis._calc_progress(state, 100)
        quality, state = DelicateSynthesis._calc_quality(state, 100)
        progress += state.progress
        if progress > DelicateSynthesis._MAX_PROGRESS:
            progress = DelicateSynthesis._MAX_PROGRESS
            if state.final_appraisal > 0:
                state.final_appraisal = 0
                progress -= 1
        state.progress = progress
        if quality > DelicateSynthesis._MAX_QUALITY:
            quality = DelicateSynthesis._MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        cp_loss = 32
        if state.material_condition == "pliant":
            cp_loss = 16
        state.cp -= cp_loss
        return state


class BasicTouch(Action):
    # Increases quality with an efficiency of 100. Costs 10 durability and 18 CP.

    CP_COST = 18
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        quality, state = BasicTouch._calc_quality(state, 100)
        quality += state.quality
        if quality > BasicTouch._MAX_QUALITY:
            quality = BasicTouch._MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        cp_loss = 18
        if state.material_condition == "pliant":
            cp_loss = 9
        state.cp -= cp_loss
        return state


class HastyTouch(Action):
    # Increases quality with an efficiency of 100. Has a 60% success rate. Costs 10 durability and 0 CP.

    CP_COST = 0
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        success_threshold = 59
        if state.material_condition == "centered":
            success_threshold += 25
        if state.success_val <= success_threshold:
            quality, state = HastyTouch._calc_quality(state, 100)
            quality += state.quality
            if quality > HastyTouch._MAX_QUALITY:
                quality = HastyTouch._MAX_QUALITY
            state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        return state


class StandardTouch(Action):
    # Increases quality with an efficiency of 125. Costs 10 durability and 32 CP.

    CP_COST = 32
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        quality, state = StandardTouch._calc_quality(state, 125)
        quality += state.quality
        if quality > StandardTouch._MAX_QUALITY:
            quality = StandardTouch._MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        cp_loss = 32
        if state.material_condition == "pliant":
            cp_loss = 16
        state.cp -= cp_loss
        return state


class PreparatoryTouch(Action):
    # Increases quality with an efficiency of 200. Costs 20 durability and 40 CP.

    CP_COST = 40
    DURABILITY_COST = 20

    @staticmethod
    def execute(state):
        quality, state = PreparatoryTouch._calc_quality(state, 200)
        quality += state.quality
        if quality > PreparatoryTouch._MAX_QUALITY:
            quality = PreparatoryTouch._MAX_QUALITY
        state.quality = quality
        durability_loss = 20
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 5
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 10
        state.durability -= durability_loss
        cp_loss = 40
        if state.material_condition == "pliant":
            cp_loss = 20
        state.cp -= cp_loss
        if 0 < state.iq_stacks < 11:
            state.iq_stacks += 1
        return state


class PreciseTouch(Action):
    # Increases quality with an efficiency of 150. Grants an extra Inner Quiet stack. Can only be used when Material
    # Condition is Good. Costs 10 durability and 18 CP.

    CP_COST = 18
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        quality, state = PreciseTouch._calc_quality(state, 150)
        quality += state.quality
        if quality > PreciseTouch._MAX_QUALITY:
            quality = PreciseTouch._MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0:  # Material condition must be Good; cannot be Sturdy
            durability_loss = 5
        state.durability -= durability_loss
        state.cp -= 18
        if 0 < state.iq_stacks < 11:
            state.iq_stacks += 1
        return state


class PatientTouch(Action):
    # Increases quality with efficiency of 100. Has a 50% chance of success. If it succeeds, Inner Quiet stacks are
    # doubled, respecting the maximum of 11 stacks. If it fails, Inner Quiet stacks are cut in half. Costs 10 durability
    # and 6 CP.

    CP_COST = 6
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        success_threshold = 49
        if state.material_condition == "centered":
            success_threshold += 25
        if state.success_val <= success_threshold:
            quality, state = PatientTouch._calc_quality(state, 100)
            quality += state.quality
            if quality > PatientTouch._MAX_QUALITY:
                quality = PatientTouch._MAX_QUALITY
            state.quality = quality
            if 0 < state.iq_stacks < 11:
                # quality function increased stacks by 1
                state.iq_stacks = (state.iq_stacks - 1) * 2
                if state.iq_stacks > 11:
                    state.iq_stacks = 11
        else:
            if state.iq_stacks > 0:
                state.iq_stacks = math.ceil(state.iq_stacks / 2)
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        cp_loss = 6
        if state.material_condition == "pliant":
            cp_loss = 3
        state.cp -= cp_loss
        return state


class PrudentTouch(Action):
    # Increases quality with an efficiency of 100. Costs 5 durability and 25 CP. Cannot be used while either Waste Not
    # buff is active.

    CP_COST = 25
    DURABILITY_COST = 5

    @staticmethod
    def execute(state):
        quality, state = PrudentTouch._calc_quality(state, 100)
        quality += state.quality
        if quality > PrudentTouch._MAX_QUALITY:
            quality = PrudentTouch._MAX_QUALITY
        state.quality = quality
        durability_loss = 5
        if state.material_condition == "sturdy":  # cannot be used while waste not is active
            durability_loss = 3
        state.durability -= durability_loss
        cp_loss = 25
        if state.material_condition == "pliant":
            cp_loss = 13
        state.cp -= cp_loss
        return state


class Reflect(Action):
    # Increases quality with an efficiency of 100 and grants 3 Inner Quiet stacks. Costs 10 durability and 24 CP. Can
    # only be used on the first turn.

    CP_COST = 24
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        quality, state = Reflect._calc_quality(state, 100)
        # This can only be used on the first turn, with 0 quality. No need for over-cap checking
        # (but we will need to make sure we ONLY use this on the first turn)
        state.quality = quality
        state.iq_stacks = 3
        state.durability -= 10
        cp_loss = 24
        if state.material_condition == "pliant":
            cp_loss = 12
        state.cp -= cp_loss
        return state


class ByregotsBlessing(Action):
    # Increases quality with an efficiency of 100 plus an extra 20 for every Inner Quiet stack past 1. Consumes all
    # Inner Quiet stacks upon use. Costs 10 durability and 24 CP.

    CP_COST = 24
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        quality, state = ByregotsBlessing._calc_quality(
            state, 100 + 20 * (state.iq_stacks - 1))
        state.iq_stacks = 0
        quality += state.quality
        if quality > ByregotsBlessing._MAX_QUALITY:
            quality = ByregotsBlessing._MAX_QUALITY
        state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        cp_loss = 24
        if state.material_condition == "pliant":
            cp_loss = 12
        state.cp -= cp_loss
        return state


class GreatStrides(Action):
    # Increases the efficiency of the next quality action by 100. Falls off after 3 turns if not consumed. Costs 32 CP.

    CP_COST = 32
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.great_strides = 4  # Extra turn because step always decrements
        cp_loss = 32
        if state.material_condition == "pliant":
            cp_loss = 16
        state.cp -= cp_loss
        return state


class Innovation(Action):
    # Increases the efficiency of all quality actions by 50 for 4 turns. Costs 18 CP.

    CP_COST = 18
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.innovation = 5  # Extra turn because step always decrements
        cp_loss = 18
        if state.material_condition == "pliant":
            cp_loss = 9
        state.cp -= cp_loss
        return state


class InnerQuiet(Action):
    # Applies a buff that allows stacks to be accumulated. Each stack increases Control, which affects output of quality
    # actions. A value of 1 offers no bonus, but all stacks after 1 apply the bonus additively. Maximum 11 stacks. Costs
    # 18 CP.

    CP_COST = 18
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.iq_stacks = 1
        cp_loss = 18
        if state.material_condition == "pliant":
            cp_loss = 9
        state.cp -= cp_loss
        return state


class Observe(Action):
    # Does nothing and moves to the next turn. Costs 7 CP.

    CP_COST = 7
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.observe = 2  # Extra turn because step always decrements
        cp_loss = 7
        if state.material_condition == "pliant":
            cp_loss = 4
        state.cp -= cp_loss
        return state


class FocusedSynthesis(Action):
    # Increases progress with efficiency of 200. Has a 50% chance of success on its own, but 100% chance if used on the
    # turn after Observe. Costs 10 durability and 5 CP.

    CP_COST = 5
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        success_threshold = 49
        if state.observe > 0:
            success_threshold = 100
        elif state.material_condition == "centered":
            success_threshold += 25
        if state.success_val <= success_threshold:
            progress, state = FocusedSynthesis._calc_progress(state, 200)
            progress += state.progress
            if progress > FocusedSynthesis._MAX_PROGRESS:
                progress = FocusedSynthesis._MAX_PROGRESS
                if state.final_appraisal > 0:
                    state.final_appraisal = 0
                    progress -= 1  # leave craft 1 progress off from completion
            state.progress = progress
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        cp_loss = 5
        if state.material_condition == "pliant":
            cp_loss = 3
        state.cp -= cp_loss
        return state


class FocusedTouch(Action):
    # Increases quality with an efficiency of 150. Has a 50% chance of success on its own, but 100% chance if used on
    # the turn after Observe. Costs 10 durability and 18 CP.

    CP_COST = 18
    DURABILITY_COST = 10

    @staticmethod
    def execute(state):
        success_threshold = 49
        if state.observe > 0:
            success_threshold = 100
        elif state.material_condition == "centered":
            success_threshold += 25
        if state.success_val <= success_threshold:
            quality, state = FocusedTouch._calc_quality(state, 150)
            quality += state.quality
            if quality > FocusedTouch._MAX_QUALITY:
                quality = FocusedTouch._MAX_QUALITY
            state.quality = quality
        durability_loss = 10
        if state.waste_not > 0 and state.material_condition == "sturdy":
            durability_loss = 3
        elif state.waste_not > 0 or state.material_condition == "sturdy":
            durability_loss = 5
        state.durability -= durability_loss
        cp_loss = 18
        if state.material_condition == "pliant":
            cp_loss = 9
        state.cp -= cp_loss
        return state


class TricksoftheTrade(Action):
    # Restores 20 CP. Can only be used when Material Condition is Good.

    CP_COST = -20  # subtract a negative number to get a positive number
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.cp += 20
        if state.cp > 572:
            state.cp = 572
        return state


class WasteNot(Action):
    # Reduces durability cost by 50% for the next 4 turns. Costs 56 CP.

    CP_COST = 56
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.waste_not = 5  # Extra turn because step always decrements
        cp_loss = 56
        if state.material_condition == "pliant":
            cp_loss = 28
        state.cp -= cp_loss
        return state


class WasteNot2(Action):
    # Reduces durability cost by 50% for the next 8 turns. Costs 98 CP.

    CP_COST = 98
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.waste_not = 9  # Extra turn because step always decrements
        cp_loss = 98
        if state.material_condition == "pliant":
            cp_loss = 49
        state.cp -= cp_loss
        return state


class MastersMend(Action):
    # Restores durability by 30 points (cannot go over maximum). Costs 88 CP.

    CP_COST = 88
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.durability += 30
        if state.durability > 50:
            state.durability = 50
        cp_loss = 88
        if state.material_condition == "pliant":
            cp_loss = 44
        state.cp -= cp_loss
        return state


class Manipulation(Action):
    # Restores durability by 5 points at the end of every turn for the next 8 turns. Costs 96 CP.

    CP_COST = 96
    DURABILITY_COST = 0

    @staticmethod
    def execute(state):
        state.manipulation = 9  # Extra turn because step always decrements
        cp_loss = 96
        if state.material_condition == "pliant":
            cp_loss = 48
        state.cp -= cp_loss
        return state
