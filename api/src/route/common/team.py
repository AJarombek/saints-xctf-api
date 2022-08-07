"""
Common code for the Team routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

links = {
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
        },
        {
            'link': '/v2/teams/groups/<name>',
            'verb': 'GET',
            'description': 'Retrieve the groups in a team based on the team name.'
        },
        {
            'link': '/v2/teams/search/<text>/<limit>',
            'verb': 'GET',
            'description': 'Text search for teams.'
        }
    ],
}
