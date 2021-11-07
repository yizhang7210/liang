from typing import (
    Callable,
    Optional
)


class ExecutionContext:
    def __init__(self, func: Callable, metric_name: str, metric_expected: float, metric_actual: Optional[float]):
        self.function = func
        self.metric_name = metric_name
        self.metric_expected = metric_expected
        self.metric_actual = metric_actual

