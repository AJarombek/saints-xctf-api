"""
Test suite for the utility functions for exercise logs (api/src/utils/logs.py)
Author: Andrew Jarombek
Date: 9/2/2020
"""

from tests.TestSuite import TestSuite
from utils.logs import to_miles, calculate_mile_pace


class TestUtilLog(TestSuite):
    def test_miles_to_miles(self) -> None:
        """
        Prove that the conversions to miles from miles works as expected.
        """
        miles = 3.11
        metric = "miles"

        self.assertEqual("3.11", "{0:.2f}".format(to_miles(metric, miles)))

        miles = 0
        metric = "miles"

        self.assertEqual(0, to_miles(metric, miles))

    def test_kilometers_to_miles(self) -> None:
        """
        Prove that the conversions to miles from kilometers works as expected.
        """
        kilometers = 5
        metric = "kilometers"

        self.assertEqual("3.11", "{0:.2f}".format(to_miles(metric, kilometers)))

        kilometers = 0
        metric = "kilometers"

        self.assertEqual(0, to_miles(metric, kilometers))

    def test_meters_to_miles(self) -> None:
        """
        Prove that the conversions to miles from meters works as expected.
        """
        meters = 5000
        metric = "meters"

        self.assertEqual("3.11", "{0:.2f}".format(to_miles(metric, meters)))

        meters = 0
        metric = "meters"

        self.assertEqual(0, to_miles(metric, meters))

    def test_mile_pace_calculation(self) -> None:
        """
        Prove that the mile pace calculation works as expected.
        """
        miles = 4
        time = "28:00"

        self.assertEqual("00:07:00", calculate_mile_pace(miles, time))

        miles = 12.31
        time = "1:25:30"

        self.assertEqual("00:06:56", calculate_mile_pace(miles, time))
