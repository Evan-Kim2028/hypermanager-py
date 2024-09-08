import time
from typing import Callable, Awaitable


def timer(func: Callable[..., Awaitable[None]]) -> Callable[..., Awaitable[None]]:
    """
    A decorator to measure and print the execution time of an asynchronous function.

    Args:
        func (Callable[..., Awaitable[None]]): The asynchronous function to measure.

    Returns:
        Callable[..., Awaitable[None]]: The wrapped function with timing functionality.
    """

    async def wrapper(*args, **kwargs):
        print_time = kwargs.pop("print_time", True)
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        if print_time:
            print(f"{func.__name__} query finished in {
                  end_time - start_time:.2f} seconds.")
        return result

    return wrapper
