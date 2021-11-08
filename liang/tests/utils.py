from typing import List

import liang.handlers
import liang.environment
import liang.measurement
import logging

from liang.measurement import DataPoint

logger = logging.getLogger(__name__)


class TestingFailureHandler(liang.handlers.FailureHandler):

    def __init__(self):
        self.num_calls = 0

    def handle(self, context: liang.environment.ExecutionContext):
        self.num_calls += 1
        logger.info("TestingFailureHandler::handle()")


class TestingMeasurer(liang.measurement.Measurer):

    def __init__(self):
        self.data_points: List[DataPoint] = []

    def add_data_point(self, data_point: DataPoint):
        self.data_points.append(data_point)

    def get_metric(self, key) -> float:
        return len(self.data_points)
