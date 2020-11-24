"""
Individual.

    Where individual is a ordered list of actions from a DOMAIN.
"""


from typing import Any, List


class Individual():

    def __init__(self, value: List[Any]):
        self.value = value

    def __str__(self):
        output = "["
        size = len(self.value)
        for member_index in range(0, size):
            output = output + str(self.value[member_index]) + \
                ("" if member_index == (size-1) else ", ")
        output = output + "]"
        return output
