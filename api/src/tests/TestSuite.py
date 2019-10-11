"""
Blueprint for a Flask test suite which is extended by other test suites
Author: Andrew Jarombek
Date: 6/22/2019
"""

import unittest
from flask.testing import FlaskClient
from app import create_app
from database import db


class TestSuite(unittest.TestCase):

    def setUp(self) -> None:
        """
        Set up logic for the test suite.  Invoked before unit tests are run.
        """
        self.app = create_app('local')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client: FlaskClient = self.app.test_client()

    def tearDown(self) -> None:
        """
        Tear down logic for the test suite.  Invoked after unit tests are run.
        """
        db.session.remove()
        self.app_context.pop()
