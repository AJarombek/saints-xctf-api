"""
ForgotPassword routes in the SaintsXCTF API.  Used for retrieving, creating,
and deleting forgot password codes for users.
Author: Andrew Jarombek
Date: 7/4/2019
"""

from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, Response
from sqlalchemy.engine import ResultProxy

from decorators import auth_required
from utils.codes import generate_code
from dao.forgotPasswordDao import ForgotPasswordDao
from dao.userDao import UserDao
from model.ForgotPassword import ForgotPassword
from model.ForgotPasswordData import ForgotPasswordData
from model.User import User

forgot_password_route = Blueprint('forgot_password_route', __name__, url_prefix='/v2/forgot_password')


@forgot_password_route.route('/<username>', methods=['GET', 'POST'])
@auth_required()
def forgot_password(username) -> Response:
    """
    Endpoints for retrieving or creating a forgot password code
    :param username: Username which uniquely identifies a User
    :return: JSON representation of a forgot password code and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /v2/forgot_password/<username|email> '''
        return forgot_password_get(username)
    if request.method == 'POST':
        ''' [POST] /v2/forgot_password/<username|email> '''
        return forgot_password_post(username)


@forgot_password_route.route('/validate/<code>', methods=['GET'])
@auth_required()
def forgot_password_code_validation(code) -> Response:
    """
    Endpoints for validating whether or not a forgot password code exists.
    :param code: Forgot password code which will be validated
    :return: JSON representation of validation results and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /v2/forgot_password/validate/<code> '''
        return forgot_password_validate_code_get(code)


@forgot_password_route.route('/links', methods=['GET'])
def forgot_password_links() -> Response:
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
    user: User = UserDao.get_user_by_username(username=username)

    # If the user cant be found, try searching the email column in the database
    if user is None:
        email = username
        user: User = UserDao.get_user_by_email(email=email)

    if user is None:
        response = jsonify({
            'self': f'/v2/forgot_password/{username}',
            'forgot_password_codes': [],
            'error': 'There is no user associated with this username/email.'
        })
        response.status_code = 400
        return response

    forgot_password_codes: ResultProxy = ForgotPasswordDao.get_forgot_password_codes(username=user.username)

    if forgot_password_codes is None:
        response = jsonify({
            'self': f'/v2/forgot_password/{username}',
            'forgot_password_codes': [],
            'error': 'This user has no forgot password codes.'
        })
        response.status_code = 400
        return response
    else:
        forgot_password_list = []
        for code in forgot_password_codes:
            fpw = ForgotPasswordData(None)
            fpw.forgot_code = code[0]
            fpw.username = code[1]
            fpw.expires = code[2]
            fpw.deleted = code[3]
            forgot_password_list.append(fpw.__dict__)

        response = jsonify({
            'self': f'/v2/forgot_password/{username}',
            'forgot_password_codes': forgot_password_list,
        })
        response.status_code = 200
        return response


def forgot_password_post(username) -> Response:
    """
    Create a new forgot password code for a specific user.
    :param username: Uniquely identifies a user.
    :return: JSON with the resulting Forgot Password object and relevant metadata.
    """
    user: User = UserDao.get_user_by_username(username=username)

    # If the user cant be found, try searching the email column in the database
    if user is None:
        email = username
        user: User = UserDao.get_user_by_email(email=email)

    if user is None:
        response = jsonify({
            'self': f'/v2/forgot_password/{username}',
            'inserted': False,
            'error': 'There is no user associated with this username/email.'
        })
        response.status_code = 400
        return response

    code = generate_code(length=8)
    expires = datetime.now() + timedelta(hours=2)

    new_forgot_password = ForgotPassword({
        'forgot_code': code,
        'username': user.username,
        'expires': expires
    })

    new_forgot_password.created_date = datetime.now()
    new_forgot_password.created_app = 'saints-xctf-api'
    new_forgot_password.created_user = None
    new_forgot_password.modified_date = None
    new_forgot_password.modified_app = None
    new_forgot_password.modified_user = None
    new_forgot_password.deleted_date = None
    new_forgot_password.deleted_app = None
    new_forgot_password.deleted_user = None
    new_forgot_password.deleted = False

    forgot_password_inserted = ForgotPasswordDao.add_forgot_password_code(new_forgot_password)

    if forgot_password_inserted:
        new_forgot_password = ForgotPasswordDao.get_forgot_password_code(code)

        response = jsonify({
            'self': f'/v2/forgot_password/{username}',
            'inserted': True,
            'forgot_password_code': new_forgot_password.forgot_code,
            'username': user.username,
            'first_name': user.first,
            'last_name': user.last
        })
        response.status_code = 201
        return response
    else:
        response = jsonify({
            'self': f'/v2/forgot_password/{username}',
            'inserted': False,
            'error': 'An unexpected error occurred.'
        })
        response.status_code = 500
        return response


def forgot_password_validate_code_get(code: str) -> Response:
    """
    Validate a forgot password code.
    :param code: Forgot password code which will be validated.
    :return: JSON with the validation results and relevant metadata.
    """
    forgot_password_code = ForgotPasswordDao.get_forgot_password_code(code)

    response = jsonify({
        'self': f'/v2/forgot_password/validate/{code}',
        'is_valid': forgot_password_code is not None
    })
    response.status_code = 200
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
            },
            {
                'link': '/v2/forgot_password/validate/<code>',
                'verb': 'GET',
                'description': 'Validate if a forgot password code exists.'
            }
        ],
    })
    response.status_code = 200
    return response
