import unittest
import liang.latency
import liang.errors
import time
from . import utils


class LatencyRecommendTest(unittest.TestCase):

    def test_recommend_runs_successfully_if_not_timeout(self):
        @liang.latency.recommend(threshold_seconds=2)
        def test_function():
            return 'output'

        self.assertEqual('output', test_function())

    def test_recommend_runs_to_completion_if_time_out(self):

        @liang.latency.recommend(threshold_seconds=1)
        def test_function():
            time.sleep(2)
            return 'output'

        self.assertEqual('output', test_function())

    def test_recommend_not_accept_non_positive_threshold(self):
        with self.assertRaises(ValueError):
            @liang.latency.recommend(threshold_seconds=-3)
            def test_negative_threshold():
                return 'output'

        with self.assertRaises(ValueError):
            @liang.latency.recommend(threshold_seconds=0)
            def test_negative_threshold():
                return 'output'

    def test_recommend_handler_not_called_if_under_threshold(self):
        custom_handler = utils.TestingFailureHandler()

        @liang.latency.recommend(threshold_seconds=1, handler=custom_handler)
        def test_function():
            return 'output'

        test_function()

        self.assertEqual(0, custom_handler.num_calls)

    def test_recommend_handler_is_called_if_over_threshold(self):
        custom_handler = utils.TestingFailureHandler()

        @liang.latency.recommend(threshold_seconds=1, handler=custom_handler)
        def test_function():
            time.sleep(2)
            return 'output'

        test_function()

        self.assertEqual(1, custom_handler.num_calls)

    def test_recommend_custom_measurer_is_respected(self):
        custom_handler = utils.TestingFailureHandler()
        custom_measurer = utils.TestingMeasurer()

        @liang.latency.recommend(threshold_seconds=1, handler=custom_handler, measurer=custom_measurer)
        def test_function():
            time.sleep(1)
            return 'output'

        test_function()
        test_function()
        test_function()

        self.assertEqual(3, custom_measurer.get_metric('test_function'))
        self.assertAlmostEqual(3.00, sum([d.value for d in custom_measurer.data_points]), delta=0.05)
