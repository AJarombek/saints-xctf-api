"""
Test suite for the API routes that handle forgot password codes assigned to a user
(api/src/route/groupRoute.py)
Author: Andrew Jarombek
Date: 11/10/2019
"""

from flask import Response
from tests.TestSuite import TestSuite


class TestGroupRoute(TestSuite):

    def test_group_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups' route. This route is redirected to
        '/v2/groups/' by default.
        """
        response: Response = self.client.get('/v2/groups')
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn('/v2/groups/', headers.get('Location'))

    def test_group_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/' route.  This test proves that the endpoint returns
        a list of groups.
        """
        response: Response = self.client.get('/v2/groups/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/groups')
        self.assertGreater(len(response_json.get('groups')), 1)

    def test_group_by_group_name_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/<group_name>' route.  This test proves that trying to
        retrieve a group with a name that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get('/v2/groups/invalid_group_name')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/groups/invalid_group_name')
        self.assertIsNone(response_json.get('group'))
        self.assertEqual(response_json.get('error'), 'there is no group with this name')

    def test_group_by_group_name_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/<group_name>' route.  This test proves that retrieving
        a group with a valid name results in the group and a 200 status.
        """
        response: Response = self.client.get('/v2/groups/wmenstf')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/groups/wmenstf')
        self.assertIsNotNone(response_json.get('group'))
