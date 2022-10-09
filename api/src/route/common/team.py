"""
Common code for the Team routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

from typing import Dict, List, Any, Union, Type

from flask import Response, jsonify

from model.Team import Team
from model.TeamData import TeamData
from dao.teamDao import TeamDao
from dao.teamDemoDao import TeamDemoDao
from route.common.versions import APIVersion


def team_links(version: str) -> Dict[str, Any]:
    """
    Get all the team API endpoints.
    :return: A dictionary describing all team API endpoints.
    """
    return {
        "self": f"/{version}/teams/links",
        "endpoints": [
            {
                "link": f"/{version}/teams",
                "verb": "GET",
                "description": "Get all the teams in the database.",
            },
            {
                "link": f"/{version}/teams/<name>",
                "verb": "GET",
                "description": "Retrieve a single team with a given name.",
            },
            {
                "link": f"/{version}/teams/members/<name>",
                "verb": "GET",
                "description": "Retrieve the members of a team with a given name.",
            },
            {
                "link": f"/{version}/teams/groups/<name>",
                "verb": "GET",
                "description": "Retrieve the groups in a team based on the team name.",
            },
            {
                "link": f"/{version}/teams/search/<text>/<limit>",
                "verb": "GET",
                "description": "Text search for teams.",
            },
        ],
    }


def teams_get(
    version: APIVersion, dao: Union[Type[TeamDao], Type[TeamDemoDao]]
) -> Response:
    """
    Retrieve all the teams in the database.
    :param version: Version of the API to use for the request.
    :param dao: Data access object to use for database access.
    :return: A response object for the GET API request.
    """
    all_teams: List[Team] = dao.get_teams()

    if all_teams is None:
        response = jsonify(
            {
                "self": f"/{version.value}/teams",
                "teams": None,
                "error": "an unexpected error occurred retrieving teams",
            }
        )
        response.status_code = 500
        return response
    else:
        team_dicts = [TeamData(team_info).__dict__ for team_info in all_teams]

        response = jsonify({"self": f"/{version.value}/teams", "teams": team_dicts})
        response.status_code = 200
        return response
