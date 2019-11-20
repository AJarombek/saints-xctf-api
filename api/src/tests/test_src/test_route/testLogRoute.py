"""
Test suite for the API routes that handle exercise logs (api/src/route/logRoute.py).
Author: Andrew Jarombek
Date: 11/17/2019
"""

import json
from datetime import datetime
from flask import Response
from tests.TestSuite import TestSuite


class TestLogRoute(TestSuite):

    def test_log_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/logs' route. This route is redirected to
        '/v2/logs/' by default.
        """
        response: Response = self.client.get('/v2/logs')
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn('/v2/logs/', headers.get('Location'))

    def test_comment_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/logs' route. This route is redirected to
        '/v2/logs/' by default.
        """
        response: Response = self.client.post('/v2/logs')
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/logs/', headers.get('Location'))
