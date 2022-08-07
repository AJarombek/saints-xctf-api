"""
Common code for the Group routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

links = {
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
            'link': '/v2/groups/<id>',
            'verb': 'PUT',
            'description': 'Update a group based on its id.'
        },
        {
            'link': '/v2/groups/team/<id>',
            'verb': 'GET',
            'description': 'Retrieve team information about a group.'
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
            'link': '/v2/groups/members/<group_id>/<username>',
            'verb': 'PUT',
            'description': 'Update a group membership for a user.'
        },
        {
            'link': '/v2/groups/members/<group_id>/<username>',
            'verb': 'DELETE',
            'description': 'Delete a users group membership.'
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
}
