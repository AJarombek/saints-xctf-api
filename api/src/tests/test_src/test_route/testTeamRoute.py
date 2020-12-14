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

    def test_team_members_by_team_name_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/teams/members/<team_name>' route.  This test proves that
        trying to retrieve the members of a team that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get('/v2/teams/members/invalid', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/teams/members/invalid')
        self.assertIsNone(response_json.get('team_members'))
        self.assertEqual(response_json.get('error'), 'the team does not exist or it has no members')

    def test_team_members_by_team_name_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/teams/members/<team_name>' route.  This test proves that
        retrieving the members of a valid team results in the members and a 200 status.
        """
        response: Response = self.client.get('/v2/teams/members/saintsxctf', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/teams/members/saintsxctf')
        self.assertIsNotNone(response_json.get('team_members'))
        self.assertGreater(len(response_json.get('team_members')), 0)

    def test_team_members_by_team_name_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/teams/members/<team_name>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams/members/saintsxctf', AuthVariant.FORBIDDEN)

    def test_team_members_by_team_name_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/teams/members/<team_name>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams/members/saintsxctf', AuthVariant.UNAUTHORIZED)

    def test_team_groups_by_team_name_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/teams/groups/<team_name>' route.  This test proves that
        trying to retrieve the groups that are in a team which doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get('/v2/teams/groups/invalid', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/teams/groups/invalid')
        self.assertIsNone(response_json.get('team_groups'))
        self.assertEqual(response_json.get('error'), 'the team does not exist or it has no groups')

    def test_team_groups_by_team_name_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/teams/groups/<team_name>' route.  This test proves that
        retrieving the groups in a valid team results in the group objects and a 200 status.
        """
        response: Response = self.client.get('/v2/teams/groups/saintsxctf', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/teams/groups/saintsxctf')
        self.assertIsNotNone(response_json.get('team_groups'))
        self.assertGreater(len(response_json.get('team_groups')), 0)

    def test_team_groups_by_team_name_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/teams/groups/<team_name>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams/groups/saintsxctf', AuthVariant.FORBIDDEN)

    def test_team_groups_by_team_name_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/teams/groups/<team_name>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams/groups/saintsxctf', AuthVariant.UNAUTHORIZED)

    def test_search_teams_by_team_name_get_route_200_no_matches(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/teams/search/<text>/<limit>' route.  This test proves that
        when the search returns an empty result set, there is an additional message field on the JSON response.  The
        response status code is 200.
        """
        response: Response = self.client.get('/v2/teams/search/invalid/1', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/teams/search/invalid/1')
        self.assertEqual(len(response_json.get('teams')), 0)
        self.assertEqual(response_json.get('message'), 'no teams were found with the provided text')

    def test_search_teams_by_team_name_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/teams/search/<text>/<limit>' route.  This test proves that
        a search which matches teams returns a list of team objects and a 200 status.
        """
        response: Response = self.client.get('/v2/teams/search/saintsxctf/1', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/teams/search/saintsxctf/1')
        self.assertIsNotNone(response_json.get('teams'))
        self.assertEqual(len(response_json.get('teams')), 1)

    def test_search_teams_by_text_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/teams/search/<text>/<limit>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams/search/St/5', AuthVariant.FORBIDDEN)

    def test_search_teams_by_text_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/teams/search/<text>/<limit>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/teams/search/St/5', AuthVariant.UNAUTHORIZED)
