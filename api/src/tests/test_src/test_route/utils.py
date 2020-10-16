"""
Utility functions which assist in testing the routes in the Flask application.
Author: Andrew Jarombek
Date: 10/15/2020
"""

from unittest import TestCase
from enum import Enum

from flask import Response
from flask.testing import FlaskClient


class AuthVariant(Enum):
    UNAUTHORIZED = 401, 'Unauthorized'
    FORBIDDEN = 403, 'Forbidden'


def test_route_auth(case: TestCase, client: FlaskClient, verb: str, endpoint: str, variant: AuthVariant) -> None:
    """
    Test making an API call to a route without a proper JWT token in the Authorization header.  This route should
    return a 401/403 HTTP code.
    :param case: Unittest test case from which to make assertions.
    :param client: Flask client for making HTTP requests.
    :param verb: The HTTP verb of the request to make.
    :param endpoint: Path of the endpoint on the API domain.
    :param variant: The condition to test.
    """
    if variant == AuthVariant.FORBIDDEN:
        headers = {'Authorization': ''}
    else:
        headers = {}

    if verb == 'GET':
        response: Response = client.get(endpoint, headers=headers)
    elif verb == 'POST':
        response: Response = client.post(endpoint, headers=headers)
    elif verb == 'PUT':
        response: Response = client.put(endpoint, headers=headers)
    elif verb == 'DELETE':
        response: Response = client.delete(endpoint, headers=headers)
    else:
        case.fail(f"Unexpected HTTP Verb: {verb}")
        return

    expected_code, expected_description = variant.value
    response_json: dict = response.get_json()
    case.assertEqual(expected_code, response.status_code)
    case.assertEqual(expected_description, response_json.get('error_description'))
