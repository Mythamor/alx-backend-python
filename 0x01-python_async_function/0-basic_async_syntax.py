#!/usr/bin/env python3

"""
Module: 0-basic_async_syntax.py
"""


import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    defines an asynch coroutine, takes an integer arg
    returns a flaot
    """

    # Generates a random float between 0 -  max_delay
    delay = random.uniform(0, max_delay)

    # Pauses the execution for the coroutine, without blocking event loop
    await asyncio.sleep(delay)
    return delay
