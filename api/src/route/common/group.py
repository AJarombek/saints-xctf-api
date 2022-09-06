"""
Common code for the Group routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

from typing import Dict, Any


def group_links(version: str) -> Dict[str, Any]:
    """
    Get all the group API endpoints.
    :return: A dictionary describing all group API endpoints.
    """
    return {
        'self': f'/{version}/groups/links',
        'endpoints': [
            {
                'link': f'/{version}/groups',
                'verb': 'GET',
                'description': 'Get all the groups in the database.'
            },
            {
                'link': f'/{version}/groups/<team_name>/<group_name>',
                'verb': 'GET',
                'description': 'Retrieve a single group based on the group name and team name.'
            },
            {
                'link': f'/{version}/groups/<id>',
                'verb': 'GET',
                'description': 'Retrieve a single group based on its id.'
            },
            {
                'link': f'/{version}/groups/<id>',
                'verb': 'PUT',
                'description': 'Update a group based on its id.'
            },
            {
                'link': f'/{version}/groups/team/<id>',
                'verb': 'GET',
                'description': 'Retrieve team information about a group.'
            },
            {
                'link': f'/{version}/groups/<team_name>/<group_name>',
                'verb': 'PUT',
                'description': 'Update a group based on the group name and team name.'
            },
            {
                'link': f'/{version}/groups/members/<team_name>/<group_name>',
                'verb': 'GET',
                'description': 'Get the members of a group based on the group name and team name.'
            },
            {
                'link': f'/{version}/groups/members/<group_id>',
                'verb': 'GET',
                'description': 'Get the members of a group based on the group id.'
            },
            {
                'link': f'/{version}/groups/members/<group_id>/<username>',
                'verb': 'PUT',
                'description': 'Update a group membership for a user.'
            },
            {
                'link': f'/{version}/groups/members/<group_id>/<username>',
                'verb': 'DELETE',
                'description': 'Delete a users group membership.'
            },
            {
                'link': f'/{version}/groups/statistics/<group_id>',
                'verb': 'GET',
                'description': 'Get the statistics of a group based on the group id.'
            },
            {
                'link': f'/{version}/groups/leaderboard/<group_id>',
                'verb': 'GET',
                'description': 'Get group leaderboard information.  There is no time constraint on this data.'
            },
            {
                'link': f'/{version}/groups/leaderboard/<group_id>/<interval>',
                'verb': 'GET',
                'description': 'Get group leaderboard information during a certain time interval.'
            },
            {
                'link': f'/{version}/groups/snapshot/<team_name>/<group_name>',
                'verb': 'GET',
                'description': 'Get a snapshot about a group based on the group name and team name.'
            }
        ],
    }
