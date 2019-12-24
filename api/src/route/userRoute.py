"""
User routes in the SaintsXCTF API.  Used for retrieving and updating application users.
Author: Andrew Jarombek
Date: 6/16/2019
"""

from flask import Blueprint, request, jsonify, current_app, Response, redirect, url_for
from sqlalchemy.schema import Column
from sqlalchemy.engine import ResultProxy
from datetime import datetime
from flaskBcrypt import flask_bcrypt
from dao.userDao import UserDao
from dao.groupDao import GroupDao
from dao.groupMemberDao import GroupMemberDao
from dao.forgotPasswordDao import ForgotPasswordDao
from dao.flairDao import FlairDao
from dao.notificationDao import NotificationDao
from dao.logDao import LogDao
from model.Code import Code
from model.FlairData import FlairData
from model.User import User
from model.UserData import UserData
from dao.codeDao import CodeDao

user_route = Blueprint('user_route', __name__, url_prefix='/v2/users')


@user_route.route('', methods=['GET', 'POST'])
def users_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'users' to the user routes.
    :return: Response object letting the caller know where to redirect the request to.
    """
    if request.method == 'GET':
        ''' [GET] /v2/users '''
        return redirect(url_for('user_route.users'), code=302)

    elif request.method == 'POST':
        ''' [POST] /v2/users '''
        return redirect(url_for('user_route.users'), code=307)


@user_route.route('/', methods=['GET', 'POST'])
def users() -> Response:
    """
    Endpoints for searching all the users or creating a user
    :return: JSON representation of a list of users and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/ '''
        return users_get()

    elif request.method == 'POST':
        ''' [POST] /v2/users/ '''
        return user_post()


@user_route.route('/<username>', methods=['GET', 'PUT', 'DELETE'])
def user(username) -> Response:
    """
    Endpoints for specific users (searching, updating, or deleting)
    :param username: Username (or email) of a User
    :return: JSON representation of a user and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/<username> '''
        return user_by_username_get(username)

    elif request.method == 'PUT':
        ''' [PUT] /v2/users/<username> '''
        return user_by_username_put(username)

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/users/<username> '''
        return user_by_username_delete(username)


@user_route.route('/soft/<username>', methods=['DELETE'])
def user_soft_by_username(username) -> Response:
    """
    Endpoints for soft deleting a user.
    :param username: Username of a User.
    :return: JSON representation of users and relevant metadata.
    """
    if request.method == 'DELETE':
        ''' [DELETE] /v2/users/soft/<username> '''
        return user_by_username_soft_delete(username)


@user_route.route('/snapshot/<username>', methods=['GET'])
def user_snapshot(username) -> Response:
    """
    Endpoint for a website snapshot for a specific user.  Provides more details than the base user route,
    such as group memberships and statistics.
    :param username: Username (or email) of a User
    :return: JSON representation of a user and relevant metadata
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/snapshot/<username> '''
        return user_snapshot_by_username_get(username)


@user_route.route('/<username>/change_password', methods=['PUT'])
def user_change_password(username) -> Response:
    """
    Endpoint for changing a users password.
    :param username: Username which uniquely identifies a user.
    :return: JSON with the result of the password change.
    """
    if request.method == 'PUT':
        ''' [GET] /v2/users/<username>/change_password '''
        return user_change_password_by_username_put(username)


@user_route.route('/<username>/update_last_login', methods=['PUT'])
def user_update_last_login(username) -> Response:
    """
    Update the date of a users previous sign in.
    :param username: Username which uniquely identifies a user.
    :return: JSON with the result of the last login update
    """
    if request.method == 'PUT':
        ''' [PUT] /v2/users/<username>/update_last_login'''
        return user_update_last_login_by_username_put(username)


