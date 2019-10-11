"""
Test suite for the main routes describing the API (api/test_src/test_route/apiRoute.py)
Author: Andrew Jarombek
Date: 6/27/2019
"""

# Thank you for all your support this past week, it helped me so much.
# I hope you are doing well, you are amazing.

from flask import Response
from tests.TestSuite import TestSuite


class TestApiRoute(TestSuite):

    def test_api_route(self) -> None:
        """
        Test performing an HTTP GET request on the '/' route. This is the entry point to the API.
        """
        response: Response = self.client.get('/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self_link'), '/')
        self.assertEqual(response_json.get('api_name'), 'saints-xctf-api')
        self.assertEqual(response_json.get('versions_link'), '/versions')

    def test_versions_route(self) -> None:
        """
        Test performing an HTTP GET request on the '/versions' route. This endpoint displays all the available versions
        of the API.
        """
        response: Response = self.client.get('/versions')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/versions')
        self.assertEqual(response_json.get('version_latest'), '/v2')
        self.assertEqual(response_json.get('version_1'), None)
        self.assertEqual(response_json.get('version_2'), '/v2')

    def test_version2_route(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2' route. This endpoint displays information about the second
        version of the API.
        """
        response: Response = self.client.get('/v2')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2')
        self.assertEqual(response_json.get('version'), 2)
        self.assertEqual(response_json.get('latest'), True)
        self.assertEqual(response_json.get('links'), '/v2/links')

    def test_links_route(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/links' route. This endpoint displays information about the
        top level API links in the second version of the API.
        """
        response: Response = self.client.get('/v2/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/links')
        self.assertEqual(response_json.get('activation_code'), '/v2/activation_code/links')
        self.assertEqual(response_json.get('comment'), '/v2/comments/links')
        self.assertEqual(response_json.get('flair'), '/v2/flair/links')
        self.assertEqual(response_json.get('forgot_password'), '/v2/forgot_password/links')
        self.assertEqual(response_json.get('group'), '/v2/groups/links')
        self.assertEqual(response_json.get('log_feed'), '/v2/log_feed/links')
        self.assertEqual(response_json.get('log'), '/v2/logs/links')
        self.assertEqual(response_json.get('mail'), '/v2/mail/links')
        self.assertEqual(response_json.get('message_feed'), '/v2/message_feed/links')
        self.assertEqual(response_json.get('message'), '/v2/messages/links')
        self.assertEqual(response_json.get('notification'), '/v2/notifications/links')
        self.assertEqual(response_json.get('range_view'), '/v2/range_view/links')
        self.assertEqual(response_json.get('user'), '/v2/users/links')
