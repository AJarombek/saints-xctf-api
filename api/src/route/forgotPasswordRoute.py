"""
ForgotPassword routes in the SaintsXCTF API.  Used for retrieving, creating,
and deleting forgot password codes for users.
Author: Andrew Jarombek
Date: 7/4/2019
"""

from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from utils.codes import generate_code
from dao.forgotPasswordDao import ForgotPasswordDao
from model.ForgotPassword import ForgotPassword

forgot_password_route = Blueprint('forgot_password_route', __name__, url_prefix='/v2/forgot_password')


@forgot_password_route.route('/<username>', methods=['GET', 'POST'])
def forgot_password(username):
    """
    Endpoints for retrieving or creating a forgot password code
    :param username: Username which uniquely identifies a User
    :return: JSON representation of a forgot password code and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /v2/forgot_password/<username> '''
        pass
    if request.method == 'POST':
        ''' [POST] /v2/forgot_password/<username> '''
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
                'updated': True,
                'user': new_forgot_password
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': f'/v2/forgot_password/{username}',
                'inserted': False,
                'error': 'the forgot password code creation failed'
            })
            response.status_code = 500
            return response
