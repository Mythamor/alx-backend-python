#!/usr/bin/env python3

"""
Module: 10. Duck typing - first element of a sequence
"""


from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Duck-typing the first element of a sequence
    """
    if lst:
        return lst[0]
    else:
        return None
