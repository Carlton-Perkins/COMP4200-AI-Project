"""
Individual.

    Where individual is a ordered list of actions from a DOMAIN.
"""


from typing import Any, List


class Individual():
    """Generic Individual interface."""

    def __init__(self, value: List[Any]):
        """Construct indiv with a predefined list."""
        self.value = value

    def __str__(self):
        """Printer for generic Individuals."""
        output = "["
        size = len(self.value)
        for member_index in range(0, size):
            which, a, b = self.value[member_index]
            output = output + "{0}:{1}:{2}".format(which.__name__, a, b) + \
                ("" if member_index == (size-1) else ", ")
        output = output + "]"
        return output

    def __len__(self):
        """Pass through method for len of value."""
        len(self.value)
