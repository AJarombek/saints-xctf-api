"""
Test suite for the API routes that handle forgot password codes assigned to a user
(api/src/route/groupRoute.py)
Author: Andrew Jarombek
Date: 11/10/2019
"""

import json
from datetime import datetime
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

    def test_group_by_group_name_put_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<group_name>' route.  This test proves that trying to
        update a group that doesn't exist results in a 400 error.
        """
        response: Response = self.client.put('/v2/groups/invalid_group_name')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/groups/invalid_group_name')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('group'))
        self.assertEqual(response_json.get('error'), 'there is no existing group with this name')

    def test_group_by_group_name_put_route_400_no_update(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<group_name>' route.  This test proves that if the
        updated group is the same as the original group, a 400 error is returned.
        """
        response: Response = self.client.get('/v2/groups/wmenstf')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get('group'))

        request_body = json.dumps(response_json.get('group'))

        response: Response = self.client.put(
            '/v2/groups/wmenstf',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/groups/wmenstf')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('group'))
        self.assertEqual(
            response_json.get('error'),
            'the group submitted is equal to the existing group with the same name'
        )

    def test_group_by_group_name_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<group_name>' route.  This test proves that if a valid
        group JSON is passed to this endpoint, the existing group will be updated and a valid 200 response code
        will be returned.
        """
        request_body = json.dumps({
            "group_name": "alumni",
            "group_title": "Alumni",
            "grouppic": "picture_bytes",
            "grouppic_name": "picture.png",
            "week_start": "sunday",
            "description": f"Updated: {datetime.now()}",
            "deleted": None
        })

        response: Response = self.client.put(
            '/v2/groups/alumni',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/groups/alumni')
        self.assertTrue(response_json.get('updated'))
        self.assertIsNotNone(response_json.get('group'))

    def test_group_members_by_group_name_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/members/<group_name>' route.  This test proves that
        trying to retrieve group members from a group with a group name that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get('/v2/groups/members/invalid_group_name')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/groups/members/invalid_group_name')
        self.assertEqual(response_json.get('group'), '/v2/groups/invalid_group_name')
        self.assertIsNone(response_json.get('group_members'))
        self.assertEqual(response_json.get('error'), 'the group does not exist or there are no members in the group')

    def test_group_members_by_group_name_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/members/<group_name>' route.  This test proves that
        retrieving group members from a group with a valid group name results in the group and a 200 status.
        """
        response: Response = self.client.get('/v2/groups/members/wmenstf')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/groups/members/wmenstf')
        self.assertEqual(response_json.get('group'), '/v2/groups/wmenstf')
        self.assertIsNotNone(response_json.get('group_members'))
        self.assertGreaterEqual(len(response_json.get('group_members')), 1)
        self.assertIn('username', response_json.get('group_members')[0])
        self.assertIn('first', response_json.get('group_members')[0])
        self.assertIn('last', response_json.get('group_members')[0])
        self.assertIn('member_since', response_json.get('group_members')[0])
        self.assertIn('user', response_json.get('group_members')[0])
        self.assertIn('deleted', response_json.get('group_members')[0])
        self.assertIsNotNone(response_json.get('group_members')[0]['username'])
