"""
RangeView routes in the SaintsXCTF API.  Used for retrieving log information over a date range.
Author: Andrew Jarombek
Date: 8/3/2019
"""

from flask import Blueprint, request, jsonify, Response
from flasgger import swag_from

from decorators import auth_required
from dao.logDao import LogDao
from utils import exerciseFilters

range_view_route = Blueprint('range_view_route', __name__, url_prefix='/v2/range_view')


@range_view_route.route('/<filter_by>/<bucket>/<exercise_types>/<start>/<end>', methods=['GET'])
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
        ''' [GET] /v2/range_view '''
        return range_view_get(filter_by, bucket, exercise_types, start, end)


@range_view_route.route('/links', methods=['GET'])
@swag_from('swagger/rangeViewRoute/rangeViewLinks.yml', methods=['GET'])
def range_view_links() -> Response:
    """
    Endpoint for information about the range view API endpoints.
    :return: Metadata about the range view API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/range_view/links '''
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
    exercise_type_filter_list = exerciseFilters.create_exercise_filter_list(exercise_types)

    if filter_by == 'group' or filter_by == 'groups':
        range_view = LogDao.get_group_range_view(
            group_id=int(bucket),
            types=exercise_type_filter_list,
            start=start,
            end=end
        )
    elif filter_by == 'user' or filter_by == 'users':
        range_view = LogDao.get_user_range_view(
            username=bucket,
            types=exercise_type_filter_list,
            start=start,
            end=end
        )
    elif filter_by == 'all':
        range_view = LogDao.get_range_view(
            types=exercise_type_filter_list,
            start=start,
            end=end
        )
    else:
        range_view = None

    if range_view is None or range_view.rowcount == 0:
        response = jsonify({
            'self': f'/v2/range_view/{filter_by}/{bucket}/{exercise_types}/{start}/{end}',
            'range_view': [],
            'message': 'no logs found in this date range with the selected filters'
        })
        response.status_code = 200
        return response
    else:
        range_view_list = []
        for item in range_view:
            range_view_list.append({
                'date': item.date,
                'miles': item.miles,
                'feel': item.feel
            })

        response = jsonify({
            'self': f'/v2/range_view/{filter_by}/{bucket}/{exercise_types}/{start}/{end}',
            'range_view': range_view_list
        })
        response.status_code = 200
        return response


def range_view_links_get() -> Response:
    """
    Get all the other range view API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/range_view/links',
        'endpoints': [
            {
                'link': '/v2/range_view/<filter_by>/<bucket>/<exercise_types>/<start>/<end>',
                'verb': 'GET',
                'description': 'Get a list of range view objects based on certain filters.'
            }
        ]
    })
    response.status_code = 200
    return response
