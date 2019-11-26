"""
Test suite for the API routes that handle team/group messages (api/src/route/messageRoute.py).
Author: Andrew Jarombek
Date: 11/26/2019
"""

import json
from datetime import datetime
from flask import Response
from tests.TestSuite import TestSuite


class TestMessageRoute(TestSuite):

    def test_message_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/messages' route. This route is redirected to
        '/v2/messages/' by default.
        """
        response: Response = self.client.get('/v2/messages')
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn('/v2/messages/', headers.get('Location'))

    def test_message_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/messages' route. This route is redirected to
        '/v2/messages/' by default.
        """
        response: Response = self.client.post('/v2/messages')
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/messages/', headers.get('Location'))

    def test_message_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/messages/' route.  This test proves that the endpoint returns
        a list of messages.
        """
        response: Response = self.client.get('/v2/messages/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/messages')
        self.assertGreater(len(response_json.get('messages')), 1)
        self.assertIn('message_id', response_json.get('messages')[0])
        self.assertIn('username', response_json.get('messages')[0])
        self.assertIn('first', response_json.get('messages')[0])
        self.assertIn('last', response_json.get('messages')[0])
        self.assertIn('group_name', response_json.get('messages')[0])
        self.assertIn('time', response_json.get('messages')[0])
        self.assertIn('content', response_json.get('messages')[0])
        self.assertIn('deleted', response_json.get('messages')[0])

    def test_message_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/messages/links' route.  This test proves that calling
        this endpoint returns a list of other message endpoints.
        """
        response: Response = self.client.get('/v2/messages/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/messages/links')
        self.assertEqual(len(response_json.get('endpoints')), 6)
