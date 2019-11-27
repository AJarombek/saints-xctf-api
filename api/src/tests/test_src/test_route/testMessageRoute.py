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

    def test_message_post_route_400_empty_body(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/messages/' route.  This test proves that calling this endpoint
        with an empty request body results in a 400 error code.
        """
        response: Response = self.client.post('/v2/messages/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/messages')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('message'))
        self.assertEqual(response_json.get('error'), "the request body isn't populated")

    def test_message_post_route_400_missing_required_field(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/messages/' route.  This test proves that calling this endpoint
        with missing required fields results in a 400 error.
        """
        # Missing the required 'group_name' field
        request_body = json.dumps({
            "username": "andy",
            "first": "Andrew",
            "last": "Jarombek",
            "content": "Test Message",
            "time": str(datetime.now())
        })

        response: Response = self.client.post(
            '/v2/messages/',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/messages')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('message'))
        self.assertEqual(
            response_json.get('error'),
            "'username', 'first', 'last', 'group_name', and 'time' are required fields"
        )

    def test_message_post_route_200(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/messages/' route.  This test proves that calling
        this endpoint with a valid request JSON results in a 200 success code and a new message object.
        """
        request_body = json.dumps({
            "username": "andy",
            "first": "Andrew",
            "last": "Jarombek",
            "group_name": "alumni",
            "content": "Test Message",
            "time": str(datetime.now())
        })

        response: Response = self.client.post(
            '/v2/messages/',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/messages')
        self.assertEqual(response_json.get('added'), True)
        self.assertIsNotNone(response_json.get('message'))
        self.assertIn('message_id', response_json.get('message'))
        self.assertIn('username', response_json.get('message'))
        self.assertIn('first', response_json.get('message'))
        self.assertIn('last', response_json.get('message'))
        self.assertIn('group_name', response_json.get('message'))
        self.assertIn('time', response_json.get('message'))
        self.assertIn('content', response_json.get('message'))
        self.assertIn('deleted', response_json.get('message'))

    def test_message_by_id_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/messages/<message_id>' route.  This test proves that trying to
        retrieve a message with an ID that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get('/v2/messages/0')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/messages/0')
        self.assertIsNone(response_json.get('message'))
        self.assertEqual(response_json.get('error'), 'there is no message with this identifier')

    def test_message_by_id_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/messages/<message_id>' route.  This test proves that retrieving
        a message with a valid ID results in the message and a 200 status.
        """
        response: Response = self.client.get('/v2/messages/2')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/messages/2')
        self.assertIsNotNone(response_json.get('message'))

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
