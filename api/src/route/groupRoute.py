"""
Group routes in the SaintsXCTF API.  Used for retrieving and updating groups.
Author: Andrew Jarombek
Date: 7/7/2019
"""

from flask import Blueprint, request, jsonify, Response, redirect, url_for
from sqlalchemy.engine import ResultProxy
from sqlalchemy.schema import Column
from datetime import datetime
from model.Group import Group
from model.GroupData import GroupData
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
    group_list: list = GroupDao.get_groups()

    if group_list is not None:
        group_data_list: list = [GroupData(group_obj).__dict__ for group_obj in group_list]

        for group_dict in group_data_list:
            if group_dict['grouppic'] is not None:
                try:
                    group_dict['grouppic'] = group_dict['grouppic'].decode('utf-8')
                except AttributeError:
                    pass

        response = jsonify({
            'self': f'/v2/groups',
            'groups': group_data_list
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
    group: Group = GroupDao.get_group(group_name=group_name)

    if group is None:
        response = jsonify({
            'self': f'/v2/groups/{group_name}',
            'group': None,
            'error': 'there is no group with this name'
        })
        response.status_code = 400
        return response
    else:
        group_dict = GroupData(group).__dict__

        if group_dict['grouppic'] is not None:
            try:
                group_dict['grouppic'] = group_dict['grouppic'].decode('utf-8')
            except AttributeError:
                pass

        response = jsonify({
            'self': f'/v2/groups/{group_name}',
            'group': group_dict
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
            'group': None,
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

            if updated_group_dict['grouppic'] is not None:
                try:
                    updated_group_dict['grouppic'] = updated_group_dict['grouppic'].decode('utf-8')
                except AttributeError:
                    pass

            response = jsonify({
                'self': f'/v2/groups/{group_name}',
                'updated': True,
                'group': updated_group_dict
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': f'/v2/groups/{group_name}',
                'updated': False,
                'group': None,
                'error': 'the group failed to update'
            })
            response.status_code = 500
            return response
    else:
        response = jsonify({
            'self': f'/v2/groups/{group_name}',
            'updated': False,
            'group': None,
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
    group_members: ResultProxy = GroupMemberDao.get_group_members(group_name=group_name)

    if group_members is None or group_members.rowcount == 0:
        response = jsonify({
            'self': f'/v2/groups/members/{group_name}',
            'group': f'/v2/groups/{group_name}',
            'group_members': None,
            'error': 'the group does not exist or there are no members in the group'
        })
        response.status_code = 400
        return response
    else:
        group_members_list = [{
                'username': member.username,
                'first': member.first,
                'last': member.last,
                'member_since': member.member_since,
                'user': member.user,
                'status': member.status,
                'deleted': member.deleted
            }
            for member in group_members]

        response = jsonify({
            'self': f'/v2/groups/members/{group_name}',
            'group': f'/v2/groups/{group_name}',
            'group_members': group_members_list
        })
        response.status_code = 200
        return response


def group_snapshot_by_group_name_get(group_name: str) -> Response:
    """
    Get a snapshot about a group based on the group name.
    :param group_name: Unique name of a group.
    :return: A response object for the GET API request.
    """
    group: Group = GroupDao.get_group(group_name=group_name)

    if group is None:
        response = jsonify({
            'self': f'/v2/groups/snapshot/{group_name}',
            'group_link': f'/v2/groups/{group_name}',
            'group': None,
            'error': 'the group does not exist'
        })
        response.status_code = 400
        return response

    group_members: ResultProxy = GroupMemberDao.get_group_members(group_name=group_name)
    group_members_list = [{
            'username': member.username,
            'first': member.first,
            'last': member.last,
            'member_since': member.member_since,
            'user': member.user,
            'status': member.status,
            'deleted': member.deleted
        }
        for member in group_members]

    # All group statistics are queried separately but combined into a single map
    miles: Column = LogDao.get_group_miles(group_name)
    miles_past_year: Column = LogDao.get_group_miles_interval(group_name, 'year')
    miles_past_month: Column = LogDao.get_group_miles_interval(group_name, 'month')
    miles_past_week: Column = LogDao.get_group_miles_interval(group_name, 'week', week_start=group['week_start'])
    run_miles: Column = LogDao.get_group_miles_interval_by_type(group_name, 'run')
    run_miles_past_year: Column = LogDao.get_group_miles_interval_by_type(group_name, 'run', 'year')
    run_miles_past_month: Column = LogDao.get_group_miles_interval_by_type(group_name, 'run', 'month')
    run_miles_past_week: Column = LogDao.get_group_miles_interval_by_type(group_name, 'run', 'week')
    all_time_feel: Column = LogDao.get_group_avg_feel(group_name)
    year_feel: Column = LogDao.get_group_avg_feel_interval(group_name, 'year')
    month_feel: Column = LogDao.get_group_avg_feel_interval(group_name, 'month')
    week_feel: Column = LogDao.get_group_avg_feel_interval(group_name, 'week', week_start=group['week_start'])

    statistics = {
        'miles': miles['total'],
        'milespastyear': miles_past_year['total'],
        'milespastmonth': miles_past_month['total'],
        'milespastweek': miles_past_week['total'],
        'runmiles': run_miles['total'],
        'runmilespastyear': run_miles_past_year['total'],
        'runmilespastmonth': run_miles_past_month['total'],
        'runmilespastweek': run_miles_past_week['total'],
        'alltimefeel': all_time_feel['average'],
        'yearfeel': year_feel['average'],
        'monthfeel': month_feel['average'],
        'weekfeel': week_feel['average']
    }

    group['members'] = group_members_list
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
