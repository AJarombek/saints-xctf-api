"""
Test suite for the API routes that handle range view objects (api/src/route/rangeViewRoute.py).
Author: Andrew Jarombek
Date: 12/7/2019
"""

from flask import Response
from tests.TestSuite import TestSuite


class TestRangeViewRoute(TestSuite):

    def test_range_view_get_route_500_groups(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/range_view/' route.  This test proves that the endpoint
        returns a 500 error code if there is no data that matches the query.
        """
        response: Response = self.client.get(
            '/v2/range_view/groups/invalid_group/r/2019-11-25/2020-01-05',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/range_view/groups/invalid_group/r/2019-11-25/2020-01-05')
        self.assertIsNone(response_json.get('range_view'))
        self.assertEqual(response_json.get('error'), 'no logs found in this date range with the selected filters')

    def test_range_view_get_route_500_users(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/range_view/' route.  This test proves that the endpoint
        returns a 500 error code if there is no data that matches the query.
        """
        response: Response = self.client.get(
            '/v2/range_view/users/invalid_user/rb/2019-11-25/2020-01-05',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/range_view/users/invalid_user/rb/2019-11-25/2020-01-05')
        self.assertIsNone(response_json.get('range_view'))
        self.assertEqual(response_json.get('error'), 'no logs found in this date range with the selected filters')

    def test_range_view_get_route_500_all(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/range_view/' route.  This test proves that the endpoint
        returns a 500 error code if there is no data that matches the query.
        """
        response: Response = self.client.get(
            '/v2/range_view/all/_/rbso/2010-11-25/2011-01-05',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/range_view/all/_/rbso/2010-11-25/2011-01-05')
        self.assertIsNone(response_json.get('range_view'))
        self.assertEqual(response_json.get('error'), 'no logs found in this date range with the selected filters')

    def test_range_view_get_route_200_user(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/range_view/' route.  This test proves that the endpoint
        returns a list of data that matches the user query.
        """
        response: Response = self.client.get(
            '/v2/range_view/users/andy/r/2016-12-01/2016-12-31',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)

        range_view = response_json.get('range_view')
        self.assertEqual(len(range_view), 11)
        self.assertIn('date', range_view[0])
        self.assertIsInstance(range_view[0].get('date'), str)
        self.assertIn('feel', range_view[0])
        self.assertIsInstance(range_view[0].get('feel'), int)
        self.assertIn('miles', range_view[0])
        self.assertIsInstance(range_view[0].get('miles'), float)

    def test_range_view_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/range_view/links' route.  This test proves that calling
        this endpoint returns a list of other range view endpoints.
        """
        response: Response = self.client.get('/v2/range_view/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/range_view/links')
        self.assertEqual(len(response_json.get('endpoints')), 1)
