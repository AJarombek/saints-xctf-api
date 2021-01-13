"""
Group routes in the SaintsXCTF API.  Used for retrieving and updating groups.
Author: Andrew Jarombek
Date: 7/7/2019
"""

from datetime import datetime
from typing import Optional

from flask import Blueprint, request, jsonify, Response, redirect, url_for
from sqlalchemy.engine import ResultProxy, RowProxy
from sqlalchemy.schema import Column

from decorators import auth_required
from model.Group import Group
from model.GroupData import GroupData
from dao.groupDao import GroupDao
from dao.groupMemberDao import GroupMemberDao
from dao.logDao import LogDao

group_route = Blueprint('group_route', __name__, url_prefix='/v2/groups')


@group_route.route('', methods=['GET'])
@auth_required()
def groups_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'groups' to the group routes.
    :return: Response object letting the browser know where to redirect the request to.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups '''
        return redirect(url_for('group_route.groups'), code=302)


@group_route.route('/', methods=['GET'])
@auth_required()
def groups() -> Response:
    """
    Endpoints for retrieving all the groups.
    :return: JSON representation of groups and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups '''
        return groups_get()


@group_route.route('/<team_name>/<group_name>', methods=['GET', 'PUT'])
@auth_required()
def group(team_name, group_name) -> Response:
    """
    Endpoints for retrieving a single group and updating an existing group.
    :param team_name: Unique name which identifies a team.
    :param group_name: Unique name which identifies a group within a team.
    :return: JSON representation of a group and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/<team_name>/<group_name> '''
        return group_by_group_name_get(team_name, group_name)

    elif request.method == 'PUT':
        ''' [PUT] /v2/groups/<group_name> '''
        return group_by_group_name_put(team_name, group_name)


@group_route.route('/<group_id>', methods=['GET', 'PUT'])
@auth_required()
def group_by_id(group_id) -> Response:
    """
    Endpoints for retrieving a single group based on its id.
    :param group_id: Unique id which identifies a group.
    :return: JSON representation of a group and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/<id> '''
        return group_by_id_get(group_id)


@group_route.route('/members/<team_name>/<group_name>', methods=['GET'])
@auth_required()
def group_members(team_name, group_name) -> Response:
    """
    Endpoint for retrieving the members of a group.
    :param team_name: Unique name which identifies a team.
    :param group_name: Unique name which identifies a group within a team.
    :return: JSON representation of the members of a group and related metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/members/<team_name>/<group_name> '''
        return group_members_by_group_name_get(team_name, group_name)


@group_route.route('/members/<group_id>', methods=['GET'])
@auth_required()
def group_members_by_id(group_id) -> Response:
    """
    Endpoint for retrieving the members of a group based on the group id.
    :param group_id: Unique id which identifies a group within a team.
    :return: JSON representation of the members of a group and related metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/members/<group_id> '''
        return group_members_by_id_get(group_id)


@group_route.route('/statistics/<group_id>', methods=['GET'])
@auth_required()
def group_statistics(group_id) -> Response:
    """
    Endpoint for retrieving statistics about group members.
    :param group_id: Unique id which identifies a group within a team.
    :return: JSON representation of group statistics and additional data.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/statistics/<group_id> '''
        return group_statistics_by_id_get(group_id)


@group_route.route('/leaderboard/<group_id>', methods=['GET'])
@group_route.route('/leaderboard/<group_id>/<interval>', methods=['GET'])
@auth_required()
def group_leaderboard(group_id, interval = None) -> Response:
    """
    Endpoint for retrieving leaderboard information about a group.
    You are so caring, it is beautiful.  My love for you is forever.
    :param group_id: Unique id which identifies a group within a team.
    :param interval: Time interval to get leaderboard info within.
    :return: JSON representation of group leaderboard info and additional data.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/leaderboard/<group_id>/<interval> '''
        return group_leaderboard_get(group_id, interval)


@group_route.route('/snapshot/<team_name>/<group_name>', methods=['GET'])
@auth_required()
def group_snapshot(team_name, group_name) -> Response:
    """
    Endpoint for retrieving a group along with statistics and leaderboards.
    :param team_name: Unique name which identifies a team.
    :param group_name: Unique name which identifies a group within a team.
    :return: JSON representation of a group and additional data.
    """
    if request.method == 'GET':
        ''' [GET] /v2/groups/snapshot/<team_name>/<group_name> '''
        return group_snapshot_by_group_name_get(team_name, group_name)


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


