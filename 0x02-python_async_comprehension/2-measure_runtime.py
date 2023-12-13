#!/usr/bi/env python3

"""
Module: 2-measure_runtime.py
"""


import asyncio
from typing import List

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Measure the total runtime of executing
    async_comprehension four times in parallel
    """
    start_time = asyncio.get_event_loop().time()

    # Execute async_comprehension four times in parallel using asyncio.gather
    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )

    end_time = asyncio.get_event_loop().time()

    return end_time - start_time
