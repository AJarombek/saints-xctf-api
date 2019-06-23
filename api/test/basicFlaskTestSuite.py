"""
Blueprint for a Flask test suite which is extended by other test suites
Author: Andrew Jarombek
Date: 6/22/2019
"""

import unittest
from ..src.app import create_app, db


class BasicFlaskTestSuite(unittest.TestCase):

    def setUp(self) -> None:
        """
        Set up logic for the test suite.  Invoked before unit tests are run.
        """
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        """
        Tear down logic for the test suite.  Invoked after unit tests are run.
        """
        db.session.remove()
        self.app_context.pop()
