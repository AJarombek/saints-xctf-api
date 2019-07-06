"""
Log routes in the SaintsXCTF API.  Used for retrieving, adding, updating, and deleting exercise logs.
Author: Andrew Jarombek
Date: 7/6/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.logDao import LogDao

log_route = Blueprint('log_route', __name__, url_prefix='/v2/logs')


@log_route.route('/', methods=['GET', 'POST'])
def logs():
    if request.method == 'GET':
        ''' [GET] /v2/logs '''
    elif request.method == 'POST':
        ''' [POST] /v2/logs '''


@log_route.route('/<log_id>', methods=['GET', 'PUT', 'DELETE'])
def logs(log_id):
    if request.method == 'GET':
        ''' [GET] /v2/logs/<log_id> '''
        log = LogDao.get_log_by_id(log_id)

        if log is None:
            pass
        else:
            pass
        
    elif request.method == 'POST':
        ''' [PUT] /v2/logs/<log_id> '''
    elif request.method == 'DELETE':
        ''' [DELETE] /v2/logs/<log_id> '''