@user_route.route('/links', methods=['GET'])
def user_links() -> Response:
    """
    Endpoint for information about the user API endpoints.
    :return: Metadata about the user API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/links '''
        return user_links_get()


def users_get() -> Response:
    """
    Retrieve all the users in the database.
    :return: A response object for the GET API request.
    """
    all_users: list = UserDao.get_users()

    if all_users is None:
        response = jsonify({
            'self': '/v2/users',
            'users': None,
            'error': 'an unexpected error occurred retrieving users'
        })
        response.status_code = 500
        return response
    else:
        user_dicts = []

        for user in all_users:
            user_dict = UserData(user).__dict__
            user_dict['this_user'] = f'/v2/users/{user_dict["username"]}'

            if user_dict.get('member_since') is not None:
                user_dict['member_since'] = str(user_dict['member_since'])
            if user_dict.get('last_signin') is not None:
                user_dict['last_signin'] = str(user_dict['last_signin'])

            if user_dict['profilepic'] is not None:
                try:
                    user_dict['profilepic'] = user_dict['profilepic'].decode('utf-8')
                except AttributeError:
                    pass

            user_dicts.append(user_dict)

        response = jsonify({
            'self': '/v2/users',
            'users': user_dicts
        })
        response.status_code = 200
        return response


def user_post() -> Response:
    """
    Create a new user.
    :return: A response object for the POST API request.
    """
    user_data: dict = request.get_json()

    if user_data is None:
        response = jsonify({
            'self': f'/v2/users',
            'added': False,
            'user': None,
            'error': "the request body isn't populated"
        })
        response.status_code = 400
        return response

    user_to_add = User(user_data)

    if None in [user_to_add.username, user_to_add.first, user_to_add.last, user_to_add.password,
                user_to_add.activation_code]:
        response = jsonify({
            'self': f'/v2/users',
            'added': False,
            'user': None,
            'error': "'username', 'first', 'last', 'password', and 'activation_code' are required fields"
        })
        response.status_code = 400
        return response

    # Passwords must be hashed before stored in the database
    password = user_to_add.password
    hashed_password = flask_bcrypt.generate_password_hash(password).decode('utf-8')
    user_to_add.password = hashed_password

    activation_code_count = CodeDao.get_code_count(activation_code=user_to_add.activation_code)

    if activation_code_count == 1:
        now = datetime.now()
        user_to_add.member_since = now.date()
        user_to_add.created_date = now
        user_to_add.last_signin = now
        user_to_add.created_app = 'api'

        # First add the user since its activation code is valid
        UserDao.add_user(user_to_add)
        # Second remove the activation code so it cant be used again
        code = Code({'activation_code': user_to_add.activation_code})
        CodeDao.remove_code(code)

        added_user = UserDao.get_user_by_username(user_to_add.username)

        if added_user is None:
            response = jsonify({
                'self': '/v2/users',
                'added': False,
                'user': None,
                'error': 'an unexpected error occurred creating the user'
            })
            response.status_code = 500
            return response
        else:
            response = jsonify({
                'self': '/v2/users',
                'added': True,
                'user': UserData(added_user).__dict__,
                'new_user': f'/v2/users/{added_user.username}'
            })
            response.status_code = 201
            return response
    else:
        current_app.logger.error('Failed to create new User: The Activation Code does not exist.')
        response = jsonify({
            'self': '/v2/users',
            'added': False,
            'user': None,
            'error': 'the activation code does not exist'
        })
        response.status_code = 400
        return response


def user_by_username_get(username) -> Response:
    """
    Retrieve a user based on its username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    user: User = UserDao.get_user_by_username(username=username)

    # If the user cant be found, try searching the email column in the database
    if user is None:
        email = username
        user: User = UserDao.get_user_by_email(email=email)

    # If the user still can't be found, return with an error code
    if user is None:
        response = jsonify({
            'self': f'/v2/users/{username}',
            'user': None,
            'error': 'there is no user with this username'
        })
        response.status_code = 400
        return response
    else:
        user_dict: dict = UserData(user).__dict__

        if user_dict.get('member_since') is not None:
            user_dict['member_since'] = str(user_dict['member_since'])
        if user_dict.get('last_signin') is not None:
            user_dict['last_signin'] = str(user_dict['last_signin'])

        if user_dict['profilepic'] is not None:
            try:
                user_dict['profilepic'] = user_dict['profilepic'].decode('utf-8')
            except AttributeError:
                pass

        response = jsonify({
            'self': f'/v2/users/{username}',
            'user': user_dict
        })
        response.status_code = 200
        return response


