"""
Log routes in the SaintsXCTF API.  Used for retrieving, adding, updating, and deleting exercise logs.
Author: Andrew Jarombek
Date: 7/6/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.logDao import LogDao
from dao.commentDao import CommentDao

log_route = Blueprint('log_route', __name__, url_prefix='/v2/logs')


@log_route.route('/', methods=['GET', 'POST'])
def logs():
    if request.method == 'GET':
        ''' [GET] /v2/logs '''
        logs = LogDao.get_logs()

        if logs is None:
            response = jsonify({
                'self': f'/v2/logs',
                'logs': None,
                'error': 'an unexpected error occurred retrieving logs'
            })
            response.status_code = 500
            return response
        else:
            for log in logs:
                log_comments = CommentDao.get_comment_by_log_id(log.get('log_id'))
                log['comments'] = log_comments

            response = jsonify({
                'self': f'/v2/logs',
                'logs': logs
            })
            response.status_code = 200
            return response

    elif request.method == 'POST':
        ''' [POST] /v2/logs '''


@log_route.route('/<log_id>', methods=['GET', 'PUT', 'DELETE'])
def logs(log_id):
    if request.method == 'GET':
        ''' [GET] /v2/logs/<log_id> '''
        log = LogDao.get_log_by_id(log_id)

        if log is None:
            comments = CommentDao.get_comment_by_log_id(log_id)
            response = jsonify({
                'self': f'/v2/logs/{log_id}',
                'log': log,
                'comments': comments
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': f'/v2/logs/{log_id}',
                'log': None,
                'comments': None
            })
            response.status_code = 500
            return response

    elif request.method == 'POST':
        ''' [PUT] /v2/logs/<log_id> '''
    elif request.method == 'DELETE':
        ''' [DELETE] /v2/logs/<log_id> '''
