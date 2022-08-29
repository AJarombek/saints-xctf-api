"""
RangeView routes in the demo version of the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/12/2022
"""

from flask import Blueprint, request, jsonify, Response
from flasgger import swag_from

from decorators import auth_required
from route.common.rangeView import range_view_links
from route.common.versions import APIVersion

range_view_demo_route = Blueprint('range_view_demo_route', __name__, url_prefix='/demo/range_view')


@range_view_demo_route.route('/<filter_by>/<bucket>/<exercise_types>/<start>/<end>', methods=['GET'])
@auth_required()
@swag_from('swagger/rangeViewRoute/rangeViewGet.yml', methods=['GET'])
def range_view(filter_by, bucket, exercise_types, start, end):
    """
    Endpoint for retrieving log information based on filters and a date range.
    :param filter_by: The first filtering mechanism for the logs in the feed.  You can filter by group (group_name)
    or user (username).
    :param bucket: The bucket to filter by (the group name or username).
    :param exercise_types: A string representing the types of exercises to include in the feed.
    :param start: The first date to include in the exercise log feed.
    :param end: The last date to include in the exercise log feed.
    :return: JSON representation of a log feed and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /demo/range_view '''
        return range_view_get(filter_by, bucket, exercise_types, start, end)


@range_view_demo_route.route('/links', methods=['GET'])
@swag_from('swagger/rangeViewRoute/rangeViewLinks.yml', methods=['GET'])
def range_view_links() -> Response:
    """
    Endpoint for information about the range view API endpoints.
    :return: Metadata about the range view API.
    """
    if request.method == 'GET':
        ''' [GET] /demo/range_view/links '''
        return range_view_links_get()


def range_view_get(filter_by, bucket, exercise_types, start, end) -> Response:
    """
    Get a list of range view objects based on certain filters.
    :param filter_by: The first filtering mechanism for the logs in the feed.  You can filter by group (group_name)
    or user (username).
    :param bucket: The bucket to filter by (the group name or username).
    :param exercise_types: A string representing the types of exercises to include in the feed.
    :param start: The first date to include in the exercise log feed.
    :param end: The last date to include in the exercise log feed.
    :return: A response object for the GET API request.
    """
    response = jsonify({
        'self': f'/demo/range_view/{filter_by}/{bucket}/{exercise_types}/{start}/{end}',
        'range_view': []
    })
    response.status_code = 200
    return response


def range_view_links_get() -> Response:
    """
    Get all the other range view API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify(range_view_links(APIVersion.demo.value))
    response.status_code = 200
    return response
