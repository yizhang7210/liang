import functools
import time
import logging


def get_function_signature(args, kwargs):
    args_repr = [repr(a) for a in args]
    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
    signature = ", ".join(args_repr + kwargs_repr)
    return signature


def require(threshold_in_seconds):
    def decorator_require(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            output = func(*args, **kwargs)
            end = time.perf_counter()
            elapsed_time = end - start
            signature = get_function_signature(args, kwargs)
            logging.info(f"Function {func.__name__!r}({signature}) finished in {elapsed_time:.4f} seconds.")

            if elapsed_time > threshold_in_seconds:
                raise RuntimeError(f"Function {func.__name__!r}({signature}) finished in {elapsed_time:.4f} seconds,"
                                   f"but is required to finish in {threshold_in_seconds} seconds.")

            return output
        return wrapper

    return decorator_require
