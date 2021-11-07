# liang
Specify non-functional requirements in your Python code.

## Installation
``` shell
pip install python-liang
```

## Latency
Specify the amount of time a function is required to run under.

### APIs
``` python
@liang.latency.require(threshold_seconds=3)
"""
Used to specify when a function is _required_ to run within `threshold_seconds`.
The function is guaranteed to terminate within `threshold_seconds`. Either:
- The function runs successfully to completion, or
- TimeoutError is raised when the function takes too long
"""

@liang.latency.recommend(threshold_seconds=3)
"""
Used to specify when a function _should_ run within `threshold_seconds`.
The function is allowed to run to completion.
If the function takes longer than `threshold_seconds`, a warning will be logged.
"""

@liang.latency.require(threshold_seconds=3, handler=CustomHandler)
@liang.latency.recommend(threshold_seconds=3, handler=CustomHandler)
"""
Can specify CustomHandler to handle when a function exceeds `threshold_seconds`.
CustomHandler needs to inherit from liang.handlers.FailureHandler and implement the
`.handle(self, context: environment.ExecutionContext)` method.
"""
```


### Examples
For example, we may want to enforce that sorting an array of ten integers takes
no more than 3 seconds:
``` python
import liang.latency

@liang.latency.require(threshold_seconds=3)
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

@liang.latency.require(threshold_seconds=3)
def bogosort_array(array):
    while not all(array[i] <= array[i+1] for i in range(len(array)-1)):
        random.shuffle(array)

array = list(reversed(range(10)))
bogosort_array(array)
# TimeoutError: Function 'bogosort_array' expected to have LATENCY_SECONDS to be 3
```
