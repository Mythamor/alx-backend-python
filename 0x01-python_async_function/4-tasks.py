#!/usr/bin/env python3

"""
Module: 4-tasks.py
"""


import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    asynchronous routine that takes two integer arguments, n and max_delay
    It spawns wait_random n times with the specified max_delay
    """
    delays = [float(await task_wait_random(max_delay)) for _ in range(n)]
    return sorted(delays)
