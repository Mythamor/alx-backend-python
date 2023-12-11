#!/usr/bin/env python3

"""
Module: 1-concurrent_coroutines.py
"""


import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    asynchronous routine that takes two integer arguments, n and max_delay
    It spawns wait_random n times with the specified max_delay
    """
    delays = [float(await wait_random(max_delay)) for _ in range(n)]
    return sorted(delays)
