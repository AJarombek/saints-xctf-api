"""
User routes in the SaintsXCTF API.  Used for retrieving and updating application users.
So much love for you here <3
Author: Andrew Jarombek
Date: 6/16/2019
"""

import re
from datetime import datetime
from typing import List

from flask import Blueprint, request, jsonify, current_app, Response, redirect, url_for
from sqlalchemy.schema import Column
from sqlalchemy.engine import ResultProxy
from sqlalchemy.exc import SQLAlchemyError
from flaskBcrypt import flask_bcrypt

from decorators import auth_required, disabled, DELETE, GET
from utils.jwt import get_claims
from dao.userDao import UserDao
from dao.groupDao import GroupDao
from dao.groupMemberDao import GroupMemberDao
from dao.forgotPasswordDao import ForgotPasswordDao
from dao.flairDao import FlairDao
from dao.notificationDao import NotificationDao
from dao.logDao import LogDao
from dao.teamMemberDao import TeamMemberDao
from dao.codeDao import CodeDao
from dao.activationCodeDao import ActivationCodeDao
from dao.teamDao import TeamDao
from model.Code import Code
from model.FlairData import FlairData
from model.Flair import Flair
from model.User import User
from model.UserData import UserData
from model.ForgotPassword import ForgotPassword
from model.Team import Team
from model.Group import Group

user_route = Blueprint('user_route', __name__, url_prefix='/v2/users')


@user_route.route('', methods=['GET', 'POST'])
@auth_required(enabled_methods=[GET])
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
@auth_required(enabled_methods=[GET])
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
@auth_required()
@disabled(disabled_methods=[DELETE])
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
@auth_required()
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
@auth_required()
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


@user_route.route('/groups/<username>', methods=['GET'])
@auth_required()
def user_groups(username) -> Response:
    """
    Endpoint for retrieving a user's group memberships.
    :param username: Username (or email) of a User
    :return: JSON representation of a list of group memberships
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/groups/<username> '''
        return user_groups_by_username_get(username)


@user_route.route('/teams/<username>', methods=['GET'])
@auth_required()
def user_teams(username) -> Response:
    """
    Endpoint for retrieving a user's team memberships.
    :param username: Username (or email) of a User
    :return: JSON representation of a list of team memberships
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/teams/<username> '''
        return user_teams_by_username_get(username)


@user_route.route('/memberships/<username>', methods=['GET', 'PUT'])
@auth_required()
def user_memberships(username) -> Response:
    """
    Endpoint for retrieving a user's team and group memberships.
    :param username: Username (or email) of a User
    :return: JSON representation of a list of team memberships with nested group memberships
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/memberships/<username> '''
        return user_memberships_by_username_get(username)
    elif request.method == 'PUT':
        ''' [PUT] /v2/users/memberships/<username> '''
        return user_memberships_by_username_put(username)


@user_route.route('/notifications/<username>', methods=['GET'])
@auth_required()
def user_notifications(username) -> Response:
    """
    Endpoint for retrieving a user's notifications.
    :param username: Username (or email) of a User
    :return: JSON representation of a list of notifications
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/notifications/<username> '''
        return user_notifications_by_username_get(username)


@user_route.route('/flair/<username>', methods=['GET'])
@auth_required()
def user_flair(username) -> Response:
    """
    Endpoint for retrieving a user's flair.
    :param username: Username (or email) of a User
    :return: JSON representation of a list of flair objects
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/flair/<username> '''
        return user_flair_by_username_get(username)


@user_route.route('/statistics/<username>', methods=['GET'])
@auth_required()
def user_statistics(username) -> Response:
    """
    Endpoint for retrieving a user's statistics.
    :param username: Username (or email) of a User
    :return: JSON representation of a users exercise statistics.
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/statistics/<username> '''
        return user_statistics_by_username_get(username)


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
@auth_required()
def user_update_last_login(username) -> Response:
    """
    Update the date of a users previous sign in.
    :param username: Username which uniquely identifies a user.
    :return: JSON with the result of the last login update
    """
    if request.method == 'PUT':
        ''' [PUT] /v2/users/<username>/update_last_login'''
        return user_update_last_login_by_username_put(username)


