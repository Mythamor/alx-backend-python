#!/usr/bin/env python3

"""
Module: 8. Complex types - functions
"""


from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    function that takes a float multiplier as argument
    returns a function that multiplies a float by multiplier
    """
    def multiplier_function(x: float) -> float:
        """
        function that multiplies a float by multiplier
        """
        return x * multiplier

    return multiplier_function
