#!/usr/bin/env python3

"""
Module: 1-concurrent_coroutines.py
"""


import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list:
    """
    asynchronous routine that takes two integer arguments, n and max_delay
    It spawns wait_random n times with the specified max_delay
    
    Args:
        n (int): Number of times to spawn wait_random
        max_delay (int): The maximum delay value for wait_random

    Returns:
        list: List of delays (float values) in ascending order

    """
    delays = [await wait_random(max_delay) for _ in range(n)]
    return sorted(delays)
