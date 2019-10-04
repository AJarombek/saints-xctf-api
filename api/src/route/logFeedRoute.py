"""
LogFeed routes in the SaintsXCTF API.  Used for retrieving multiple exercise logs.
Author: Andrew Jarombek
Date: 7/10/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.logDao import LogDao
from dao.commentDao import CommentDao

log_feed_route = Blueprint('log_feed_route', __name__, url_prefix='/v2/log_feed')


@log_feed_route.route('/<filter_by>/<bucket>/<limit>/<offset>', methods=['GET'])
def logs(filter_by, bucket, limit, offset):
    """
    Endpoints for retrieving exercise logs based on filters.
    :param filter_by: The filtering mechanism for the exercise logs.
    You can filter by user (username) or group (group_name).
    :param bucket: The bucket to filter by (either a username or a group name)
    :param limit: The maximum number of logs to return
    :param offset: The number of logs to skip from the results of this filter before returning
    :return: JSON representation of exercise logs and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/log_feed '''
        if filter_by == 'group' or filter_by == 'groups':
            logs = LogDao.get_group_log_feed(group_name=bucket, limit=limit, offset=offset)
        elif filter_by == 'user' or filter_by == 'users':
            logs = LogDao.get_user_log_feed(username=bucket, limit=limit, offset=offset)
        elif filter_by == 'all':
            logs = LogDao.get_log_feed(limit=limit, offset=offset)
        else:
            logs = None

        # Generate LogFeed API URLs
        self_url = f'/v2/log_feed/{filter_by}/{bucket}/{limit}/{offset}'

        prev_offset = (offset - limit) >= 0
        if prev_offset:
            prev_url = f'/v2/log_feed/{filter_by}/{bucket}/{limit}/{prev_offset}'
        else:
            prev_url = None

        if logs is None:
            next_url = None

            response = jsonify({
                'self': self_url,
                'next': next_url,
                'prev': prev_url,
                'logs': None,
                'error': 'no logs found in this feed'
            })
            response.status_code = 500
            return response
        else:

            for log in logs:
                comments = CommentDao.get_comments_by_log_id(log.get('log_id'))
                log.comments = comments

            next_url = f'/v2/log_feed/{filter_by}/{bucket}/{limit}/{offset + limit}'

            response = jsonify({
                'self': self_url,
                'next': next_url,
                'prev': prev_url,
                'logs': logs
            })
            response.status_code = 200
            return response
