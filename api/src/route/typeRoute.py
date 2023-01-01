"""
Exercise type routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 12/8/2022
"""

from typing import List

from flask import Blueprint, Response, request, redirect, url_for, jsonify
from flasgger import swag_from

from dao.typeDao import TypeDao
from model.Type import Type

type_route = Blueprint("type_route", __name__, url_prefix="/v2/types")


@type_route.route("", methods=["GET"])
def types_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'types' to the type routes.
    :return: Response object letting the caller know where to redirect the request to.
    """
    if request.method == "GET":
        """[GET] /v2/types"""
        return redirect(url_for("type_route.types"), code=302)


@type_route.route("/", methods=["GET"])
@swag_from("swagger/typeRoute/typesGet.yml", methods=["GET"])
def types() -> Response:
    """
    Endpoints for searching all the available exercise types.
    :return: JSON representation of a list of types and relevant metadata
    """
    if request.method == "GET":
        """[GET] /v2/types/"""
        return types_get()


@type_route.route("/links", methods=["GET"])
@swag_from("swagger/typeRoute/typeLinks.yml", methods=["GET"])
def type_links() -> Response:
    """
    Endpoint for information about the type API endpoints.
    :return: Metadata about the type API.
    """
    if request.method == "GET":
        """[GET] /v2/types/links"""
        return type_links_get()


def types_get() -> Response:
    """
    Retrieve all the exercise types in the database.
    :return: A response object for the GET API request.
    """
    all_types: List[Type] = TypeDao.get_types()

    if all_types is None:
        response = jsonify(
            {
                "self": "/v2/types/",
                "types": None,
                "error": "an unexpected error occurred retrieving exercise types",
            }
        )
        response.status_code = 500
        return response
    else:
        response = jsonify(
            {
                "self": "/v2/types/",
                "types": [type_info.type for type_info in all_types],
            }
        )
        response.status_code = 200
        return response


def type_links_get() -> Response:
    """
    Get all the other exercise type API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify(
        {
            "self": f"/v2/types/links",
            "endpoints": [
                {
                    "link": "/v2/types",
                    "verb": "GET",
                    "description": "Get all the exercise types in the database.",
                }
            ],
        }
    )
    response.status_code = 200
    return response
