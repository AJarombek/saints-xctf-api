"""
Team routes in the SaintsXCTF API.  Used for retrieving and updating teams.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from flask import Blueprint, Response, request, redirect, url_for, jsonify
from sqlalchemy.engine import ResultProxy

from decorators import auth_required
from dao.teamDao import TeamDao
from dao.teamMemberDao import TeamMemberDao
from dao.teamGroupDao import TeamGroupDao
from model.Team import Team
from model.TeamData import TeamData

team_route = Blueprint('team_route', __name__, url_prefix='/v2/teams')


@team_route.route('', methods=['GET'])
@auth_required()
def teams_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'teams' to the team routes.
    :return: Response object letting the caller know where to redirect the request to.
    """
    if request.method == 'GET':
        ''' [GET] /v2/teams '''
        return redirect(url_for('team_route.teams'), code=302)


@team_route.route('/', methods=['GET'])
@auth_required()
def teams() -> Response:
    """
    Endpoints for searching all the teams
    :return: JSON representation of a list of teams and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /v2/teams/ '''
        return teams_get()


@team_route.route('/<name>', methods=['GET'])
@auth_required()
def team(name) -> Response:
    """
    Endpoints for specific teams (just searching)
    :param name: Name of a team
    :return: JSON representation of a team and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /v2/teams/<name> '''
        return team_by_name_get(name)


@team_route.route('/members/<team_name>', methods=['GET'])
@auth_required()
def team_members(team_name) -> Response:
    """
    Endpoint for retrieving the members of a team.
    :param team_name: Unique name which identifies a team.
    :return: JSON representation of the members of a team and related metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/teams/members/<team_name> '''
        return team_members_by_team_name_get(team_name)


@team_route.route('/groups/<team_name>', methods=['GET'])
@auth_required()
def team_groups(team_name) -> Response:
    """
    Endpoint for retrieving the groups that are part of a team.
    :param team_name: Unique name which identifies a team.
    :return: JSON representation of the groups in a team and related metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/teams/groups/<team_name> '''
        return team_groups_by_team_name_get(team_name)


@team_route.route('/links', methods=['GET'])
def team_links() -> Response:
    """
    Endpoint for information about the team API endpoints.
    :return: Metadata about the team API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/teams/links '''
        return team_links_get()


def teams_get() -> Response:
    """
    Retrieve all the teams in the database.
    :return: A response object for the GET API request.
    """
    all_teams: list = TeamDao.get_teams()

    if all_teams is None:
        response = jsonify({
            'self': '/v2/teams',
            'teams': None,
            'error': 'an unexpected error occurred retrieving teams'
        })
        response.status_code = 500
        return response
    else:
        team_dicts = [TeamData(team_info).__dict__ for team_info in all_teams]

        response = jsonify({
            'self': '/v2/teams',
            'teams': team_dicts
        })
        response.status_code = 200
        return response


def team_by_name_get(name) -> Response:
    """
    Retrieve a team based on its name.
    :param name: Name that uniquely identifies a team.
    :return: A response object for the GET API request.
    """
    team_info: Team = TeamDao.get_team_by_name(name=name)

    if team_info is None:
        response = jsonify({
            'self': f'/v2/teams/{name}',
            'team': None,
            'error': 'there is no team with this name'
        })
        response.status_code = 400
        return response
    else:
        team_dict: dict = TeamData(team_info).__dict__

        response = jsonify({
            'self': f'/v2/teams/{name}',
            'team': team_dict
        })
        response.status_code = 200
        return response


def team_members_by_team_name_get(team_name) -> Response:
    """
    Get the members of a team based on the team name.
    :param team_name: Unique name of a team.
    :return: A response object for the GET API request.
    """
    team_members_result: ResultProxy = TeamMemberDao.get_team_members(team_name=team_name)

    if team_members_result is None or team_members_result.rowcount == 0:
        response = jsonify({
            'self': f'/v2/teams/members/{team_name}',
            'team': f'/v2/teams/{team_name}',
            'team_members': None,
            'error': 'the team does not exist or it has no members'
        })
        response.status_code = 400
        return response
    else:
        team_members_list = [{
            'username': member.username,
            'first': member.first,
            'last': member.last,
            'member_since': member.member_since,
            'user': member.user,
            'status': member.status,
            'deleted': member.deleted
        }
            for member in team_members_result]

        response = jsonify({
            'self': f'/v2/teams/members/{team_name}',
            'group': f'/v2/teams/{team_name}',
            'team_members': team_members_list
        })
        response.status_code = 200
        return response


def team_groups_by_team_name_get(team_name) -> Response:
    """
    Get the groups that are part of a team based on the team name.
    :param team_name: Unique name of a team.
    :return: A response object for the GET API request.
    """
    team_groups_result: ResultProxy = TeamGroupDao.get_team_groups(team_name=team_name)

    if team_groups_result is None or team_groups_result.rowcount == 0:
        response = jsonify({
            'self': f'/v2/teams/groups/{team_name}',
            'team': f'/v2/teams/{team_name}',
            'team_groups': None,
            'error': 'the team does not exist or it has no groups'
        })
        response.status_code = 400
        return response
    else:
        team_groups_list = [{
            'id': member.id,
            'group_name': member.group_name,
            'group_title': member.group_title,
            'grouppic_name': member.grouppic_name,
            'description': member.description,
            'week_start': member.week_start,
            'deleted': member.deleted
        }
            for member in team_groups_result]

        response = jsonify({
            'self': f'/v2/teams/groups/{team_name}',
            'group': f'/v2/teams/{team_name}',
            'team_groups': team_groups_list
        })
        response.status_code = 200
        return response


def team_links_get() -> Response:
    """
    Get all the other team API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/teams/links',
        'endpoints': [
            {
                'link': '/v2/teams',
                'verb': 'GET',
                'description': 'Get all the teams in the database.'
            },
            {
                'link': '/v2/teams/<name>',
                'verb': 'GET',
                'description': 'Retrieve a single team with a given name.'
            },
            {
                'link': '/v2/teams/members/<name>',
                'verb': 'GET',
                'description': 'Retrieve the members of a team with a given name.'
            }
        ],
    })
    response.status_code = 200
    return response