def user_by_username_put(username) -> Response:
    """
    Update an existing user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the PUT API request.
    """
    old_user: User = UserDao.get_user_by_username(username=username)

    if old_user is None:
        response = jsonify({
            'self': f'/v2/users/{username}',
            'updated': False,
            'user': None,
            'error': 'there is no existing user with this username'
        })
        response.status_code = 400
        return response

    user_data: dict = request.get_json()
    new_user = User(user_data)

    if new_user != old_user:
        is_updated = UserDao.update_user(username, new_user)

        if is_updated:
            updated_user = UserDao.get_user_by_username(username)

            updated_user_dict: dict = UserData(updated_user).__dict__

            if updated_user_dict['profilepic'] is not None:
                try:
                    updated_user_dict['profilepic'] = updated_user_dict['profilepic'].decode('utf-8')
                except AttributeError:
                    pass

            response = jsonify({
                'self': f'/v2/users/{username}',
                'updated': True,
                'user': updated_user_dict
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': f'/v2/users/{username}',
                'updated': False,
                'user': None,
                'error': 'the user failed to update'
            })
            response.status_code = 500
            return response
    else:
        response = jsonify({
            'self': f'/v2/users/{username}',
            'updated': False,
            'user': None,
            'error': 'the user submitted is equal to the existing user with the same username'
        })
        response.status_code = 400
        return response


def user_by_username_delete(username) -> Response:
    """
    Hard delete an existing user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the DELETE API request.
    """
    is_deleted = UserDao.delete_user(username=username)

    if is_deleted:
        response = jsonify({
            'self': f'/v2/users/{username}',
            'deleted': True,
        })
        response.status_code = 204
        return response
    else:
        response = jsonify({
            'self': f'/v2/users/{username}',
            'deleted': False,
            'error': 'failed to delete the user'
        })
        response.status_code = 500
        return response


def user_by_username_soft_delete(username) -> Response:
    """
    Soft delete an existing user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the DELETE API request.
    """
    existing_user: User = UserDao.get_user_by_username(username=username)

    if existing_user is None:
        response = jsonify({
            'self': f'/v2/users/soft/{username}',
            'deleted': False,
            'error': 'there is no existing user with this username'
        })
        response.status_code = 400
        return response

    if existing_user.deleted == 'Y':
        response = jsonify({
            'self': f'/v2/users/soft/{username}',
            'deleted': False,
            'error': 'this user is already soft deleted'
        })
        response.status_code = 400
        return response

    # Update the user model to reflect the soft delete
    existing_user.deleted = 'Y'
    existing_user.deleted_date = datetime.now()
    existing_user.deleted_app = 'api'
    existing_user.modified_date = datetime.now()
    existing_user.modified_app = 'api'

    is_deleted: bool = UserDao.soft_delete_user(existing_user)

    if is_deleted:
        response = jsonify({
            'self': f'/v2/users/soft/{username}',
            'deleted': True,
        })
        response.status_code = 204
        return response
    else:
        response = jsonify({
            'self': f'/v2/users/soft/{username}',
            'deleted': False,
            'error': 'failed to soft delete the user'
        })
        response.status_code = 500
        return response