@user_route.route('/lookup/<username>', methods=['GET'])
def user_lookup(username) -> Response:
    """
    Endpoint for looking up a username/email to see if its currently in use.  This endpoint is used while a user is
    registering, before they have access to view other user's details.
    :param username: Username (or email) of a User.
    :return: JSON representation of the result of a user lookup.
    """
    if request.method == 'GET':
        ''' [GET] /v2/users/lookup/<username> '''
        return user_lookup_by_username_get(username)


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

            if user_dict.get('profilepic') is not None:
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

    def create_validation_error_response(message: str):
        """
        Reusable 400 HTTP error response for the users POST request.
        :param message: Message sent in the response JSON's 'error' field.
        :return: An HTTP response object.
        """
        error_response = jsonify({
            'self': f'/v2/users',
            'added': False,
            'user': None,
            'error': message
        })
        error_response.status_code = 400
        return error_response

    if user_data is None:
        return create_validation_error_response("The request body isn't populated.")

    user_to_add = User(user_data)

    if None in [user_to_add.username, user_to_add.first, user_to_add.last, user_to_add.password,
                user_to_add.activation_code, user_to_add.email]:
        return create_validation_error_response(
            "'username', 'first', 'last', 'email', 'password', and 'activation_code' are required fields"
        )

    if len(user_to_add.password) < 6:
        return create_validation_error_response("Password must contain at least 6 characters.")

    username_pattern = re.compile('^[a-zA-Z0-9]+$')

    if not username_pattern.match(user_to_add.username):
        return create_validation_error_response("Username can only contain Roman characters and numbers.")

    email_pattern = re.compile('^(([a-zA-Z0-9_.-])+@([a-zA-Z0-9_.-])+\\.([a-zA-Z])+([a-zA-Z])+)?$')

    if not email_pattern.match(user_to_add.email):
        return create_validation_error_response("The email address is invalid.")

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
        user_to_add.created_app = 'saints-xctf-api'
        user_to_add.created_user = None
        user_to_add.modified_date = None
        user_to_add.modified_app = None
        user_to_add.modified_user = None
        user_to_add.deleted_date = None
        user_to_add.deleted_app = None
        user_to_add.deleted_user = None
        user_to_add.deleted = False

        # First, add the user since its activation code is valid.
        UserDao.add_user(user_to_add)

        # Second, set the initial team and group for the user.
        code: Code = ActivationCodeDao.get_activation_code(user_to_add.activation_code)

        initial_group_id = int(code.group_id)
        initial_group: Group = GroupDao.get_group_by_id(initial_group_id)
        initial_team: Team = TeamDao.get_team_by_group_id(initial_group_id)

        TeamMemberDao.set_initial_membership(
            username=user_to_add.username,
            team_name=initial_team.name,
            group_id=initial_group_id,
            group_name=initial_group.group_name
        )

        # Third, remove the activation code so it cant be used again.
        CodeDao.remove_code(code)

        added_user = UserDao.get_user_by_username(user_to_add.username)

        if added_user is None:
            response = jsonify({
                'self': '/v2/users',
                'added': False,
                'user': None,
                'error': 'An unexpected error occurred creating the user.'
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
            'error': 'The activation code is invalid or expired.'
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

        if user_dict.get('profilepic') is not None:
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

    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get('sub')

    if username == jwt_username:
        current_app.logger.info(f'User {jwt_username} is updating their user details.')
    else:
        current_app.logger.info(f'User {jwt_username} is not authorized to update user {username}.')
        response = jsonify({
            'self': f'/v2/users/{username}',
            'updated': False,
            'user': None,
            'error': f'User {jwt_username} is not authorized to update user {username}.'
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

            if updated_user_dict.get('profilepic') is not None:
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
    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get('sub')

    if username == jwt_username:
        current_app.logger.info(f'User {jwt_username} is soft deleting their user.')
    else:
        current_app.logger.info(f'User {jwt_username} is not authorized to soft delete user {username}.')
        response = jsonify({
            'self': f'/v2/users/soft/{username}',
            'deleted': False,
            'error': f'User {jwt_username} is not authorized to soft delete user {username}.'
        })
        response.status_code = 400
        return response

    existing_user: User = UserDao.get_user_by_username(username=username)

    if existing_user is None:
        response = jsonify({
            'self': f'/v2/users/soft/{username}',
            'deleted': False,
            'error': 'there is no existing user with this username'
        })
        response.status_code = 400
        return response

    # Update the user model to reflect the soft delete
    existing_user.deleted = True
    existing_user.deleted_date = datetime.now()
    existing_user.deleted_app = 'saints-xctf-api'
    existing_user.modified_date = datetime.now()
    existing_user.modified_app = 'saints-xctf-api'

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

        if user_dict.get('profilepic') is not None:
            try:
                user_dict['profilepic'] = user_dict['profilepic'].decode('utf-8')
            except AttributeError:
                pass

        username = user_dict['username']
        groups: ResultProxy = GroupMemberDao.get_user_groups(username=username)
        group_list = []

        for group in groups:
            group_dict = {
                'id': group['id'],
                'group_name': group['group_name'],
                'group_title': group['group_title'],
                'status': group['status'],
                'user': group['user']
            }
            newest_log: Column = GroupDao.get_newest_log_date(group['group_name'])
            group_dict['newest_log'] = newest_log['newest']

            newest_message = GroupDao.get_newest_message_date(group['group_name'])
            group_dict['newest_message'] = newest_message['newest']

            group_list.append(group_dict)

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

        flairs: List[Flair] = FlairDao.get_flair_by_username(username=username)
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
                'description': notification['description']
            })

        user_dict['notifications'] = notification_dicts

        stats = compile_user_statistics(user, username)
        user_dict['statistics'] = stats

        response = jsonify({
            'self': f'/v2/users/snapshot/{username}',
            'user': user_dict
        })
        response.status_code = 200
        return response


def user_groups_by_username_get(username) -> Response:
    """
    Get the group memberships for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    groups: ResultProxy = GroupMemberDao.get_user_groups(username=username)
    group_list = []

    for group in groups:
        group_list.append({
            'id': group['id'],
            'group_name': group['group_name'],
            'group_title': group['group_title'],
            'status': group['status'],
            'user': group['user']
        })

    response = jsonify({
        'self': f'/v2/users/groups/{username}',
        'groups': group_list
    })
    response.status_code = 200
    return response


def user_teams_by_username_get(username) -> Response:
    """
    Get the team memberships for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    teams: ResultProxy = TeamMemberDao.get_user_teams(username=username)
    team_list = []

    for team in teams:
        team_list.append({
            'team_name': team['team_name'],
            'title': team['title'],
            'status': team['status'],
            'user': team['user']
        })

    response = jsonify({
        'self': f'/v2/users/teams/{username}',
        'teams': team_list
    })
    response.status_code = 200
    return response


def user_memberships_by_username_get(username) -> Response:
    """
    Get the team and group memberships for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    teams: ResultProxy = TeamMemberDao.get_user_teams(username=username)
    membership_list = []

    for team in teams:
        groups: ResultProxy = GroupMemberDao.get_user_groups_in_team(username=username, team_name=team['team_name'])
        membership_list.append({
            'team_name': team['team_name'],
            'title': team['title'],
            'status': team['status'],
            'user': team['user'],
            'groups': [
                {
                    'group_name': group['group_name'],
                    'group_title': group['group_title'],
                    'group_id': group['group_id'],
                    'status': group['status'],
                    'user': group['user']
                }
                for group in groups
            ]
        })

    response = jsonify({
        'self': f'/v2/users/memberships/{username}',
        'memberships': membership_list
    })
    response.status_code = 200
    return response


def user_memberships_by_username_put(username) -> Response:
    """
    Update the team and group memberships of a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the PUT API request.
    """
    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get('sub')

    if username == jwt_username:
        current_app.logger.info(f'User {jwt_username} is updating their memberships.')
    else:
        current_app.logger.info(f'User {jwt_username} is not authorized to update the memberships of user {username}.')
        response = jsonify({
            'self': f'/v2/users/memberships/{username}',
            'updated': False,
            'error': f'User {jwt_username} is not authorized to update the memberships of user {username}.'
        })
        response.status_code = 400
        return response

    membership_data: dict = request.get_json()
    teams_joined = membership_data.get('teams_joined')
    teams_left = membership_data.get('teams_left')
    groups_joined = membership_data.get('groups_joined')
    groups_left = membership_data.get('groups_left')

    committed: bool = False

    try:
        committed = TeamMemberDao.update_user_memberships(
            username, teams_joined, teams_left, groups_joined, groups_left
        )
    except SQLAlchemyError as e:
        current_app.logger.error(str(e))

    if committed:
        response = jsonify({
            'self': f'/v2/users/memberships/{username}',
            'updated': True,
        })
        response.status_code = 201
        return response
    else:
        response = jsonify({
            'self': f'/v2/users/memberships/{username}',
            'updated': False,
            'error': "failed to update the user's memberships"
        })
        response.status_code = 500
        return response


def user_notifications_by_username_get(username) -> Response:
    """
    Get the notifications for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    notifications: ResultProxy = NotificationDao.get_notification_by_username(username=username)

    notification_dicts = []
    for notification in notifications:
        notification_dicts.append({
            'notification_id': notification['notification_id'],
            'username': notification['username'],
            'time': notification['time'],
            'link': notification['link'],
            'viewed': notification['viewed'],
            'description': notification['description']
        })

    response = jsonify({
        'self': f'/v2/users/notifications/{username}',
        'notifications': notification_dicts
    })
    response.status_code = 200
    return response


def user_flair_by_username_get(username) -> Response:
    """
    Get the flair for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    flairs: List[Flair] = FlairDao.get_flair_by_username(username=username)

    flair_dicts = []

    for flair in flairs:
        flair_dicts.append(FlairData(flair).__dict__)

    response = jsonify({
        'self': f'/v2/users/flair/{username}',
        'flair': flair_dicts
    })
    response.status_code = 200
    return response


def user_statistics_by_username_get(username) -> Response:
    """
    Get exercise statistics for a user.
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
            'self': f'/v2/users/statistics/{username}',
            'stats': None,
            'error': 'there is no user with this username'
        })
        response.status_code = 400
        return response

    response = jsonify({
        'self': f'/v2/users/statistics/{username}',
        'stats': compile_user_statistics(user, username)
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
    forgot_password_code: str = request_dict.get('forgot_password_code')
    new_password: str = request_dict.get('new_password')

    if forgot_password_code is None or new_password is None:
        response = jsonify({
            'self': f'/v2/users/{username}/change_password',
            'password_updated': False,
            'forgot_password_code_deleted': False,
            'error': "'forgot_password_code' and 'new_password' are required fields."
        })
        response.status_code = 500
        return response

    forgot_password_code_info: ForgotPassword = ForgotPasswordDao.get_forgot_password_code(forgot_password_code)

    if not forgot_password_code_info:
        response = jsonify({
            'self': f'/v2/users/{username}/change_password',
            'password_updated': False,
            'forgot_password_code_deleted': False,
            'error': "This forgot password code is invalid."
        })
        response.status_code = 500
        return response

    if forgot_password_code_info.username != username:
        response = jsonify({
            'self': f'/v2/users/{username}/change_password',
            'password_updated': False,
            'forgot_password_code_deleted': False,
            'error': "This forgot password code does not belong to the specified user."
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
    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get('sub')

    if username == jwt_username:
        current_app.logger.info(f'User {jwt_username} logged in.')
    else:
        current_app.logger.info(
            f'User {jwt_username} is not authorized to update the last login date of user {username}.'
        )
        response = jsonify({
            'self': f'/v2/users/{username}/update_last_login',
            'last_login_updated': False,
            'error': f'User {jwt_username} is not authorized to update the last login date of user {username}.'
        })
        response.status_code = 400
        return response

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


def user_lookup_by_username_get(username: str) -> Response:
    """
    Check if a user exists based on its username or email.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    existing_user: User = UserDao.get_user_by_username(username=username)

    # If the user cant be found, try searching the email column in the database
    if existing_user is None:
        email = username
        existing_user: User = UserDao.get_user_by_email(email=email)

    # If the user still can't be found, return with an error code
    if existing_user is None:
        response = jsonify({
            'self': f'/v2/users/lookup/{username}',
            'exists': False,
            'error': 'There is no user with this username or email.'
        })
        response.status_code = 400
        return response
    else:
        response = jsonify({
            'self': f'/v2/users/lookup/{username}',
            'exists': True
        })
        response.status_code = 200
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
                'link': '/v2/users/groups/<username>',
                'verb': 'GET',
                'description': 'Get a list of groups that a user with a given username is a member of.'
            },
            {
                'link': '/v2/users/teams/<username>',
                'verb': 'GET',
                'description': 'Get a list of teams that a user with a given username is a member of.'
            },
            {
                'link': '/v2/users/memberships/<username>',
                'verb': 'GET',
                'description': 'Get a list of teams with nested lists of groups that a user is a member of.'
            },
            {
                'link': '/v2/users/memberships/<username>',
                'verb': 'PUT',
                'description': "Update a user's group and team memberships."
            },
            {
                'link': '/v2/users/notifications/<username>',
                'verb': 'GET',
                'description': 'Get a list of notifications for a user with a given username.'
            },
            {
                'link': '/v2/users/flair/<username>',
                'verb': 'GET',
                'description': 'Get a list of flair objects assigned to a user with a given username.'
            },
            {
                'link': '/v2/users/statistics/<username>',
                'verb': 'GET',
                'description': 'Get exercise statistics for a user with a given username.'
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
            },
            {
                'link': '/v2/users/lookup/<username>',
                'verb': 'GET',
                'description': 'Check if a user exists with a username or email.'
            }
        ],
    })
    response.status_code = 200
    return response


"""
Helper Methods
"""


def compile_user_statistics(user: UserData, username: str) -> dict:
    """
    Query user statistics and combine them into a single map.
    :param user: A user object containing information such as their preferred week start date.
    :param username: The username of the user to get statistics for.
    """
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

    return {
        'miles_all_time': float(miles['total']),
        'miles_past_year': float(0 if miles_past_year['total'] is None else miles_past_year['total']),
        'miles_past_month': float(0 if miles_past_month['total'] is None else miles_past_month['total']),
        'miles_past_week': float(0 if miles_past_week['total'] is None else miles_past_week['total']),
        'run_miles_all_time': float(0 if run_miles['total'] is None else run_miles['total']),
        'run_miles_past_year': float(0 if run_miles_past_year['total'] is None else run_miles_past_year['total']),
        'run_miles_past_month': float(0 if run_miles_past_month['total'] is None else run_miles_past_month['total']),
        'run_miles_past_week': float(0 if run_miles_past_week['total'] is None else run_miles_past_week['total']),
        'feel_all_time': float(0 if all_time_feel['average'] is None else all_time_feel['average']),
        'feel_past_year': float(0 if year_feel['average'] is None else year_feel['average']),
        'feel_past_month': float(0 if month_feel['average'] is None else month_feel['average']),
        'feel_past_week': float(0 if week_feel['average'] is None else week_feel['average'])
    }

