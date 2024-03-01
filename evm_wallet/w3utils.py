from evm_wallet.logger import W3Logger
from evm_wallet.w3error import W3Error
import time
import random
import asyncio

RETRY_COUNT = 3
DELAY_TIME = 2


def async_retry(async_func):
    async def wrapper(*args, **kwargs):
        tries, delay = RETRY_COUNT, DELAY_TIME
        while tries > 0:
            try:
                return await async_func(*args, **kwargs)
            except Exception as e:
                W3Logger().error(f"Error | {e}")
                tries -= 1
                if tries <= 0:
                    raise
                await asyncio.sleep(delay)

                delay *= 2
                delay += random.uniform(0, 1)
                delay = min(delay, 10)

    return wrapper


def retry(func):
    def wrapper(*args, **kwargs):
        retries = 0
        while retries <= RETRY_COUNT:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                W3Logger().error(f"Error | {e}")
                sleep(10, 20)
                retries += 1

                if retries == RETRY_COUNT:
                    raise W3Error(e)

    return wrapper


def sleep(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)

    W3Logger().info(f"💤 Sleep {delay} s.")
    for _ in range(delay):
        time.sleep(1)

async def async_sleep(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)

    W3Logger().info(f"💤 Sleep {delay} s.")
    for _ in range(delay):
        await asyncio.sleep(1)