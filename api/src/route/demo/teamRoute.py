"""
Team routes in the demo version of the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/10/2022
"""

from flask import Blueprint, Response, request, redirect, url_for, jsonify
from flasgger import swag_from

from decorators import auth_required
from model.Team import Team
from model.TeamData import TeamData
from route.common.team import links

team_demo_route = Blueprint('team_demo_route', __name__, url_prefix='/demo/teams')

team_database = {
    'friends': Team(team={}),
    'jarombek': Team(team={}),
    'saintsxctf': Team(team={}),
    'saintsxctf_alumni': Team(team={}),
}


@team_demo_route.route('', methods=['GET'])
@auth_required()
def teams_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'teams' to the team routes.
    :return: Response object letting the caller know where to redirect the request to.
    """
    if request.method == 'GET':
        ''' [GET] /demo/teams '''
        return redirect(url_for('team_route.teams'), code=302)


@team_demo_route.route('/', methods=['GET'])
@auth_required()
@swag_from('swagger/teamRoute/teamsGet.yml', methods=['GET'])
def teams() -> Response:
    """
    Endpoints for searching all the teams
    :return: JSON representation of a list of teams and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /demo/teams/ '''
        return teams_get()


@team_demo_route.route('/<name>', methods=['GET'])
@auth_required()
@swag_from('swagger/teamRoute/teamGet.yml', methods=['GET'])
def team(name) -> Response:
    """
    Endpoints for specific teams (just searching)
    :param name: Name of a team
    :return: JSON representation of a team and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /demo/teams/<name> '''
        return team_by_name_get(name)


@team_demo_route.route('/members/<team_name>', methods=['GET'])
@auth_required()
@swag_from('swagger/teamRoute/teamMembersGet.yml', methods=['GET'])
def team_members(team_name) -> Response:
    """
    Endpoint for retrieving the members of a team.
    :param team_name: Unique name which identifies a team.
    :return: JSON representation of the members of a team and related metadata.
    """
    if request.method == 'GET':
        ''' [GET] /demo/teams/members/<team_name> '''
        return team_members_by_team_name_get(team_name)


@team_demo_route.route('/groups/<team_name>', methods=['GET'])
@auth_required()
@swag_from('swagger/teamRoute/teamGroupsGet.yml', methods=['GET'])
def team_groups(team_name) -> Response:
    """
    Endpoint for retrieving the groups that are part of a team.
    :param team_name: Unique name which identifies a team.
    :return: JSON representation of the groups in a team and related metadata.
    """
    if request.method == 'GET':
        ''' [GET] /demo/teams/groups/<team_name> '''
        return team_groups_by_team_name_get(team_name)


@team_demo_route.route('/search/<text>/<limit>', methods=['GET'])
@auth_required()
@swag_from('swagger/teamRoute/teamSearchGet.yml', methods=['GET'])
def search_teams(text, limit) -> Response:
    """
    Endpoint that performs a text search for teams.
    :param text: A string of text that was searched for.
    :param limit: The maximum number of teams to return.
    :return: JSON representation of a list of teams and their related metadata.
    """
    if request.method == 'GET':
        ''' [GET] /demo/teams/search/<text>/<limit> '''
        return search_teams_by_text_get(text, limit)


@team_demo_route.route('/links', methods=['GET'])
@swag_from('swagger/teamRoute/teamLinks.yml', methods=['GET'])
def team_links() -> Response:
    """
    Endpoint for information about the team API endpoints.
    :return: Metadata about the team API.
    """
    if request.method == 'GET':
        ''' [GET] /demo/teams/links '''
        return team_links_get()


def teams_get() -> Response:
    """
    Retrieve all the teams in the database.
    :return: A response object for the GET API request.
    """
    response = jsonify({
        'self': '/demo/teams',
        'teams': []
    })
    response.status_code = 200
    return response


def team_by_name_get(name) -> Response:
    """
    Retrieve a team based on its name.
    :param name: Name that uniquely identifies a team.
    :return: A response object for the GET API request.
    """
    response = jsonify({
        'self': f'/demo/teams/{name}',
        'team': {}
    })
    response.status_code = 200
    return response


def team_members_by_team_name_get(team_name) -> Response:
    """
    Get the members of a team based on the team name.
    :param team_name: Unique name of a team.
    :return: A response object for the GET API request.
    """
    response = jsonify({
        'self': f'/demo/teams/members/{team_name}',
        'group': f'/demo/teams/{team_name}',
        'team_members': []
    })
    response.status_code = 200
    return response


def team_groups_by_team_name_get(team_name) -> Response:
    """
    Get the groups that are part of a team based on the team name.
    :param team_name: Unique name of a team.
    :return: A response object for the GET API request.
    """
    response = jsonify({
        'self': f'/demo/teams/groups/{team_name}',
        'group': f'/demo/teams/{team_name}',
        'team_groups': []
    })
    response.status_code = 200
    return response


def search_teams_by_text_get(text: str, limit: int) -> Response:
    """
    Search for teams based on a string of text.  Limit the number of teams returned.
    :param text: A string of text that was searched for.
    :param limit: The maximum number of teams to return.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/demo/teams/search/{text}/{limit}',
        'teams': []
    })
    response.status_code = 200
    return response


def team_links_get() -> Response:
    """
    Get all the other team API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify(links)
    response.status_code = 200
    return response
