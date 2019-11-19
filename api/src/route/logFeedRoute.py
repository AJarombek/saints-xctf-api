"""
LogFeed routes in the SaintsXCTF API.  Used for retrieving multiple exercise logs.
Author: Andrew Jarombek
Date: 7/10/2019
"""

from flask import Blueprint, request, jsonify, Response
from sqlalchemy.engine import ResultProxy
from model.CommentData import CommentData
from dao.logDao import LogDao
from dao.commentDao import CommentDao

log_feed_route = Blueprint('log_feed_route', __name__, url_prefix='/v2/log_feed')


@log_feed_route.route('/<filter_by>/<bucket>/<limit>/<offset>', methods=['GET'])
def log_feed(filter_by, bucket, limit, offset):
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
        return log_feed_get(filter_by, bucket, limit, offset)


@log_feed_route.route('/links', methods=['GET'])
def log_feed_links() -> Response:
    """
    Endpoint for information about the log feed API endpoints.
    :return: Metadata about the log feed API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/log_feed/links '''
        return log_feed_links_get()


def log_feed_get(filter_by, bucket, limit, offset) -> Response:
    """
    Get a list of exercise logs based on certain filters.
    :param filter_by: The filtering mechanism for the exercise logs.
    You can filter by user (username) or group (group_name).
    :param bucket: The bucket to filter by (either a username or a group name)
    :param limit: The maximum number of logs to return
    :param offset: The number of logs to skip from the results of this filter before returning
    :return: A response object for the GET API request.
    """
    logs: ResultProxy = None
    limit = int(limit)
    offset = int(offset)

    if filter_by == 'group' or filter_by == 'groups' or filter_by == 'groupname':
        logs = LogDao.get_group_log_feed(group_name=bucket, limit=limit, offset=offset)
    elif filter_by == 'user' or filter_by == 'users' or filter_by == 'username':
        logs = LogDao.get_user_log_feed(username=bucket, limit=limit, offset=offset)
    elif filter_by == 'all':
        logs = LogDao.get_log_feed(limit=limit, offset=offset)

    # Generate LogFeed API URLs
    self_url = f'/v2/log_feed/{filter_by}/{bucket}/{limit}/{offset}'

    prev_offset = offset - limit
    if prev_offset >= 0:
        prev_url = f'/v2/log_feed/{filter_by}/{bucket}/{limit}/{prev_offset}'
    else:
        prev_url = None

    if logs is None or logs.rowcount == 0:
        response = jsonify({
            'self': self_url,
            'next': None,
            'prev': prev_url,
            'logs': None,
            'error': 'no logs found in this feed'
        })
        response.status_code = 500
        return response
    else:

        log_list = []
        for log in logs:
            comments: list = CommentDao.get_comments_by_log_id(log.log_id)
            comments = [CommentData(comment).__dict__ for comment in comments]

            log_list.append({
                'log_id': log.log_id,
                'username': log.username,
                'first': log.first,
                'last': log.last,
                'name': log.name,
                'location': log.location,
                'date': log.date,
                'type': log.type,
                'distance': log.distance,
                'metric': log.metric,
                'miles': log.miles,
                'time': log.time,
                'pace': log.pace,
                'feel': log.feel,
                'description': log.description,
                'comments': comments
            })

        next_url = f'/v2/log_feed/{filter_by}/{bucket}/{limit}/{offset + limit}'

        response = jsonify({
            'self': self_url,
            'next': next_url,
            'prev': prev_url,
            'logs': log_list
        })
        response.status_code = 200
        return response


def log_feed_links_get() -> Response:
    """
    Get all the other log feed API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/log_feed/links',
        'endpoints': [
            {
                'link': '/v2/log_feed/<filter_by>/<bucket>/<limit>/<offset>',
                'verb': 'GET',
                'description': 'Get a list of exercise logs based on certain filters.'
            }
        ]
    })
    response.status_code = 200
    return response
