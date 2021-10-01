# liang
Enforce non-functional requirements in your Python code.

## Installation
``` shell
pip install python-liang
```

## Latency
Enforce that a function takes no more than the specified amount of time
in seconds. By default, an exception will be raised if the function exceeds the
time limit.

For example, we may want to enforce that sorting an array of ten integers takes
no more than 3 seconds:
``` python
import liang.latency

@liang.latency.require(threshold_in_seconds=3)
def timsort_array(array):
    array.sort()

array = list(reversed(range(10)))
timsort_array(array)
print(array)
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

The function should complete as normal. But if we try a less efficient approach:
``` python
import random

@liang.latency.require(threshold_in_seconds=3)
def bogosort_array(array):
    while not all(array[i] <= array[i+1] for i in range(len(array)-1)):
        random.shuffle(array)

array = list(reversed(range(10)))
bogosort_array(array)
# RuntimeError: Function 'bogosort_array'([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# expected to have LATENCY to be 3 but is actually 7.129362316.
```

Sometimes, we don't want to raise an exception. We can create a custom handler.
This one will log an error using Python's `logging`:
``` python
import liang.environment
import liang.handlers
import liang.utils
import logging


class LoggerHandler(liang.handlers.FailureHandler):
    def handle(self, context: liang.environment.ExecutionContext):
        function = context.function
        signature = liang.utils.get_function_signature(
                context.args, context.kwargs)
        logging.error(
            f"Function {function.__name__!r}({signature}) expected to have "
            f"{context.metric_name} to be "
            f"{context.metric_expected} but is actually "
            f"{context.metric_actual}.")

@liang.latency.require(threshold_in_seconds=3, handler=LoggerHandler())
def bogosort_array_no_exception(array):
    while not all(array[i] <= array[i+1] for i in range(len(array)-1)):
        random.shuffle(array)

bogosort_array_no_exception(array)
# ERROR:root:Function 'bogosortt_array'([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# expected to have LATENCY to be 3 but is actually 21.552379815000002.
print(array)
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```
This way the execution continues, and you are notified of the violation.
