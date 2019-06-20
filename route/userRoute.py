"""
User routes in the SaintsXCTF API.  Used for retrieving and updating application users.
Author: Andrew Jarombek
Date: 6/16/2019
"""

from flask import Blueprint, request
from dao.userDao import UserDao

mail_route = Blueprint('user_route', __name__, url_prefix='/user')


@mail_route.route('/', methods=['GET'])
def users():
    pass


@mail_route.route('/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user(username):
    if request.method == 'GET':
        user_dao = UserDao()
        user = user_dao.get_user_by_username(username=username)
        return
