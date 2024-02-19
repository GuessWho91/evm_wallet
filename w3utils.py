from logger import W3Logger
from w3error import W3Error
import time
import random

RETRY_COUNT = 2


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
