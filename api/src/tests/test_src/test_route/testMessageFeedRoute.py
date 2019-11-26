"""
Test suite for the API routes that handle feeds of team/group messages (api/src/route/messageFeedRoute.py).
Author: Andrew Jarombek
Date: 11/25/2019
"""

import json
from datetime import datetime
from flask import Response
from tests.TestSuite import TestSuite


class TestMessageFeedRoute(TestSuite):

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