def user_snapshot_by_username_get(username) -> Response:
    """
    Get a snapshot with information about a user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    user: User = UserDao.get_user_by_username(username=username)

    # If the user cant be found, try searching the email column in the database
    if user is None:
        email = username
        user: User = UserDao.get_user_by_email(email=email)

    # If the user still can't be found, return with an error code
    if user is None:
        response = jsonify({
            'self': f'/v2/users/snapshot/{username}',
            'user': None,
            'error': 'there is no user with this username'
        })
        response.status_code = 400
        return response
    else:
        user_dict: dict = UserData(user).__dict__

        if user_dict.get('member_since') is not None:
            user_dict['member_since'] = str(user_dict['member_since'])
        if user_dict.get('last_signin') is not None:
            user_dict['last_signin'] = str(user_dict['last_signin'])

        if user_dict['profilepic'] is not None:
            try:
                user_dict['profilepic'] = user_dict['profilepic'].decode('utf-8')
            except AttributeError:
                pass

        username = user_dict['username']
        groups: ResultProxy = GroupMemberDao.get_user_groups(username=username)
        group_list = []

        for group in groups:
            grout_dict = {
                'group_name': group['group_name'],
                'group_title': group['group_title'],
                'status': group['status'],
                'user': group['user']
            }
            newest_log: Column = GroupDao.get_newest_log_date(group['group_name'])
            grout_dict['newest_log'] = newest_log['newest']

            newest_message = GroupDao.get_newest_message_date(group['group_name'])
            grout_dict['newest_message'] = newest_message['newest']

            group_list.append(grout_dict)

        user_dict['groups'] = group_list

        forgot_password_codes: ResultProxy = ForgotPasswordDao.get_forgot_password_codes(username=username)

        forgot_password_list = []
        for forgot_password_code in forgot_password_codes:
            forgot_password_list.append({
                'forgot_code': forgot_password_code['forgot_code'],
                'username': forgot_password_code['username'],
                'expires': forgot_password_code['expires'],
                'deleted': forgot_password_code['deleted'],
            })

        user_dict['forgotpassword'] = forgot_password_list

        flairs: list = FlairDao.get_flair_by_username(username=username)
        flair_dicts = []

        for flair in flairs:
            flair_dicts.append(FlairData(flair).__dict__)

        user_dict['flair'] = flair_dicts

        notifications: ResultProxy = NotificationDao.get_notification_by_username(username=username)

        notification_dicts = []
        for notification in notifications:
            notification_dicts.append({
                'notification_id': notification['notification_id'],
                'username': notification['username'],
                'time': notification['time'],
                'link': notification['link'],
                'viewed': notification['viewed'],
                'description': notification['description'],
                'deleted': notification['deleted']
            })

        user_dict['notifications'] = notification_dicts

        # All user statistics are queried separately but combined into a single map
        miles: Column = LogDao.get_user_miles(username)
        miles_past_year: Column = LogDao.get_user_miles_interval(username, 'year')
        miles_past_month: Column = LogDao.get_user_miles_interval(username, 'month')
        miles_past_week: Column = LogDao.get_user_miles_interval(username, 'week', week_start=user.week_start)
        run_miles: Column = LogDao.get_user_miles_interval_by_type(username, 'run')
        run_miles_past_year: Column = LogDao.get_user_miles_interval_by_type(username, 'run', 'year')
        run_miles_past_month: Column = LogDao.get_user_miles_interval_by_type(username, 'run', 'month')
        run_miles_past_week: Column = LogDao.get_user_miles_interval_by_type(username, 'run', 'week')
        all_time_feel: Column = LogDao.get_user_avg_feel(username)
        year_feel: Column = LogDao.get_user_avg_feel_interval(username, 'year')
        month_feel: Column = LogDao.get_user_avg_feel_interval(username, 'month')
        week_feel: Column = LogDao.get_user_avg_feel_interval(username, 'week', week_start=user.week_start)

        stats = {
            'miles': miles['total'],
            'milespastyear': miles_past_year['total'],
            'milespastmonth': miles_past_month['total'],
            'milespastweek': miles_past_week['total'],
            'runmiles': run_miles['total'],
            'runmilespastyear': run_miles_past_year['total'],
            'runmilespastmonth': run_miles_past_month['total'],
            'runmilespastweek': run_miles_past_week['total'],
            'alltimefeel': all_time_feel['average'],
            'yearfeel': year_feel['average'],
            'monthfeel': month_feel['average'],
            'weekfeel': week_feel['average']
        }

        user_dict['statistics'] = stats

        response = jsonify({
            'self': f'/v2/users/snapshot/{username}',
            'user': user_dict
        })
        response.status_code = 200
        return response


def user_change_password_by_username_put(username) -> Response:
    """
    Change the password of a user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    # Request should use the following pattern: {"forgot_password_code": "...", "new_password": "..."}
    request_dict: dict = request.get_json()
    forgot_password_code = request_dict.get('forgot_password_code')
    new_password = request_dict.get('new_password')

    if forgot_password_code is None or new_password is None:
        response = jsonify({
            'self': f'/v2/users/{username}/change_password',
            'password_updated': False,
            'forgot_password_code_deleted': False,
            'error': "'forgot_password_code' and 'new_password' are required fields"
        })
        response.status_code = 500
        return response

    hashed_password = flask_bcrypt.generate_password_hash(new_password).decode('utf-8')

    password_updated: bool = UserDao.update_user_password(username, hashed_password)

    if password_updated:
        code_deleted: bool = ForgotPasswordDao.delete_forgot_password_code(code=forgot_password_code)
        response = jsonify({
            'self': f'/v2/users/{username}/change_password',
            'password_updated': True,
            'forgot_password_code_deleted': code_deleted
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            'self': f'/v2/users/{username}/change_password',
            'password_updated': False,
            'forgot_password_code_deleted': False,
            'error': 'an unexpected error occurred changing passwords'
        })
        response.status_code = 500
        return response


