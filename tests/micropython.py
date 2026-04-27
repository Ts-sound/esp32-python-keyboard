"""
Micropython stub for testing on CPython.
"""


def const(value):
    """Stub for micropython.const - returns value unchanged"""
    return value


import asyncio as _asyncio_module


async def sleep_ms(ms):
    """Stub for asyncio.sleep_ms - converts ms to seconds"""
    await _asyncio_module.sleep(ms / 1000)


_asyncio_module.sleep_ms = sleep_ms