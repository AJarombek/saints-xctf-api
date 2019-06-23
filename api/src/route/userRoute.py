"""
User routes in the SaintsXCTF API.  Used for retrieving and updating application users.
Author: Andrew Jarombek
Date: 6/16/2019
"""

from flask import Blueprint, request, jsonify
from dao.userDao import UserDao

user_route = Blueprint('user_route', __name__, url_prefix='/v1/user')


@user_route.route('/', methods=['GET'])
def users():
    pass


@user_route.route('/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user(username):
    if request.method == 'GET':
        user = UserDao.get_user_by_username(username=username)

        # If the user cant be found, try searching the email column in the database
        if user is None:
            email = username
            user = UserDao.get_user_by_email(email=email)

        # If the user still can't be found, return with an error code
        if user is None:
            return jsonify({
                'self': f'{base_url}/v1/user'
            })