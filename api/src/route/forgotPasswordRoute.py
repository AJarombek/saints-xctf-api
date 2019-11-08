"""
ForgotPassword routes in the SaintsXCTF API.  Used for retrieving, creating,
and deleting forgot password codes for users.
Author: Andrew Jarombek
Date: 7/4/2019
"""

from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, Response
from utils.codes import generate_code
from dao.forgotPasswordDao import ForgotPasswordDao
from model.ForgotPassword import ForgotPassword
from model.ForgotPasswordData import ForgotPasswordData

forgot_password_route = Blueprint('forgot_password_route', __name__, url_prefix='/v2/forgot_password')


@forgot_password_route.route('/<username>', methods=['GET', 'POST'])
def forgot_password(username) -> Response:
    """
    Endpoints for retrieving or creating a forgot password code
    :param username: Username which uniquely identifies a User
    :return: JSON representation of a forgot password code and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /v2/forgot_password/<username> '''
        return forgot_password_get(username)
    if request.method == 'POST':
        ''' [POST] /v2/forgot_password/<username> '''
        return forgot_password_post(username)


@forgot_password_route.route('/links', methods=['GET'])
def flair_links() -> Response:
    """
    Endpoint for information about the forgot password API endpoints.
    :return: Metadata about the forgot password API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/forgot_password/links '''
        return forgot_password_links_get()


def forgot_password_get(username) -> Response:
    """
    Retrieve an existing forgot password code for a specific user.
    :param username: Uniquely identifies a user.
    :return: JSON with the resulting Forgot Password object and relevant metadata.
    """
    forgot_password_codes: list = ForgotPasswordDao.get_forgot_password_codes(username=username)

    if forgot_password_codes is None:
        response = jsonify({
            'self': f'/v2/forgot_password/{username}',
            'forgot_password_codes': None,
            'error': 'this user has no forgot password codes'
        })
        response.status_code = 400
        return response
    else:
        forgot_password_dicts: list = [ForgotPasswordData(code).__dict__ for code in forgot_password_codes]

        response = jsonify({
            'self': f'/v2/forgot_password/{username}',
            'forgot_password_codes': forgot_password_dicts,
        })
        response.status_code = 200
        return response


def forgot_password_post(username) -> Response:
    """
    Create a new forgot password code for a specific user.
    :param username: Uniquely identifies a user.
    :return: JSON with the resulting Forgot Password object and relevant metadata.
    """
    code = generate_code(length=8)
    expires = datetime.now() + timedelta(hours=2)
    expires = expires.date()

    new_forgot_password = ForgotPassword({
        'forgot_code': code,
        'username': username,
        'expires': expires
    })
    forgot_password_inserted = ForgotPasswordDao.add_forgot_password_code(new_forgot_password)

    if forgot_password_inserted:
        new_forgot_password = ForgotPasswordDao.get_forgot_password_code(code)
        response = jsonify({
            'self': f'/v2/forgot_password/{username}',
            'inserted': True,
            'forgot_password_code': new_forgot_password
        })
        response.status_code = 201
        return response
    else:
        response = jsonify({
            'self': f'/v2/forgot_password/{username}',
            'inserted': False,
            'error': 'the forgot password code creation failed'
        })
        response.status_code = 500
        return response


def forgot_password_links_get() -> Response:
    """
    Get all the other forgot password API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/forgot_password/links',
        'endpoints': [
            {
                'link': '/v2/forgot_password/<username>',
                'verb': 'GET',
                'description': 'Retrieve a single forgot password code assigned to a given username.'
            },
            {
                'link': '/v2/forgot_password/<username>',
                'verb': 'POST',
                'description': 'Create a new forgot password code.'
            }
        ],
    })
    response.status_code = 200
    return response
