"""
RangeView routes in the SaintsXCTF API.  Used for retrieving log information over a date range.
Author: Andrew Jarombek
Date: 8/3/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.logDao import LogDao

range_view_route = Blueprint('range_view_route', __name__, url_prefix='/v2/rangeview')


@range_view_route.route('/<filter_by>/<bucket>/<exercise_types>/<start>/<end>', methods=['GET'])
def messages(filter_by, bucket, exercise_types, start, end):
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
        ''' [GET] /v2/rangeview '''
        if filter_by == 'group' or filter_by == 'groups':
            range_view = LogDao.get_group_range_view(group_name=bucket, types=exercise_types, start=start, end=end)
        elif filter_by == 'user' or filter_by == 'users':
            range_view = LogDao.get_user_range_view(username=bucket, types=exercise_types, start=start, end=end)
        elif filter_by == 'all':
            range_view = LogDao.get_range_view(types=exercise_types, start=start, end=end)
        else:
            range_view = None
