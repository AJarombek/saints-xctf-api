"""
Log routes in the SaintsXCTF API.  Used for retrieving, adding, updating, and deleting exercise logs.
Author: Andrew Jarombek
Date: 7/6/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.logDao import LogDao
from dao.commentDao import CommentDao
from model.Log import Log

log_route = Blueprint('log_route', __name__, url_prefix='/v2/logs')


@log_route.route('/', methods=['GET', 'POST'])
def logs():
    if request.method == 'GET':
        ''' [GET] /v2/logs '''
        logs = LogDao.get_logs()

        if logs is None:
            response = jsonify({
                'self': '/v2/logs',
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
                'self': '/v2/logs',
                'logs': logs
            })
            response.status_code = 200
            return response

    elif request.method == 'POST':
        ''' [POST] /v2/logs '''
        log_data: dict = request.get_json()
        log_to_add = Log(log_data)
        log_added_successfully = LogDao.add_log(new_log=log_to_add)

        if log_added_successfully:
            log_added = LogDao.get_log_by_id(log_id=log_to_add.log_id)

            response = jsonify({
                'self': '/v2/logs',
                'added': True,
                'log': log_added
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': '/v2/logs',
                'added': False,
                'log': None,
                'error': 'failed to create a new log'
            })
            response.status_code = 500
            return response


@log_route.route('/<log_id>', methods=['GET', 'PUT', 'DELETE'])
def logs_with_id(log_id):
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

    elif request.method == 'PUT':
        ''' [PUT] /v2/logs/<log_id> '''
        old_log = LogDao.get_log_by_id(log_id=log_id)

        if old_log is None:
            response = jsonify({
                'self': f'/v2/logs/{log_id}',
                'updated': False,
                'log': None,
                'error': 'there is no existing log with this id'
            })
            response.status_code = 400
            return response

        log_data: dict = request.get_json()
        new_log = Log(log_data)

        if old_log != new_log:
            is_updated = LogDao.update_log(new_log)

            if is_updated:
                updated_log = LogDao.get_log_by_id(log_id=new_log.log_id)

                response = jsonify({
                    'self': f'/v2/logs/{log_id}',
                    'updated': True,
                    'log': updated_log
                })
                response.status_code = 200
                return response
            else:
                response = jsonify({
                    'self': f'/v2/logs/{log_id}',
                    'updated': False,
                    'log': None,
                    'error': 'the log failed to update'
                })
                response.status_code = 500
                return response

        else:
            response = jsonify({
                'self': f'/v2/logs/{log_id}',
                'updated': False,
                'log': None,
                'error': 'the log submitted is equal to the existing log with the same id'
            })
            response.status_code = 400
            return response

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/logs/<log_id> '''
        are_comments_deleted = CommentDao.delete_comments_by_log_id(log_id=log_id)

        if not are_comments_deleted:
            response = jsonify({
                'self': f'/v2/logs/{log_id}',
                'deleted': False,
                'error': 'failed to delete the comments on this log'
            })
            response.status_code = 500
            return response

        is_log_deleted = LogDao.delete_log(log_id=log_id)

        if is_log_deleted:
            response = jsonify({
                'self': f'/v2/logs/{log_id}',
                'deleted': True,
            })
            response.status_code = 204
            return response
        else:
            response = jsonify({
                'self': f'/v2/logs/{log_id}',
                'deleted': False,
                'error': 'failed to delete the log'
            })
            response.status_code = 500
            return response
