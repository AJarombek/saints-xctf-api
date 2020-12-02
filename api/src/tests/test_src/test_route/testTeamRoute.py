"""
Test suite for the API routes for teams (api/src/route/teamRoute.py).
Author: Andrew Jarombek
Date: 12/1/2020
"""

from flask import Response

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import test_route_auth, AuthVariant


class TestTeamRoute(TestSuite):

    def test_team_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/teams' route. This route is redirected to
        '/v2/teams/' by default.
        """
        response: Response = self.client.get('/v2/teams', headers={'Authorization': 'Bearer j.w.t'})
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn('/v2/teams/', headers.get('Location'))

    def test_team_get_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/teams' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams', AuthVariant.FORBIDDEN)

    def test_team_get_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/teams' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams', AuthVariant.UNAUTHORIZED)

    def test_team_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/teams/' route.  This test proves that the endpoint returns
        a list of teams.
        """
        response: Response = self.client.get('/v2/teams/', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/teams')
        self.assertGreater(len(response_json.get('teams')), 1)

    def test_team_get_all_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/teams/' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams/', AuthVariant.FORBIDDEN)

    def test_team_get_all_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/teams/' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams/', AuthVariant.UNAUTHORIZED)
        
    def test_team_by_name_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/teams/<name>' route.  This test proves that
        trying to retrieve a team with a name that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get('/v2/teams/invalid', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/teams/invalid')
        self.assertIsNone(response_json.get('team'))
        self.assertEqual(response_json.get('error'), 'there is no team with this name')

    def test_team_by_name_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/teams/<name>' route.  This test proves that
        retrieving a team with a valid name results in the team and a 200 status.
        """
        response: Response = self.client.get('/v2/teams/saintsxctf', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/teams/saintsxctf')
        self.assertIsNotNone(response_json.get('team'))

    def test_team_by_name_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/teams/<name>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams/saintsxctf', AuthVariant.FORBIDDEN)

    def test_team_by_name_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/teams/<name>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams/saintsxctf', AuthVariant.UNAUTHORIZED)
