import unittest
import liang.measurement


class MeasurerTest(unittest.TestCase):

    def test_single_point_measurer(self):
        measurer = liang.measurement.SinglePointMeasurer(8)

        measurer.add_data_point(liang.measurement.DataPoint('test', 1.0))
        self.assertEqual(1.0, measurer.get_metric('test'))

        measurer.add_data_point(liang.measurement.DataPoint('test', 2.0))
        self.assertEqual(2.0, measurer.get_metric('test'))

        self.assertEqual(8, measurer.get_metric('does_not_exist'))

    def test_percentile_measurer(self):
        measurer = liang.measurement.PercentileMeasurer(12, percentile=50, max_history=10)

        measurer.add_data_point(liang.measurement.DataPoint('test', 1.0))
        self.assertEqual(1.0, measurer.get_metric('test'))

        measurer.add_data_point(liang.measurement.DataPoint('test', 2.0))
        self.assertEqual(1.5, measurer.get_metric('test'))

        self.assertEqual(12, measurer.get_metric('does_not_exist'))

        for i in range(20):
            measurer.add_data_point(liang.measurement.DataPoint('key', i))

        self.assertEqual(14.5, measurer.get_metric('key'))
