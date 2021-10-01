import functools
import logging
import time

from liang import (
    environment,
    handlers
)

METRIC_NAME = 'LATENCY'


def require(threshold_in_seconds: int, handler: handlers.FailureHandler = None):
    if not handler:
        handler = handlers.RaiseExceptionFailureHandler()

    def decorator_require(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            output = func(*args, **kwargs)
            end = time.perf_counter()
            elapsed_time_seconds = end - start
            logging.info(f"Function {func.__name__!r} finished in {elapsed_time_seconds:.4f} seconds.")

            if elapsed_time_seconds > threshold_in_seconds:
                context = environment.ExecutionContext(func, args, kwargs, METRIC_NAME, threshold_in_seconds, elapsed_time_seconds)
                handler.handle(context)

            return output

        return wrapper

    return decorator_require
