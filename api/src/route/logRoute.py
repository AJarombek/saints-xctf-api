"""
Log routes in the SaintsXCTF API.  Used for retrieving, adding, updating, and deleting exercise logs.
Author: Andrew Jarombek
Date: 7/6/2019
"""

from datetime import datetime
from flask import Blueprint, request, jsonify, redirect, url_for, Response
from dao.logDao import LogDao
from dao.commentDao import CommentDao
from model.Log import Log

log_route = Blueprint('log_route', __name__, url_prefix='/v2/logs')


@log_route.route('', methods=['GET', 'POST'])
def logs_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'logs' to the log routes.
    :return: Response object letting the browser know where to redirect the request to.
    """
    if request.method == 'GET':
        ''' [GET] /v2/logs '''
        return redirect(url_for('log_route.logs'), code=302)

    elif request.method == 'POST':
        ''' [POST] /v2/logs '''
        return redirect(url_for('log_route.logs'), code=307)


@log_route.route('/', methods=['GET', 'POST'])
def logs():
    """
    Endpoints for retrieving all the logs and creating new logs.
    :return: JSON representation of exercise logs and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/logs/ '''
        return logs_get()

    elif request.method == 'POST':
        ''' [POST] /v2/logs/ '''
        return logs_post()


@log_route.route('/<log_id>', methods=['GET', 'PUT', 'DELETE'])
def logs_with_id(log_id):
    """
    Endpoints for retrieving a single log, editing an existing log, and deleting a log.
    :param log_id: Unique identifier for a log.
    :return: JSON representation of a log and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/logs/<log_id> '''
        return log_by_id_get(log_id)

    elif request.method == 'PUT':
        ''' [PUT] /v2/logs/<log_id> '''
        return log_by_id_put(log_id)

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/logs/<log_id> '''
        return log_by_id_delete(log_id)


@log_route.route('/soft/<log_id>', methods=['DELETE'])
def log_soft_with_id(log_id) -> Response:
    """
    Endpoints for soft deleting exercise logs.
    :param log_id: Unique identifier for an exercise log.
    :return: JSON representation of logs and relevant metadata.
    """
    if request.method == 'DELETE':
        ''' [DELETE] /v2/logs/soft/<code> '''
        return log_by_id_soft_delete(log_id)


@log_route.route('/links', methods=['GET'])
def log_links() -> Response:
    """
    Endpoint for information about the log API endpoints.
    :return: Metadata about the log API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/logs/links '''
        return log_links_get()


def logs_get() -> Response:
    """
    Retrieve all the exercise logs in the database.
    :return: A response object for the GET API request.
    """
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
            log_comments = CommentDao.get_comments_by_log_id(log.get('log_id'))
            log['comments'] = log_comments

        response = jsonify({
            'self': '/v2/logs',
            'logs': logs
        })
        response.status_code = 200
        return response


def logs_post() -> Response:
    """
    Create a new exercise log.
    :return: A response object for the POST API request.
    """
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


def log_by_id_get(log_id) -> Response:
    """
    Get a single exercise log based on a unique ID.
    :param log_id: The unique identifier for an exercise log.
    :return: A response object for the GET API request.
    """
    log = LogDao.get_log_by_id(log_id)

    if log is None:
        comments = CommentDao.get_comments_by_log_id(log_id)
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
            'comments': None,
            'message': 'failed to retrieve a log with this id'
        })
        response.status_code = 500
        return response


def log_by_id_put(log_id) -> Response:
    """
    Update an existing exercise log based on a unique ID.
    :param log_id: The unique identifier for an exercise log.
    :return: A response object for the PUT API request.
    """
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


def log_by_id_delete(log_id) -> Response:
    """
    Delete an existing exercise log based on a unique ID.
    :param log_id: The unique identifier for an exercise log.
    :return: A response object for the DELETE API request.
    """
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


def log_by_id_soft_delete(log_id) -> Response:
    """
    Soft delete an exercise log based on a unique id.
    :param log_id: Unique identifier for an exercise log.
    :return: A response object for the DELETE API request.
    """
    existing_log: Log = LogDao.get_log_by_id(log_id=log_id)

    if existing_log is None:
        response = jsonify({
            'self': f'/v2/logs/soft/{log_id}',
            'deleted': False,
            'error': 'there is no existing exercise log with this id'
        })
        response.status_code = 400
        return response

    if existing_log.deleted:
        response = jsonify({
            'self': f'/v2/logs/soft/{log_id}',
            'deleted': False,
            'error': 'this exercise log is already soft deleted'
        })
        response.status_code = 400
        return response

    # Update the comment model to reflect the soft delete
    existing_log.deleted = True
    existing_log.deleted_date = datetime.now()
    existing_log.deleted_app = 'api'
    existing_log.modified_date = datetime.now()
    existing_log.modified_app = 'api'

    is_deleted: bool = LogDao.soft_delete_log(existing_log)

    if is_deleted:
        response = jsonify({
            'self': f'/v2/logs/soft/{log_id}',
            'deleted': True,
        })
        response.status_code = 204
        return response
    else:
        response = jsonify({
            'self': f'/v2/logs/soft/{log_id}',
            'deleted': False,
            'error': 'failed to soft delete the log'
        })
        response.status_code = 500
        return response


def log_links_get() -> Response:
    """
    Get all the other log API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/logs/links',
        'endpoints': [
            {
                'link': '/v2/logs',
                'verb': 'GET',
                'description': 'Get all the exercise logs in the database.'
            },
            {
                'link': '/v2/logs',
                'verb': 'POST',
                'description': 'Create a new exercise log.'
            },
            {
                'link': '/v2/logs/<log_id>',
                'verb': 'GET',
                'description': 'Retrieve a single exercise log with a given unique id.'
            },
            {
                'link': '/v2/logs/<log_id>',
                'verb': 'PUT',
                'description': 'Update an exercise log with a given unique id.'
            },
            {
                'link': '/v2/logs/<log_id>',
                'verb': 'DELETE',
                'description': 'Delete a single exercise log with a given unique id.'
            },
            {
                'link': '/v2/logs/soft/<comment_id>',
                'verb': 'DELETE',
                'description': 'Soft delete a single exercise log with a given unique id.'
            }
        ],
    })
    response.status_code = 200
    return response
