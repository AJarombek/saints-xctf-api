"""
User routes in the SaintsXCTF API.  Used for retrieving and updating application users.
Author: Andrew Jarombek
Date: 6/16/2019
"""

from flask import Blueprint, request, jsonify, current_app
from bcrypt import bcrypt
from dao.userDao import UserDao
from dao.groupDao import GroupDao
from dao.groupMemberDao import GroupMemberDao
from dao.forgotPasswordDao import ForgotPasswordDao
from dao.flairDao import FlairDao
from dao.notificationDao import NotificationDao
from dao.logDao import LogDao
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
        ''' [GET] /v2/users '''
        all_users = UserDao.get_users()
        all_users = map(lambda user: user.update({'this_user': f'/v2/users/{user.get("username")}'}), all_users)

        return jsonify({
            'self': '/v2/users',
            'users': all_users
        })

    elif request.method == 'POST':
        ''' [POST] /v2/users '''
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
                    'user': None,
                    'error': 'an unexpected error occurred creating the user'
                })
                response.status_code = 500
                return response
            else:
                response = jsonify({
                    'self': '/v2/users',
                    'user': added_user,
                    'new_user': f'/v2/users/{added_user.username}'
                })
                response.status_code = 201
                return response
        else:
            current_app.logger.error('Failed to create new User: The Activation Code does not exist.')
            response = jsonify({
                'self': '/v2/users',
                'user': None,
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
        ''' [GET] /v2/users/<username> '''
        user = UserDao.get_user_by_username(username=username)

        # If the user cant be found, try searching the email column in the database
        if user is None:
            email = username
            user = UserDao.get_user_by_email(email=email)

        # If the user still can't be found, return with an error code
        if user is None:
            return jsonify({
                'self': f'/v2/users/{username}',
                'user': None
            })
        else:
            return jsonify({
                'self': f'/v2/users/{username}',
                'user': user
            })

    elif request.method == 'PUT':
        ''' [PUT] /v2/users/<username> '''
        old_user = UserDao.get_user_by_username(username=username)

        user_data: dict = request.get_json()
        new_user = User(user_data)

        if new_user != old_user:
            is_updated = UserDao.update_user(username, new_user)

            if is_updated:
                updated_user = UserDao.get_user_by_username(username)

                response = jsonify({
                    'self': f'/v2/users/{username}',
                    'updated': True,
                    'user': updated_user
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
                'error': 'the user submitted is equal to the existing user'
            })
            response.status_code = 400
            return response

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/users/<username> '''
        is_deleted = UserDao.delete_user(username=username)

        if is_deleted:
            status_code = 204
        else:
            status_code = 500

        response = jsonify({
            'self': f'/v2/users/{username}',
            'deleted': is_deleted
        })
        response.status_code = status_code
        return response


@user_route.route('/snapshot/<username>', methods=['GET'])
def user_snapshot(username):
    """
    Endpoint for a website snapshot for a specific user.  Provides more details than the base user route,
    such as group memberships and statistics.
    :param username: Username (or email) of a User
    :return: JSON representation of a user and relevant metadata
    """
    user = UserDao.get_user_by_username(username=username)

    # If the user cant be found, try searching the email column in the database
    if user is None:
        email = username
        user = UserDao.get_user_by_email(email=email)

    # If the user still can't be found, return with an error code
    if user is None:
        return jsonify({
            'self': f'/v2/users/{username}',
            'user': False
        })
    else:
        username = user['username']
        groups = GroupMemberDao.get_user_groups(username=username)

        for group in groups:
            newest_log = GroupDao.get_newest_log_date(group['group_name'])
            group['newest_log'] = newest_log

            newest_message = GroupDao.get_newest_message_date(group['group_name'])
            group['newest_message'] = newest_message

        user['groups'] = groups

        forgot_password = ForgotPasswordDao.get_forgot_password_codes(username=username)
        user['forgotpassword'] = forgot_password

        flair = FlairDao.get_flair_by_username(username=username)
        user['flair'] = flair

        notifications = NotificationDao.get_notification_by_username(username=username)
        user['notifications'] = notifications

        # All user statistics are queried separately but combined into a single map
        miles = LogDao.get_user_miles(username)
        miles_past_year = LogDao.get_user_miles_interval(username, 'year')
        miles_past_month = LogDao.get_user_miles_interval(username, 'month')
        miles_past_week = LogDao.get_user_miles_interval(username, 'week', week_start=user['week_start'])
        run_miles = LogDao.get_user_miles_interval_by_type(username, 'run')
        run_miles_past_year = LogDao.get_user_miles_interval_by_type(username, 'run', 'year')
        run_miles_past_month = LogDao.get_user_miles_interval_by_type(username, 'run', 'month')
        run_miles_past_week = LogDao.get_user_miles_interval_by_type(username, 'run', 'week')
        all_time_feel = LogDao.get_user_avg_feel(username)
        year_feel = LogDao.get_user_avg_feel_interval(username, 'year')
        month_feel = LogDao.get_user_avg_feel_interval(username, 'month')
        week_feel = LogDao.get_user_avg_feel_interval(username, 'week', week_start=user['week_start'])

        stats = {
            'miles': miles,
            'milespastyear': miles_past_year,
            'milespastmonth': miles_past_month,
            'milespastweek': miles_past_week,
            'runmiles': run_miles,
            'runmilespastyear': run_miles_past_year,
            'runmilespastmonth': run_miles_past_month,
            'runmilespastweek': run_miles_past_week,
            'alltimefeel': all_time_feel,
            'yearfeel': year_feel,
            'monthfeel': month_feel,
            'weekfeel': week_feel
        }

        user['statistics'] = stats

        return jsonify({
            'self': f'/v2/users/{username}',
            'user': user
        })


@user_route.route('/<username>/change_password', methods=['PUT'])
def user_change_password(username):
    """
    Endpoint for changing a users password.
    :param username: Username which uniquely identifies a user.
    :return: JSON with the result of the password change.
    """
    # Request should use the following pattern: {"forgot_password_code": "...", "new_password": "..."}
    request_dict: dict = request.get_json()
    forgot_password_code = request_dict.get('forgot_password_code')
    new_password = request_dict.get('new_password')

    hashed_password = bcrypt.generate_password_hash(new_password)

    password_updated = UserDao.update_user_password(username, hashed_password)

    if password_updated:
        code_deleted = ForgotPasswordDao.delete_forgot_password_code(code=forgot_password_code)
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


@user_route.route('/<username>/update_last_login', methods=['PUT'])
def user_update_last_login(username):
    """
    Update the date of a users previous sign in.
    :param username: Username which uniquely identifies a user.
    :return: JSON with the result of the last login update
    """
    last_login_updated = UserDao.update_user_last_login(username)
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
