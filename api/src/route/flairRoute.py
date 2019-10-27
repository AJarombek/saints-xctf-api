"""
Flair routes in the SaintsXCTF API.  Used for retrieving, creating, and deleting flair displayed on user profiles.
Author: Andrew Jarombek
Date: 7/5/2019
"""

from flask import Blueprint, request, jsonify, redirect, url_for, Response
from dao.flairDao import FlairDao
from model.Flair import Flair

flair_route = Blueprint('flair_route', __name__, url_prefix='/v2/flair')


@flair_route.route('', methods=['POST'])
def flair_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'flair' to the flair routes.
    :return: Response object letting the browser know where to redirect the request to.
    """
    if request.method == 'POST':
        ''' [POST] /v2/flair '''
        return redirect(url_for('flair_route.flair'), code=307)


@flair_route.route('/', methods=['POST'])
def flair():
    """
    Endpoint for creating flair.
    :return: JSON representation of user's flair and relevant metadata.
    """
    if request.method == 'POST':
        ''' [GET] /v2/flair/ '''
        return flair_post()


@flair_route.route('/links', methods=['GET'])
def flair_links() -> Response:
    """
    Endpoint for information about the flair API endpoints.
    :return: Metadata about the flair API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/flair/links '''
        return flair_links_get()


def flair_post():
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


def flair_links_get() -> Response:
    """
    Get all the other flair API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/flair/links',
        'endpoints': [
            {
                'link': '/v2/flair',
                'verb': 'POST',
                'description': 'Create a new flair item.'
            }
        ],
    })
    response.status_code = 200
    return response
