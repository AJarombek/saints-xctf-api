"""
Flair routes in the SaintsXCTF API.  Used for retrieving, creating, and deleting flair displayed on user profiles.
Author: Andrew Jarombek
Date: 7/5/2019
"""

from flask import Blueprint, request, jsonify, redirect, url_for, Response
from datetime import datetime
from dao.flairDao import FlairDao
from model.Flair import Flair
from model.FlairData import FlairData

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

    if flair_data is None:
        response = jsonify({
            'self': f'/v2/flair',
            'added': False,
            'error': "the request body isn't populated"
        })
        response.status_code = 400
        return response

    username = flair_data.get('username')
    flair_content = flair_data.get('flair')

    if username is None or flair_content is None:
        response = jsonify({
            'self': f'/v2/flair',
            'added': False,
            'error': "'username' and 'flair' are required fields"
        })
        response.status_code = 400
        return response

    flair = Flair({
        'username': username,
        'flair': flair_content
    })

    flair.created_date = datetime.now()
    flair.created_app = 'api'

    flair_added: bool = FlairDao.add_flair(flair)

    if flair_added:
        new_flair: Flair = FlairDao.get_flair_by_content(username, flair_content)
        new_flair_dict: dict = FlairData(new_flair).__dict__

        response = jsonify({
            'self': f'/v2/flair',
            'added': True,
            'flair': new_flair_dict
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