def group_by_group_name_get(team_name: str, group_name: str) -> Response:
    """
    Get a group based on the unique group name.
    :param team_name: Unique name which identifies a team.
    :param group_name: Unique name which identifies a group within a team.
    :return: A response object for the GET API request.
    """
    group_row: Optional[RowProxy] = GroupDao.get_group(team_name=team_name, group_name=group_name)

    if group_row is None:
        response = jsonify({
            'self': f'/v2/groups/{team_name}/{group_name}',
            'group': None,
            'error': 'there is no group with this name'
        })
        response.status_code = 400
        return response
    else:
        group_dict = {key: value for key, value in group_row.items()}
        response = jsonify({
            'self': f'/v2/groups/{team_name}/{group_name}',
            'group': group_dict
        })
        response.status_code = 200
        return response


def group_by_group_name_put(team_name: str, group_name: str) -> Response:
    """
    Update a group in the database.
    :param team_name: Unique name which identifies a team.
    :param group_name: Unique name which identifies a group within a team.
    :return: A response object for the PUT API request.
    """
    old_group_row: Optional[RowProxy] = GroupDao.get_group(team_name=team_name, group_name=group_name)

    if old_group_row is None:
        response = jsonify({
            'self': f'/v2/groups/{team_name}/{group_name}',
            'updated': False,
            'group': None,
            'error': 'there is no existing group with this name'
        })
        response.status_code = 400
        return response

    old_group_dict = {key: value for key, value in old_group_row.items()}
    old_group = Group(old_group_dict)
    group_data: dict = request.get_json()
    new_group = Group(group_data)

    if old_group != new_group:

        new_group.modified_date = datetime.now()
        new_group.modified_app = 'saints-xctf-api'

        is_updated = GroupDao.update_group(group=new_group)

        if is_updated:
            updated_group_row: Optional[RowProxy] = GroupDao.get_group(
                team_name=team_name,
                group_name=new_group.group_name
            )

            updated_group_dict = {key: value for key, value in updated_group_row.items()}
            response = jsonify({
                'self': f'/v2/groups/{team_name}/{group_name}',
                'updated': True,
                'group': updated_group_dict
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': f'/v2/groups/{team_name}/{group_name}',
                'updated': False,
                'group': None,
                'error': 'the group failed to update'
            })
            response.status_code = 500
            return response
    else:
        response = jsonify({
            'self': f'/v2/groups/{team_name}/{group_name}',
            'updated': False,
            'group': None,
            'error': 'the group submitted is equal to the existing group with the same name'
        })
        response.status_code = 400
        return response


def group_by_id_get(group_id: str) -> Response:
    """
    Get a group based on the unique group id.
    :param group_id: Unique id which identifies a group.
    :return: A response object for the GET API request.
    """
    group_row: Group = GroupDao.get_group_by_id(group_id=int(group_id))

    if group_row is None:
        response = jsonify({
            'self': f'/v2/groups/{group_id}',
            'group': None,
            'error': 'there is no group with this id'
        })
        response.status_code = 400
        return response
    else:
        group_dict = GroupData(group_row).__dict__

        if group_dict['grouppic'] is not None:
            try:
                group_dict['grouppic'] = group_dict['grouppic'].decode('utf-8')
            except AttributeError:
                pass

        response = jsonify({
            'self': f'/v2/groups/{group_id}',
            'group': group_dict
        })
        response.status_code = 200
        return response


def group_members_by_group_name_get(team_name: str, group_name: str) -> Response:
    """
    Get the members of a group based on the group name.
    :param team_name: Unique name which identifies a team.
    :param group_name: Unique name which identifies a group within a team.
    :return: A response object for the GET API request.
    """
    group_members: ResultProxy = GroupMemberDao.get_group_members(group_name=group_name, team_name=team_name)

    if group_members is None or group_members.rowcount == 0:
        response = jsonify({
            'self': f'/v2/groups/members/{team_name}/{group_name}',
            'group': f'/v2/groups/{team_name}/{group_name}',
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
                'status': member.status
            }
            for member in group_members]

        response = jsonify({
            'self': f'/v2/groups/members/{team_name}/{group_name}',
            'group': f'/v2/groups/{team_name}/{group_name}',
            'group_members': group_members_list
        })
        response.status_code = 200
        return response


