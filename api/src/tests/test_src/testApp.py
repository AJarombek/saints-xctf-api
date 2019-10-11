"""
Test suite for the entrypoint to the Flask application (api/test_src/app.py)
Author: Andrew Jarombek
Date: 6/22/2019
"""

import unittest
from flask import current_app
from tests.TestSuite import TestSuite


class TestApp(TestSuite):

    def test_app_exists(self):
        self.assertTrue(current_app is not None)