def user_update_last_login_by_username_put(username) -> Response:
    """
    Change the last login date of a user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the PUT API request.
    """
    last_login_updated: bool = UserDao.update_user_last_login(username)
    if last_login_updated:
        response = jsonify({
            'self': f'/v2/users/{username}/update_last_login',
            'last_login_updated': True
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            'self': f'/v2/users/{username}/update_last_login',
            'last_login_updated': False,
            'error': 'an unexpected error occurred updating the users last login date'
        })
        response.status_code = 500
        return response


def user_links_get() -> Response:
    """
    Get all the other user API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/users/links',
        'endpoints': [
            {
                'link': '/v2/users',
                'verb': 'GET',
                'description': 'Get all the users in the database.'
            },
            {
                'link': '/v2/users',
                'verb': 'POST',
                'description': 'Create a new user.'
            },
            {
                'link': '/v2/users/<username>',
                'verb': 'GET',
                'description': 'Retrieve a single user with a given username.'
            },
            {
                'link': '/v2/users/<username>',
                'verb': 'PUT',
                'description': 'Update a user with a given username.'
            },
            {
                'link': '/v2/users/<username>',
                'verb': 'DELETE',
                'description': 'Delete a user with a given username.'
            },
            {
                'link': '/v2/users/soft/<username>',
                'verb': 'DELETE',
                'description': 'Soft delete a user with a given username.'
            },
            {
                'link': '/v2/users/snapshot/<username>',
                'verb': 'GET',
                'description': 'Get a snapshot about a user and their exercise statistics with a given username.'
            },
            {
                'link': '/v2/users/<username>/change_password',
                'verb': 'PUT',
                'description': 'Update a user with a given username.  Specifically, alter the users password.'
            },
            {
                'link': '/v2/users/<username>/update_last_login',
                'verb': 'PUT',
                'description': 'Update a user with a given username.  Specifically, change the users last login date.'
            }
        ],
    })
    response.status_code = 200
    return response