def group_members_by_id_get(group_id: str) -> Response:
    """
    Get the members of a group based on the group id.
    :param group_id: Unique id which identifies a group.
    :return: A response object for the GET API request.
    """
    group_members: ResultProxy = GroupMemberDao.get_group_members_by_id(group_id=group_id)

    if group_members is None or group_members.rowcount == 0:
        response = jsonify({
            'self': f'/v2/groups/members/{group_id}',
            'group': f'/v2/groups/{group_id}',
            'group_members': None,
            'error': 'a group does not exist with this id or the group has no members'
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
                'status': member.status
            }
            for member in group_members]

        response = jsonify({
            'self': f'/v2/groups/members/{group_id}',
            'group': f'/v2/groups/{group_id}',
            'group_members': group_members_list
        })
        response.status_code = 200
        return response


def group_statistics_by_id_get(group_id: str) -> Response:
    """
    Get statistics of a group based on the group id.
    :param group_id: Unique id which identifies a group.
    :return: A response object for the GET API request.
    """
    group_object: Group = GroupDao.get_group_by_id(group_id=int(group_id))

    if group_object is None:
        response = jsonify({
            'self': f'/v2/groups/statistics/{group_id}',
            'stats': None,
            'error': 'there is no group with this id'
        })
        response.status_code = 400
        return response

    response = jsonify({
        'self': f'/v2/groups/statistics/{group_id}',
        'stats': compile_group_statistics(group_object)
    })
    response.status_code = 200
    return response


def group_leaderboard_get(group_id: str, interval: str) -> Response:
    """
    Get stats of users in a group based on the group id.  These stats are used to build a leaderboard.
    :param group_id: Unique id which identifies a group.
    :param interval: Time interval to get leaderboard info within.
    :return: A response object for the GET API request.
    """
    group_object: Group = GroupDao.get_group_by_id(group_id=int(group_id))

    if group_object is None:
        response = jsonify({
            'self': f"/v2/groups/leaderboard/{group_id}{f'/{interval}' if interval else ''}",
            'leaderboard': None,
            'error': 'there is no group with this id'
        })
        response.status_code = 400
        return response

    leaderboard: ResultProxy = GroupDao.get_group_leaderboard(group_id=group_object.id)

    if leaderboard is None or leaderboard.rowcount == 0:
        response = jsonify({
            'self': f"/v2/groups/leaderboard/{group_id}{f'/{interval}' if interval else ''}",
            'leaderboard': None,
            'error': 'an unexpected error occurred retrieving leaderboard data'
        })
        response.status_code = 500
        return response
    else:
        leaderboard_list = [{
                'username': entry.username,
                'first': entry.first,
                'last': entry.last,
                'miles': entry.miles,
                'miles_run': entry.miles_run,
                'miles_biked': entry.miles_biked,
                'miles_swam': entry.miles_swam,
                'miles_other': entry.miles_other
            }
            for entry in leaderboard]

        response = jsonify({
            'self': f"/v2/groups/leaderboard/{group_id}{f'/{interval}' if interval else ''}",
            'leaderboard': leaderboard_list
        })
        response.status_code = 200
        return response


