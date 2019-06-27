"""
User routes in the SaintsXCTF API.  Used for retrieving and updating application users.
Author: Andrew Jarombek
Date: 6/16/2019
"""

from app import app, bcrypt
from flask import Blueprint, request, jsonify
from dao.userDao import UserDao
from model.Code import Code
from model.User import User
from dao.codeDao import CodeDao

user_route = Blueprint('user_route', __name__, url_prefix='/v2/users')


@user_route.route('/', methods=['GET', 'POST'])
def users():
    """
    Endpoints for searching all the users or creating a user
    :return: JSON representation of a list of users and relevant metadata
    """
    if request.method == 'GET':
        all_users = UserDao.get_users()

        return jsonify({
            'self': '/v2/users',
            'users': all_users
        })

    elif request.method == 'POST':
        user_data: dict = request.get_json()

        # Passwords must be hashed before stored in the database
        password = user_data.get('password')
        hashed_password = bcrypt.generate_password_hash(password)
        user_data.password = hashed_password

        user_to_add = User(user_data)

        activation_code_count = CodeDao.get_code_count(activation_code=user_to_add.activation_code)

        if activation_code_count == 1:
            # First add the user since its activation code is valid
            UserDao.add_user(user_to_add)
            # Second remove the activation code so it cant be used again
            code = Code(activation_code=user.activation_code)
            CodeDao.remove_code(code)

            added_user = UserDao.get_user_by_username(user_to_add.username)

            if added_user is None:
                response = jsonify({
                    'self': '/v2/users',
                    'users': None,
                    'error': 'an unexpected error occurred creating the user'
                })
                response.status_code = 500
                return response
            else:
                response = jsonify({
                    'self': '/v2/users',
                    'users': added_user,
                    'new_user': f'/v2/users/{added_user.username}'
                })
                response.status_code = 201
                return response
        else:
            app.logger.error('Failed to create new User: The Activation Code does not exist.')
            response = jsonify({
                'self': '/v2/users',
                'users': None,
                'error': 'the activation code does not exist'
            })
            response.status_code = 400
            return response


@user_route.route('/<username>', methods=['GET', 'PUT', 'DELETE'])
def user(username):
    """
    Endpoints for specific users (searching, updating, or deleting)
    :param username: Username (or email) of a User
    :return: JSON representation of a user and relevant metadata
    """
    if request.method == 'GET':
        user = UserDao.get_user_by_username(username=username)

        # If the user cant be found, try searching the email column in the database
        if user is None:
            email = username
            user = UserDao.get_user_by_email(email=email)

        # If the user still can't be found, return with an error code
        if user is None:
            return jsonify({
                'self': f'/v2/users/{username}',
                'users': False
            })

    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
