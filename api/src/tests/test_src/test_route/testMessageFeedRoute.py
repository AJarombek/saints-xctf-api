"""
Test suite for the API routes that handle feeds of team/group messages (api/src/route/messageFeedRoute.py).
Author: Andrew Jarombek
Date: 11/25/2019
"""

from flask import Response
from tests.TestSuite import TestSuite


class TestMessageFeedRoute(TestSuite):

    def test_message_feed_get_route_500_prev_none(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/message_feed/' route.  This test proves that the endpoint
        returns a 500 error code if there are no messages that match the query.
        """
        response: Response = self.client.get(
            '/v2/message_feed/group/invalid_group/10/0',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/message_feed/group/invalid_group/10/0')
        self.assertIsNone(response_json.get('next'))
        self.assertIsNone(response_json.get('prev'))
        self.assertIsNone(response_json.get('logs'))
        self.assertEqual(response_json.get('error'), 'no messages found in this feed')

    def test_message_feed_get_route_500_prev_populated(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/log_feed/' route.  This test proves that the endpoint returns
        a 500 error code if there are no messages that match the query.  If the offset is high enough, the 'prev' JSON
        property will still be populated.
        """
        response: Response = self.client.get(
            '/v2/message_feed/group/invalid_group/10/10',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/message_feed/group/invalid_group/10/10')
        self.assertIsNone(response_json.get('next'))
        self.assertEqual(response_json.get('prev'), '/v2/message_feed/group/invalid_group/10/0')
        self.assertIsNone(response_json.get('logs'))
        self.assertEqual(response_json.get('error'), 'no messages found in this feed')

    def test_message_feed_get_route_200_group(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/message_feed/' route.  This test proves that the endpoint
        returns a list of exercise logs that match the user query.
        """
        response: Response = self.client.get(
            '/v2/message_feed/group/mensxc/5/0',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/message_feed/group/mensxc/5/0')
        self.assertEqual(response_json.get('next'), '/v2/message_feed/group/mensxc/5/5')
        self.assertIsNone(response_json.get('prev'))
        self.assertEqual(len(response_json.get('messages')), 5)
        self.assertIn('message_id', response_json.get('messages')[0])
        self.assertIn('username', response_json.get('messages')[0])
        self.assertIn('first', response_json.get('messages')[0])
        self.assertIn('last', response_json.get('messages')[0])
        self.assertIn('group_name', response_json.get('messages')[0])
        self.assertIn('time', response_json.get('messages')[0])
        self.assertIn('content', response_json.get('messages')[0])
        self.assertIn('deleted', response_json.get('messages')[0])

    def test_message_feed_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/message_feed/links' route.  This test proves that calling
        this endpoint returns a list of other message feed endpoints.
        """
        response: Response = self.client.get('/v2/message_feed/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/message_feed/links')
        self.assertEqual(len(response_json.get('endpoints')), 1)
