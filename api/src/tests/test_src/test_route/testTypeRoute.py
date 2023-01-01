"""
Test suite for the API routes for exercise types (api/src/route/typeRoute.py).
Author: Andrew Jarombek
Date: 12/31/2022
"""

from flask import Response

from tests.TestSuite import TestSuite


class TestTypeRoute(TestSuite):
    def test_types_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/types' route. This route is redirected to
        '/v2/types/' by default.
        """
        response: Response = self.client.get("/v2/types")
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn("/v2/types/", headers.get("Location"))

    def test_types_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/types' route.  This test proves that
        the endpoint returns a list of exercise types and a 200 status.
        """
        response: Response = self.client.get("/v2/types/")
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/types/")
        self.assertIsNotNone(response_json.get("types"))
        self.assertEqual(len(response_json.get("types")), 4)
        self.assertIsInstance(response_json.get("types")[0], str)

    def test_types_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/types/links' route.  This test proves that calling
        this endpoint returns a list of other exercise type endpoints.
        """
        response: Response = self.client.get("/v2/types/links")
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/types/links")
        self.assertEqual(len(response_json.get("endpoints")), 1)
