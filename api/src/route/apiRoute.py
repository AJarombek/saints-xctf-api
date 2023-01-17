"""
Global routes in the SaintsXCTF API.  Used for retrieving information about the API.
Author: Andrew Jarombek
Date: 6/21/2019
"""

from flask import Blueprint, jsonify, Response, abort
from flasgger import swag_from

api_route = Blueprint("api_route", __name__, url_prefix="/")


@api_route.route("/", methods=["GET"])
@swag_from("swagger/apiRoute/api.yml")
def api() -> Response:
    """
    Entry point for the SaintsXCTF API
    :return: A JSON welcome message
    """
    return jsonify(
        {"self_link": "/", "api_name": "saints-xctf-api", "versions_link": "/versions"}
    )


@api_route.route("/versions", methods=["GET"])
@swag_from("swagger/apiRoute/versions.yml")
def versions() -> Response:
    """
    Endpoint to get all versions of the SaintsXCTF API
    :return: A JSON with links to API versions
    """
    return jsonify(
        {
            "self": "/versions",
            "version_latest": "/v2",
            "version_1": None,
            "version_2": "/v2",
        }
    )


@api_route.route("/v2", methods=["GET"])
@swag_from("swagger/apiRoute/v2.yml")
def version2() -> Response:
    """
    Endpoint for information about the second version of the SaintsXCTF API
    :return: A JSON with details about the second version of the API
    """
    return jsonify({"self": "/v2", "version": 2, "latest": True, "links": "/v2/links"})


@api_route.route("/v2/links", methods=["GET"])
@swag_from("swagger/apiRoute/v2Links.yml")
def links() -> Response:
    """
    Endpoint for links to endpoints in the second version of the SaintsXCTF API
    :return: A JSON with links in the second version of the API
    """
    return jsonify(
        {
            "self": "/v2/links",
            "activation_code": "/v2/activation_code/links",
            "comment": "/v2/comments/links",
            "flair": "/v2/flair/links",
            "forgot_password": "/v2/forgot_password/links",
            "group": "/v2/groups/links",
            "log_feed": "/v2/log_feed/links",
            "log": "/v2/logs/links",
            "notification": "/v2/notifications/links",
            "range_view": "/v2/range_view/links",
            "team": "/v2/teams/links",
            "user": "/v2/users/links",
        }
    )


@api_route.route("/404", methods=["GET"])
@swag_from("swagger/apiRoute/404.yml")
def error404() -> Response:
    """
    Route for testing the logic of 404 HTTP errors.
    :return: Custom error handling JSON.
    """
    abort(404)


@api_route.route("/500", methods=["GET"])
@swag_from("swagger/apiRoute/500.yml")
def error500() -> Response:
    """
    Route for testing the logic of 500 HTTP errors.
    :return: Custom error handling JSON.
    """
    raise Exception
