import abc
import collections
from typing import (
    Dict,
    Optional
)

import numpy as np


class DataPoint:
    def __init__(self, key: str, value: float):
        self.key = key
        self.value = value

    def __str__(self):
        return f'datapoint:{self.key}={self.value}'

    def __repr__(self):
        return f'datapoint:{self.key}={self.value}'


class Measurer(abc.ABC):
    @abc.abstractmethod
    def add_data_point(self, data_point: DataPoint):
        pass

    @abc.abstractmethod
    def get_metric(self, key) -> float:
        pass


class SinglePointMeasurer(Measurer):

    def __init__(self, default_value: float):
        self.default_value = default_value
        self.data_map = {}

    def add_data_point(self, data_point: DataPoint):
        self.data_map[data_point.key] = data_point.value

    def get_metric(self, key) -> float:
        return self.data_map.get(key, self.default_value)


class PercentileMeasurer(Measurer):

    def __init__(self, default_value: float, percentile: int, max_history: int = 100):
        self.default_value = default_value
        self.percentile = percentile
        self.max_history = max_history
        self.history_map: Dict[str, collections.deque] = {}

    def add_data_point(self, data_point: DataPoint):
        if data_point.key not in self.history_map:
            self.history_map[data_point.key] = collections.deque(maxlen=self.max_history)

        self.history_map[data_point.key].appendleft(data_point.value)

    def get_metric(self, key) -> float:
        if key not in self.history_map:
            return self.default_value

        return np.percentile(self.history_map[key], self.percentile)
