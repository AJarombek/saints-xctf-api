"""
Flair routes in the SaintsXCTF API.  Used for retrieving, creating, and deleting flair displayed on user profiles.
Author: Andrew Jarombek
Date: 7/5/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.flairDao import FlairDao
from model.Flair import Flair

flair_route = Blueprint('flair_route', __name__, url_prefix='/v2/flair')


@flair_route.route('/', methods=['POST'])
def flair():
    """
    Endpoint for creating flair used on a users profile.
    :return: JSON with the resulting Flair object and relevant metadata.
    """
    flair_data: dict = request.get_json()
    username = flair_data.get('username')
    flair_content = flair_data.get('flair')
    flair = Flair({
        'username': username,
        'flair': flair_content
    })
    flair_added = FlairDao.add_flair(flair)

    if flair_added:
        new_flair = FlairDao.get_flair_by_content(username, flair_content)
        response = jsonify({
            'self': f'/v2/flair',
            'added': True,
            'flair': new_flair
        })
        response.status_code = 201
        return response
    else:
        response = jsonify({
            'self': f'/v2/flair',
            'added': False,
            'flair': None,
            'error': 'the flair creation failed'
        })
        response.status_code = 500
        return response
