"""
Team routes in the SaintsXCTF API.  Used for retrieving and updating teams.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from flask import Blueprint, Response, request, redirect, url_for, jsonify

from decorators import auth_required

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


@team_route.route('/<username>', methods=['GET'])
@auth_required()
def team(username) -> Response:
    """
    Endpoints for specific teams (just searching)
    :param username: Name of a team
    :return: JSON representation of a team and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /v2/teams/<name> '''
        return team_by_name_get(username)


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
    pass


def team_by_name_get(name) -> Response:
    """
    Retrieve a team based on its name.
    :param name: Name that uniquely identifies a team.
    :return: A response object for the GET API request.
    """
    pass


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
            }
        ],
    })
    response.status_code = 200
    return response
