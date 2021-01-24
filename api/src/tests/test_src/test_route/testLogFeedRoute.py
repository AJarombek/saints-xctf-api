"""
Test suite for the API routes that handle feeds of exercise logs (api/src/route/logFeedRoute.py).
Author: Andrew Jarombek
Date: 11/17/2019
"""

from flask import Response

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import test_route_auth, AuthVariant


class TestLogFeedRoute(TestSuite):

    def test_log_feed_get_route_500_prev_none(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/log_feed/' route.  This test proves that the endpoint returns
        a 500 error code if there are no logs that match the query.
        """
        response: Response = self.client.get(
            '/v2/log_feed/username/invalid_user/10/0',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/log_feed/username/invalid_user/10/0')
        self.assertIsNone(response_json.get('next'))
        self.assertIsNone(response_json.get('prev'))
        self.assertIsNone(response_json.get('logs'))
        self.assertEqual(response_json.get('error'), 'no logs found in this feed')

    def test_log_feed_get_route_500_prev_populated(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/log_feed/' route.  This test proves that the endpoint returns
        a 500 error code if there are no logs that match the query.  If the offset is high enough, the 'prev' JSON
        property will still be populated.
        """
        response: Response = self.client.get(
            '/v2/log_feed/username/invalid_user/10/10',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/log_feed/username/invalid_user/10/10')
        self.assertIsNone(response_json.get('next'))
        self.assertEqual(response_json.get('prev'), '/v2/log_feed/username/invalid_user/10/0')
        self.assertIsNone(response_json.get('logs'))
        self.assertEqual(response_json.get('error'), 'no logs found in this feed')

    def test_log_feed_get_route_200_user(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/log_feed/' route.  This test proves that the endpoint returns
        a list of exercise logs that match the user query.
        """
        response: Response = self.client.get(
            '/v2/log_feed/username/andy/25/100',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/log_feed/username/andy/25/100')
        self.assertEqual(response_json.get('next'), '/v2/log_feed/username/andy/25/125')
        self.assertEqual(response_json.get('prev'), '/v2/log_feed/username/andy/25/75')
        self.assertEqual(len(response_json.get('logs')), 25)

    def test_log_feed_get_route_200_group(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/log_feed/' route.  This test proves that the endpoint returns
        a list of exercise logs that match the group query.
        """
        response: Response = self.client.get(
            '/v2/log_feed/group/5/20/80',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/log_feed/group/5/20/80')
        self.assertEqual(response_json.get('next'), '/v2/log_feed/group/5/20/100')
        self.assertEqual(response_json.get('prev'), '/v2/log_feed/group/5/20/60')
        self.assertEqual(len(response_json.get('logs')), 20)

    def test_log_feed_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/log_feed/' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/log_feed/username/andy/25/100', AuthVariant.FORBIDDEN)

    def test_log_feed_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/log_feed/' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/log_feed/username/andy/25/100', AuthVariant.UNAUTHORIZED)

    def test_log_feed_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/log_feed/links' route.  This test proves that calling
        this endpoint returns a list of other log feed endpoints.
        """
        response: Response = self.client.get('/v2/log_feed/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/log_feed/links')
        self.assertEqual(len(response_json.get('endpoints')), 1)
