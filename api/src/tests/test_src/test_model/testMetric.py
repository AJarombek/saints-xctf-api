"""
Test suite for the model representing a distance metric (api/src/model/Metric.py)
Author: Andrew Jarombek
Date: 11/21/2019
"""

from tests.TestSuite import TestSuite
from model.Metric import Metric


class TestMetric(TestSuite):
    metric1_dict = {'metric': 'meters'}
    metric2_dict = {'metric': 'miles'}
    metric3_dict = {'metric': 'kilometers'}

    metric1 = Metric(metric1_dict)
    metric1copy = Metric(metric1_dict)

    metric2 = Metric(metric2_dict)
    metric3 = Metric(metric3_dict)

    def test_metric_str(self) -> None:
        """
        Prove that the human readable string representation of a Metric object is as expected.
        """
        metric_str = 'Metric: [metric: meters]'

        self.assertEquals(str(self.metric1), metric_str)
        self.assertEquals(self.metric1.__str__(), metric_str)

    def test_metric_repr(self) -> None:
        """
        Prove that the machine readable string representation of a Metric object is as expected.
        """
        self.assertEquals(repr(self.metric2), "<Metric 'miles'>")
        self.assertEquals(self.metric2.__repr__(), "<Metric 'miles'>")

    def test_metric_eq(self) -> None:
        """
        Prove that two Metric objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.metric1 == self.metric1copy)
        self.assertTrue(self.metric1.__eq__(self.metric1copy))

    def test_metric_ne(self) -> None:
        """
        Prove that two Metric objects with different property values test negative for value equality.
        """
        self.assertTrue(self.metric1 != self.metric3)
        self.assertTrue(self.metric1.__ne__(self.metric3))