def group_snapshot_by_group_name_get(team_name: str, group_name: str) -> Response:
    """
    Get a snapshot about a group based on the group name.
    :param team_name: Unique name which identifies a team.
    :param group_name: Unique name which identifies a group within a team.
    :return: A response object for the GET API request.
    """
    group_row: Optional[RowProxy] = GroupDao.get_group(team_name=team_name, group_name=group_name)

    if group_row is None:
        response = jsonify({
            'self': f'/v2/groups/snapshot/{team_name}/{group_name}',
            'group': f'/v2/groups/{team_name}/{group_name}',
            'group_snapshot': None,
            'error': 'the group does not exist'
        })
        response.status_code = 400
        return response

    group_dict = {key: value for key, value in group_row.items()}
    group = Group(group_dict)

    group_members: ResultProxy = GroupMemberDao.get_group_members(group_name=group_name, team_name=team_name)
    group_members_list = [{
            'username': member.username,
            'first': member.first,
            'last': member.last,
            'member_since': member.member_since,
            'user': member.user,
            'status': member.status
        }
        for member in group_members]

    # All group statistics are queried separately but combined into a single map
    statistics = compile_group_statistics(group_object=group)

    group_dict: dict = GroupData(group).__dict__

    try:
        group_dict['grouppic'] = group_dict['grouppic'].decode('utf-8')
    except AttributeError:
        pass

    group_dict['members'] = group_members_list
    group_dict['statistics'] = statistics

    response = jsonify({
        'self': f'/v2/groups/snapshot/{team_name}/{group_name}',
        'group': f'/v2/groups/{team_name}/{group_name}',
        'group_snapshot': group_dict
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
                'link': '/v2/groups/<team_name>/<group_name>',
                'verb': 'GET',
                'description': 'Retrieve a single group based on the group name and team name.'
            },
            {
                'link': '/v2/groups/<id>',
                'verb': 'GET',
                'description': 'Retrieve a single group based on its id.'
            },
            {
                'link': '/v2/groups/<team_name>/<group_name>',
                'verb': 'PUT',
                'description': 'Update a group based on the group name and team name.'
            },
            {
                'link': '/v2/groups/members/<team_name>/<group_name>',
                'verb': 'GET',
                'description': 'Get the members of a group based on the group name and team name.'
            },
            {
                'link': '/v2/groups/members/<group_id>',
                'verb': 'GET',
                'description': 'Get the members of a group based on the group id.'
            },
            {
                'link': '/v2/groups/statistics/<group_id>',
                'verb': 'GET',
                'description': 'Get the statistics of a group based on the group id.'
            },
            {
                'link': '/v2/groups/leaderboard/<group_id>',
                'verb': 'GET',
                'description': 'Get group leaderboard information.  There is no time constraint on this data.'
            },
            {
                'link': '/v2/groups/leaderboard/<group_id>/<interval>',
                'verb': 'GET',
                'description': 'Get group leaderboard information during a certain time interval.'
            },
            {
                'link': '/v2/groups/snapshot/<team_name>/<group_name>',
                'verb': 'GET',
                'description': 'Get a snapshot about a group based on the group name and team name.'
            }
        ],
    })
    response.status_code = 200
    return response


"""
Helper Methods
"""


def compile_group_statistics(group_object: Group):
    """
    Query group statistics and combine them into a single map.
    :param group_object: A group object containing information such as the preferred week start date.
    """
    group_name = group_object.group_name

    miles: Column = LogDao.get_group_miles(group_name)
    miles_past_year: Column = LogDao.get_group_miles_interval(group_name, 'year')
    miles_past_month: Column = LogDao.get_group_miles_interval(group_name, 'month')
    miles_past_week: Column = LogDao.get_group_miles_interval(group_name, 'week', week_start=group_object.week_start)
    run_miles: Column = LogDao.get_group_miles_interval_by_type(group_name, 'run')
    run_miles_past_year: Column = LogDao.get_group_miles_interval_by_type(group_name, 'run', 'year')
    run_miles_past_month: Column = LogDao.get_group_miles_interval_by_type(group_name, 'run', 'month')
    run_miles_past_week: Column = LogDao.get_group_miles_interval_by_type(group_name, 'run', 'week')
    all_time_feel: Column = LogDao.get_group_avg_feel(group_name)
    year_feel: Column = LogDao.get_group_avg_feel_interval(group_name, 'year')
    month_feel: Column = LogDao.get_group_avg_feel_interval(group_name, 'month')
    week_feel: Column = LogDao.get_group_avg_feel_interval(group_name, 'week', week_start=group_object.week_start)

    return {
        'miles_all_time': float(miles['total']),
        'miles_past_year': float(0 if miles_past_year['total'] is None else miles_past_year['total']),
        'miles_past_month': float(0 if miles_past_month['total'] is None else miles_past_month['total']),
        'miles_past_week': float(0 if miles_past_week['total'] is None else miles_past_week['total']),
        'run_miles_all_time': float(0 if run_miles['total'] is None else run_miles['total']),
        'run_miles_past_year': float(0 if run_miles_past_year['total'] is None else run_miles_past_year['total']),
        'run_miles_past_month': float(0 if run_miles_past_month['total'] is None else run_miles_past_month['total']),
        'run_miles_past_week': float(0 if run_miles_past_week['total'] is None else run_miles_past_week['total']),
        'feel_all_time': float(0 if all_time_feel['average'] is None else all_time_feel['average']),
        'feel_past_year': float(0 if year_feel['average'] is None else year_feel['average']),
        'feel_past_month': float(0 if month_feel['average'] is None else month_feel['average']),
        'feel_past_week': float(0 if week_feel['average'] is None else week_feel['average'])
    }
