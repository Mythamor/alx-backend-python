#!/usr/bin/env python3

"""
Module: 6. Complex types - mixed list
"""


from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    function which takes a list mxd_lst of integers & floats
    returns their sum as a float.
    """
    return sum(mxd_lst)
