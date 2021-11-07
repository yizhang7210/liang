import functools
import logging
import signal
import time

from liang import (
    environment,
    handlers,
    utils
)

logger = logging.getLogger(__name__)

METRIC_NAME = 'LATENCY_SECONDS'


def require(threshold_seconds: int, handler: handlers.FailureHandler = None):

    if threshold_seconds <= 0:
        raise ValueError(f"threshold_seconds needs to be an integer greater than 0")

    if not handler:
        handler = handlers.RaiseExceptionFailureHandler()

    def decorator_require(func):
        def _handle_timeout(signum, frame):
            context = environment.ExecutionContext(func, METRIC_NAME, threshold_seconds, None)
            handler.handle(context)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(threshold_seconds)

            try:
                signature = utils.get_function_signature(args, kwargs)
                logger.info(f"Function {func.__name__!r}({signature}) starting execution.")
                start = time.perf_counter()
                output = func(*args, **kwargs)
                end = time.perf_counter()
                elapsed_time_seconds = end - start
                logger.info(f"Function {func.__name__!r}({signature}) finished in {elapsed_time_seconds:.4f} seconds.")
            finally:
                signal.alarm(0)

            return output

        return wrapper

    return decorator_require


def recommend(threshold_seconds: int, handler: handlers.FailureHandler = None):
    if not handler:
        handler = handlers.LogWarningFailureHandler()

    def decorator_measure(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signature = utils.get_function_signature(args, kwargs)
            logger.info(f"Function {func.__name__!r}({signature}) starting execution.")
            start = time.perf_counter()
            output = func(*args, **kwargs)
            end = time.perf_counter()
            elapsed_time_seconds = end - start
            logger.info(f"Function {func.__name__!r}({signature}) finished in {elapsed_time_seconds:.4f} seconds.")

            if elapsed_time_seconds > threshold_seconds:
                context = environment.ExecutionContext(func, METRIC_NAME, threshold_seconds, elapsed_time_seconds)
                handler.handle(context)

            return output

        return wrapper

    return decorator_measure
