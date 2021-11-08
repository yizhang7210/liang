import unittest
import liang.latency
import liang.errors
import time
from . import utils


class LatencyRequireTest(unittest.TestCase):

    def test_require_runs_successfully_if_not_timeout(self):
        @liang.latency.require(threshold_seconds=2)
        def test_function():
            return 'output'

        self.assertEqual('output', test_function())

    def test_require_stops_execution_at_time_out(self):

        @liang.latency.require(threshold_seconds=1)
        def test_function():
            time.sleep(2)
            return 'output'

        with self.assertRaises(liang.errors.MetricNotSatisfiedError) as e:
            test_function()

        self.assertTrue('expected to have LATENCY_SECONDS to be 1' in e.exception.message)

    def test_require_not_accept_non_positive_threshold(self):
        with self.assertRaises(ValueError):
            @liang.latency.require(threshold_seconds=-3)
            def test_negative_threshold():
                return 'output'

        with self.assertRaises(ValueError):
            @liang.latency.require(threshold_seconds=0)
            def test_negative_threshold():
                return 'output'

    def test_require_handler_not_called_if_successful(self):
        custom_handler = utils.TestingFailureHandler()

        @liang.latency.require(threshold_seconds=1, handler=custom_handler)
        def test_function():
            return 'output'

        test_function()

        self.assertEqual(0, custom_handler.num_calls)

    def test_require_handler_is_called_if_not_successful(self):
        custom_handler = utils.TestingFailureHandler()

        @liang.latency.require(threshold_seconds=1, handler=custom_handler)
        def test_function():
            time.sleep(2)
            return 'output'

        test_function()

        self.assertEqual(1, custom_handler.num_calls)


