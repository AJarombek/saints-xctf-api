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

    def test_log_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/logs' route. This route is redirected to
        '/v2/logs/' by default.
        """
        response: Response = self.client.post('/v2/logs')
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/logs/', headers.get('Location'))

    def test_log_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/logs/' route.  This test proves that the endpoint returns
        a list of logs.
        """
        response: Response = self.client.get('/v2/logs/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/logs')
        self.assertGreater(len(response_json.get('logs')), 1)

    def test_log_post_route_400_empty_body(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/logs/' route.  This test proves that calling this endpoint
        with an empty request body results in a 400 error code.
        """
        response: Response = self.client.post('/v2/logs/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/logs')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('log'))
        self.assertEqual(response_json.get('error'), "the request body isn't populated")

    def test_log_post_route_400_missing_required_field(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/logs/' route.  This test proves that calling this endpoint
        with missing required fields results in a 400 error.
        """
        # Missing the required 'date' field
        request_body = json.dumps({
            "log_id": 2,
            "username": "andy",
            "first": "Andrew",
            "last": "Jarombek",
            "type": "run",
            "feel": 6,
            "miles": 4.75,
            "time_created": str(datetime.now())
        })

        response: Response = self.client.post(
            '/v2/logs/',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/logs')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('log'))
        self.assertEqual(
            response_json.get('error'),
            "'log_id', 'username', 'first', 'last', 'date', 'type', 'feel', and 'time_created' are required fields"
        )
