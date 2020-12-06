"""
Chance.

    Helper functions for probability based actions.
"""

from random import uniform


def chance(percent: float) -> bool:
    """Given float, return if random number is within percent."""
    return uniform(0, 1) < percent
