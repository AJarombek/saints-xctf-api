"""
Runner which executes the test suite for my SaintsXCTF API
Author: Andrew Jarombek
Date: 6/22/2019
"""

import unittest
from unittest import TestResult
from src.appTests import AppTests


def run_tests(verbosity: int = 3) -> TestResult:
    """
    Execute Unit tests for the API.
    :param verbosity: Set the verbosity level of the unit test logs.  Defaults to 3.
    """

    # Create the test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test files to the test suite
    suite.addTests(loader.loadTestsFromModule(AppTests))

    # Create a test runner an execute the test suite
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)
