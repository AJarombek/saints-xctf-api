"""
Group routes in the SaintsXCTF API.  Used for retrieving and updating groups.
Author: Andrew Jarombek
Date: 7/7/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.groupDao import GroupDao
from dao.groupMemberDao import GroupMemberDao

group_route = Blueprint('group_route', __name__, url_prefix='/v2/groups')


@group_route.route('/', methods=['GET'])
def groups():
    """
    Endpoints for retrieving all the groups.
    :return: JSON representation of groups and relevant metadata.
    """
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
def group(group_name):
    """
    Endpoints for retrieving a single group and updating an existing group.
    :param group_name: Unique name which identifies a group.
    :return: JSON representation of a group and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/<group_name> '''
        group = GroupDao.get_group(group_name=group_name)

        if group is None:
            response = jsonify({
                'self': f'/v2/groups/{group_name}',
                'group': None,
                'error': 'there is no group with this name'
            })
            response.status_code = 400
            return response
        else:
            response = jsonify({
                'self': f'/v2/groups/{group_name}',
                'group': group
            })
            response.status_code = 200
            return response

    elif request.method == 'PUT':
        ''' [PUT] /v2/groups/<group_name> '''


@group_route.route('/members/<group_name>', methods=['GET'])
def group_members(group_name):
    """
    Endpoint for retrieving the members of a group.
    :param group_name: Unique name which identifies a group.
    :return: JSON representation of the members of a group and related metadata.
    """
    group_members = GroupMemberDao.get_group_members(group_name=group_name)

    if group_members is None:
        response = jsonify({
            'self': f'/v2/groups/members/{group_name}',
            'group': f'/v2/groups/{group_name}',
            'group_members': None,
            'error': 'the group does not exist or there are no members in the group'
        })
        response.status_code = 400
        return response
    else:
        response = jsonify({
            'self': f'/v2/groups/members/{group_name}',
            'group': f'/v2/groups/{group_name}',
            'group_members': group_members
        })
        response.status_code = 200
        return response


@group_route.route('/snapshot/<group_name>', methods=['GET'])
def group_snapshot(group_name):
    """
    Endpoint for retrieving a group along with statistics and leaderboards.
    :param group_name: Uniquely identifies a group.
    :return: JSON representation of a group and additional data.
    """
    group = GroupDao.get_group(group_name=group_name)
