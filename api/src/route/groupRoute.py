"""
Group routes in the SaintsXCTF API.  Used for retrieving and updating groups.
Author: Andrew Jarombek
Date: 7/7/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.groupDao import GroupDao

group_route = Blueprint('group_route', __name__, url_prefix='/v2/groups')


@group_route.route('/', methods=['GET'])
def groups():
    if request.method == 'GET':
        ''' [GET] /v2/groups '''
        groups = GroupDao.get_groups()

        if groups is None:
            response = jsonify({
                'self': f'/v2/groups',
                'groups': groups
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': f'/v2/groups',
                'groups': None,
                'error': 'failed to retrieve groups from the database'
            })
            response.status_code = 500
            return response


@group_route.route('/<group_name>', methods=['GET', 'PUT'])
def logs_with_id(group_name):
    if request.method == 'GET':
        ''' [GET] /v2/groups/<group_name> '''
        group = GroupDao.get_group(group_name=group_name)
        
    elif request.method == 'PUT':
        ''' [PUT] /v2/groups/<group_name> '''


@group_route.route('/snapshot/<group_name>', methods=['GET'])
def group_snapshot(group_name):
    pass
