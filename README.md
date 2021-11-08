# liang
Specify non-functional requirements in your Python code.

## Installation
``` shell script
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
If the function takes longer than `threshold_seconds`, a warning will be logged by default.
"""

@liang.latency.require(threshold_seconds=3, handler=CustomHandler)
@liang.latency.recommend(threshold_seconds=3, handler=CustomHandler)
"""
Can specify CustomHandler to handle when a function exceeds `threshold_seconds`.
CustomHandler needs to inherit from liang.handlers.FailureHandler and implement the
`.handle(self, context: environment.ExecutionContext)` method.
"""

@liang.latency.recommend(threshold_seconds=3, measurer=CustomMeasurer)
"""
Can specify CustomMeasurer to calculate the latency metric.
For example the measurer can calculate the average of previous `n` runs, and only
enters the handler if the average is over the threshold.
"""

```

### Handlers
Liang provides the following handlers out of the box.
``` python
RaiseExceptionFailureHandler  # raise a MetricNotSatisfiedError
LogWarningFailureHandler      # logs a warning message
```

### Measurers
Liang provides the following measurers out of the box.
``` python
SinglePointMeasurer(default_value: float)
"""
Simply returns the latest value by key, or default_value.
"""

PercentileMeasurer(default_value: float, percentile: int, max_history: int = 100)
"""
Accumulates `max_history` values by key, and return the `percentile`th percentile over
the stored history.

Returns `default_value` if the key does not have any data points.
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

If we want to log a warning when the 80th percentile of up to 10 previous runs of a function is longer than 2 seconds:
``` python
import liang.measurement
import time

custom_measurer = liang.measurement.PercentileMeasurer(0, percentile=80, max_history=10)

@liang.latency.recommend(threshold_seconds=2, measurer=custom_measurer)
def test_function(sleep_time):
    time.sleep(sleep_time)


for i in range(5):
    test_function(i)

# You should see the following logs:
# INFO:liang.latency:Function 'test_function'(0) starting execution.
# INFO:liang.latency:Function 'test_function'(0) finished in 0.0000 seconds.
# INFO:liang.latency:Function 'test_function'(1) starting execution.
# INFO:liang.latency:Function 'test_function'(1) finished in 1.0024 seconds.
# INFO:liang.latency:Function 'test_function'(2) starting execution.
# INFO:liang.latency:Function 'test_function'(2) finished in 2.0024 seconds.
# INFO:liang.latency:Function 'test_function'(3) starting execution.
# INFO:liang.latency:Function 'test_function'(3) finished in 3.0006 seconds.
# WARNING:liang.handlers:Function 'test_function' expected to have LATENCY_SECONDS to be 2 but is actually 2.40
# INFO:liang.latency:Function 'test_function'(4) starting execution.
# INFO:liang.latency:Function 'test_function'(4) finished in 4.0026 seconds.
# WARNING:liang.handlers:Function 'test_function' expected to have LATENCY_SECONDS to be 2 but is actually 3.20
```


