"""
Group routes in the SaintsXCTF API.  Used for retrieving and updating groups.
Author: Andrew Jarombek
Date: 7/7/2019
"""

from flask import Blueprint, request, jsonify, Response, redirect, url_for
from datetime import datetime
from model.Group import Group
from model.GroupData import GroupData
from model.GroupMember import GroupMember
from model.GroupMemberData import GroupMemberData
from dao.groupDao import GroupDao
from dao.groupMemberDao import GroupMemberDao
from dao.logDao import LogDao

group_route = Blueprint('group_route', __name__, url_prefix='/v2/groups')


@group_route.route('', methods=['GET'])
def groups_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'groups' to the group routes.
    :return: Response object letting the browser know where to redirect the request to.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups '''
        return redirect(url_for('group_route.groups'), code=302)


@group_route.route('/', methods=['GET'])
def groups() -> Response:
    """
    Endpoints for retrieving all the groups.
    :return: JSON representation of groups and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups '''
        return groups_get()


@group_route.route('/<group_name>', methods=['GET', 'PUT'])
def group(group_name) -> Response:
    """
    Endpoints for retrieving a single group and updating an existing group.
    :param group_name: Unique name which identifies a group.
    :return: JSON representation of a group and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/<group_name> '''
        return group_by_group_name_get(group_name)

    elif request.method == 'PUT':
        ''' [PUT] /v2/groups/<group_name> '''
        return group_by_group_name_put(group_name)


@group_route.route('/members/<group_name>', methods=['GET'])
def group_members(group_name) -> Response:
    """
    Endpoint for retrieving the members of a group.
    :param group_name: Unique name which identifies a group.
    :return: JSON representation of the members of a group and related metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/members/<group_name> '''
        return group_members_by_group_name_get(group_name)


@group_route.route('/snapshot/<group_name>', methods=['GET'])
def group_snapshot(group_name) -> Response:
    """
    Endpoint for retrieving a group along with statistics and leaderboards.
    :param group_name: Uniquely identifies a group.
    :return: JSON representation of a group and additional data.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/snapshot/<group_name> '''
        return group_snapshot_by_group_name_get(group_name)


@group_route.route('/links', methods=['GET'])
def group_links() -> Response:
    """
    Endpoint for information about the group API endpoints.
    :return: Metadata about the group API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/links '''
        return group_links_get()


def groups_get() -> Response:
    """
    Get all the groups in the database.
    :return: A response object for the GET API request.
    """
    groups = GroupDao.get_groups()

    if groups is not None:
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


def group_by_group_name_get(group_name: str) -> Response:
    """
    Get a group based on the unique group name.
    :return: A response object for the GET API request.
    """
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


def group_by_group_name_put(group_name: str) -> Response:
    """
    Update a group in the database.
    :param group_name: Unique name of a group.
    :return: A response object for the PUT API request.
    """
    old_group: Group = GroupDao.get_group(group_name=group_name)

    if old_group is None:
        response = jsonify({
            'self': f'/v2/groups/{group_name}',
            'updated': False,
            'comment': None,
            'error': 'there is no existing group with this name'
        })
        response.status_code = 400
        return response

    group_data: dict = request.get_json()
    new_group = Group(group_data)

    if old_group != new_group:

        new_group.modified_date = datetime.now()
        new_group.modified_app = 'api'

        is_updated = GroupDao.update_group(group=new_group)

        if is_updated:
            updated_group: Group = GroupDao.get_group(group_name=new_group.group_name)
            updated_group_dict: dict = GroupData(updated_group).__dict__

            response = jsonify({
                'self': f'/v2/groups/{group_name}',
                'updated': True,
                'comment': updated_group_dict
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': f'/v2/groups/{group_name}',
                'updated': False,
                'comment': None,
                'error': 'the group failed to update'
            })
            response.status_code = 500
            return response
    else:
        response = jsonify({
            'self': f'/v2/groups/{group_name}',
            'updated': False,
            'comment': None,
            'error': 'the group submitted is equal to the existing group with the same name'
        })
        response.status_code = 400
        return response


def group_members_by_group_name_get(group_name: str) -> Response:
    """
    Get the members of a group based on the group name.
    :param group_name: Unique name of a group.
    :return: A response object for the GET API request.
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


def group_snapshot_by_group_name_get(group_name: str) -> Response:
    """
    Get a snapshot about a group based on the group name.
    :param group_name: Unique name of a group.
    :return: A response object for the GET API request.
    """
    group = GroupDao.get_group(group_name=group_name)

    if group is None:
        response = jsonify({
            'self': f'/v2/groups/snapshot/{group_name}',
            'group_link': f'/v2/groups/{group_name}',
            'group': None,
            'error': 'the group does not exist'
        })
        response.status_code = 400
        return response

    group_members = GroupMemberDao.get_group_members(group_name=group_name)

    # All group statistics are queried separately but combined into a single map
    miles = LogDao.get_group_miles(group_name)
    miles_past_year = LogDao.get_group_miles_interval(group_name, 'year')
    miles_past_month = LogDao.get_group_miles_interval(group_name, 'month')
    miles_past_week = LogDao.get_group_miles_interval(group_name, 'week', week_start=group['week_start'])
    run_miles = LogDao.get_group_miles_interval_by_type(group_name, 'run')
    run_miles_past_year = LogDao.get_group_miles_interval_by_type(group_name, 'run', 'year')
    run_miles_past_month = LogDao.get_group_miles_interval_by_type(group_name, 'run', 'month')
    run_miles_past_week = LogDao.get_group_miles_interval_by_type(group_name, 'run', 'week')
    all_time_feel = LogDao.get_group_avg_feel(group_name)
    year_feel = LogDao.get_group_avg_feel_interval(group_name, 'year')
    month_feel = LogDao.get_group_avg_feel_interval(group_name, 'month')
    week_feel = LogDao.get_group_avg_feel_interval(group_name, 'week', week_start=group['week_start'])

    statistics = {
        'miles': miles,
        'milespastyear': miles_past_year,
        'milespastmonth': miles_past_month,
        'milespastweek': miles_past_week,
        'runmiles': run_miles,
        'runmilespastyear': run_miles_past_year,
        'runmilespastmonth': run_miles_past_month,
        'runmilespastweek': run_miles_past_week,
        'alltimefeel': all_time_feel,
        'yearfeel': year_feel,
        'monthfeel': month_feel,
        'weekfeel': week_feel
    }

    group['members'] = group_members
    group['statistics'] = statistics

    response = jsonify({
        'self': f'/v2/groups/snapshot/{group_name}',
        'group_link': f'/v2/groups/{group_name}',
        'group': group
    })
    response.status_code = 200
    return response


def group_links_get() -> Response:
    """
    Get all the other group API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/groups/links',
        'endpoints': [
            {
                'link': '/v2/groups',
                'verb': 'GET',
                'description': 'Get all the groups in the database.'
            },
            {
                'link': '/v2/groups/<group_name>',
                'verb': 'GET',
                'description': 'Retrieve a single group based on the group name.'
            },
            {
                'link': '/v2/groups/<group_name>',
                'verb': 'PUT',
                'description': 'Update a group based on the group name.'
            },
            {
                'link': '/v2/groups/members/<group_name>',
                'verb': 'GET',
                'description': 'Get the members of a group based on the group name.'
            },
            {
                'link': '/v2/groups/snapshot/<group_name>',
                'verb': 'GET',
                'description': 'Get a snapshot about a group based on the group name.'
            }
        ],
    })
    response.status_code = 200
    return response
