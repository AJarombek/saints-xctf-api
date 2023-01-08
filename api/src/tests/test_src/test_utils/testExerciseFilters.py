"""
Test suite for the utility functions for exercise filters (api/src/utils/exerciseFilters.py)
Author: Andrew Jarombek
Date: 1/7/2023
"""

from tests.TestSuite import TestSuite
from utils.exerciseFilters import create_exercise_filter_list


class TestExerciseFiltersLog(TestSuite):
    def test_create_exercise_filter_list(self) -> None:
        """
        Prove that creating exercise filters works as expected.
        """
        self.assertEqual([], create_exercise_filter_list(""))
        self.assertEqual([], create_exercise_filter_list("xyz"))
        self.assertEqual(["run"], create_exercise_filter_list("r"))
        self.assertEqual(["swim", "bike"], create_exercise_filter_list("sb"))
        self.assertEqual(
            [
                "run",
                "other",
                "core",
                "strength",
                "weights",
                "yoga",
                "walk",
                "hike",
                "virtual bike",
                "kayak",
                "canoe",
                "row",
                "stand up paddle",
                "alpine ski",
                "backcountry ski",
                "nordic ski",
                "snowboard",
                "snowshoe",
                "ice skate",
                "roller ski",
                "inline skate",
            ],
            create_exercise_filter_list("ro"),
        )
