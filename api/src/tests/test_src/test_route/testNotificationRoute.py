"""
Test suite for the API routes that handle user notifications (api/src/route/notificationRoute.py).
Author: Andrew Jarombek
Date: 12/2/2019
"""

import json
from datetime import datetime
from flask import Response
from tests.TestSuite import TestSuite


class TestNotificationRoute(TestSuite):

    def test_notification_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/notifications' route. This route is redirected to
        '/v2/notifications/' by default.
        """
        response: Response = self.client.get('/v2/notifications')
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn('/v2/notifications/', headers.get('Location'))

    def test_notification_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/notifications' route. This route is redirected to
        '/v2/notifications/' by default.
        """
        response: Response = self.client.post('/v2/notifications')
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/notifications/', headers.get('Location'))

    def test_notification_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/notifications/' route.  This test proves that the endpoint
        returns a list of notifications.
        """
        response: Response = self.client.get('/v2/notifications/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/notifications')
        self.assertGreater(len(response_json.get('notifications')), 1)
        self.assertIn('notification_id', response_json.get('notifications')[0])
        self.assertIn('username', response_json.get('notifications')[0])
        self.assertIn('time', response_json.get('notifications')[0])
        self.assertIn('link', response_json.get('notifications')[0])
        self.assertIn('viewed', response_json.get('notifications')[0])
        self.assertIn('description', response_json.get('notifications')[0])
        self.assertIn('deleted', response_json.get('notifications')[0])

    def test_notification_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/notifications/links' route.  This test proves that calling
        this endpoint returns a list of other notification endpoints.
        """
        response: Response = self.client.get('/v2/notifications/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/notifications/links')
        self.assertEqual(len(response_json.get('endpoints')), 6)
