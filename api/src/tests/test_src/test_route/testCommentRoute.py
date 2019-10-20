"""
Test suite for the API routes that handle comments on logs (api/src/route/commentRoute.py)
Author: Andrew Jarombek
Date: 10/11/2019
"""

from flask import Response
from tests.TestSuite import TestSuite


class TestCommentRoute(TestSuite):

    def test_comment_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments' route. This route is redirected to
        '/v2/comments/' by default.
        """
        response: Response = self.client.post('/v2/comments')
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/comments/', headers.get('Location'))

    def test_comment_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/comments' route. This route is redirected to
        '/v2/comments/' by default.
        """
        response: Response = self.client.post('/v2/comments')
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/comments/', headers.get('Location'))

    def test_comment_get_links_route_200(self) -> None:
        response: Response = self.client.get('/v2/comments/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/comments/links')
        self.assertEqual(len(response_json.get('endpoints')), 6)
