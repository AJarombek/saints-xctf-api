"""
User routes in the demo version of the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/7/2022
"""

from flask import Blueprint, request, jsonify, Response, redirect, url_for
from flasgger import swag_from

from decorators import auth_required, disabled, DELETE, GET
from route.common.versions import APIVersion
from dao.userDemoDao import UserDemoDao
from dao.groupMemberDemoDao import GroupMemberDemoDao
from dao.groupDemoDao import GroupDemoDao
from dao.forgotPasswordDemoDao import ForgotPasswordDemoDao
from dao.flairDemoDao import FlairDemoDao
from dao.notificationDemoDao import NotificationDemoDao
from dao.logDemoDao import LogDemoDao
from dao.teamMemberDemoDao import TeamMemberDemoDao
import route.common.user as R

user_demo_route = Blueprint("user_demo_route", __name__, url_prefix="/demo/users")


@user_demo_route.route("", methods=["GET", "POST"])
@auth_required(enabled_methods=[GET])
def users_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'users' to the user routes.
    :return: Response object letting the caller know where to redirect the request to.
    """
    if request.method == "GET":
        """[GET] /demo/users"""
        return redirect(url_for("user_demo_route.users"), code=302)

    elif request.method == "POST":
        """[POST] /demo/users"""
        return redirect(url_for("user_demo_route.users"), code=307)


@user_demo_route.route("/", methods=["GET", "POST"])
@auth_required(enabled_methods=[GET])
@swag_from("swagger/userRoute/usersGet.yml", methods=["GET"])
@swag_from("swagger/userRoute/usersPost.yml", methods=["POST"])
def users() -> Response:
    """
    Endpoints for searching all the users or creating a user
    :return: JSON representation of a list of users and relevant metadata
    """
    if request.method == "GET":
        """[GET] /demo/users/"""
        return users_get()

    elif request.method == "POST":
        """[POST] /demo/users/"""
        return user_post()


@user_demo_route.route("/<username>", methods=["GET", "PUT", "DELETE"])
@auth_required()
@disabled(disabled_methods=[DELETE])
@swag_from("swagger/userRoute/userGet.yml", methods=["GET"])
@swag_from("swagger/userRoute/userPut.yml", methods=["PUT"])
def user(username) -> Response:
    """
    Endpoints for specific users (searching, updating, or deleting)
    :param username: Username (or email) of a User
    :return: JSON representation of a user and relevant metadata
    """
    if request.method == "GET":
        """[GET] /demo/users/<username>"""
        return user_by_username_get(username)

    elif request.method == "PUT":
        """[PUT] /demo/users/<username>"""
        return user_by_username_put(username)

    elif request.method == "DELETE":
        """[DELETE] /demo/users/<username>"""
        return user_by_username_delete(username)


@user_demo_route.route("/soft/<username>", methods=["DELETE"])
@auth_required()
@swag_from("swagger/userRoute/userSoftDelete.yml", methods=["DELETE"])
def user_soft_by_username(username) -> Response:
    """
    Endpoints for soft deleting a user.
    :param username: Username of a User.
    :return: JSON representation of users and relevant metadata.
    """
    if request.method == "DELETE":
        """[DELETE] /demo/users/soft/<username>"""
        return user_by_username_soft_delete(username)


@user_demo_route.route("/snapshot/<username>", methods=["GET"])
@auth_required()
@swag_from("swagger/userRoute/userSnapshotGet.yml", methods=["GET"])
def user_snapshot(username) -> Response:
    """
    Endpoint for a website snapshot for a specific user.  Provides more details than the base user route,
    such as group memberships and statistics.
    :param username: Username (or email) of a User
    :return: JSON representation of a user and relevant metadata
    """
    if request.method == "GET":
        """[GET] /demo/users/snapshot/<username>"""
        return user_snapshot_by_username_get(username)


@user_demo_route.route("/groups/<username>", methods=["GET"])
@auth_required()
@swag_from("swagger/userRoute/userGroupsGet.yml", methods=["GET"])
def user_groups(username) -> Response:
    """
    Endpoint for retrieving a user's group memberships.
    :param username: Username (or email) of a User
    :return: JSON representation of a list of group memberships
    """
    if request.method == "GET":
        """[GET] /demo/users/groups/<username>"""
        return user_groups_by_username_get(username)


@user_demo_route.route("/teams/<username>", methods=["GET"])
@auth_required()
@swag_from("swagger/userRoute/userTeamsGet.yml", methods=["GET"])
def user_teams(username) -> Response:
    """
    Endpoint for retrieving a user's team memberships.
    :param username: Username (or email) of a User
    :return: JSON representation of a list of team memberships
    """
    if request.method == "GET":
        """[GET] /demo/users/teams/<username>"""
        return user_teams_by_username_get(username)


@user_demo_route.route("/memberships/<username>", methods=["GET", "PUT"])
@auth_required()
@swag_from("swagger/userRoute/userMembershipsGet.yml", methods=["GET"])
@swag_from("swagger/userRoute/userMembershipsPut.yml", methods=["PUT"])
def user_memberships(username) -> Response:
    """
    Endpoint for retrieving a user's team and group memberships.
    :param username: Username (or email) of a User
    :return: JSON representation of a list of team memberships with nested group memberships
    """
    if request.method == "GET":
        """[GET] /demo/users/memberships/<username>"""
        return user_memberships_by_username_get(username)
    elif request.method == "PUT":
        """[PUT] /demo/users/memberships/<username>"""
        return user_memberships_by_username_put(username)


@user_demo_route.route("/notifications/<username>", methods=["GET"])
@auth_required()
@swag_from("swagger/userRoute/userNotificationsGet.yml", methods=["GET"])
def user_notifications(username) -> Response:
    """
    Endpoint for retrieving a user's notifications.
    :param username: Username (or email) of a User
    :return: JSON representation of a list of notifications
    """
    if request.method == "GET":
        """[GET] /demo/users/notifications/<username>"""
        return user_notifications_by_username_get(username)


@user_demo_route.route("/flair/<username>", methods=["GET"])
@auth_required()
@swag_from("swagger/userRoute/userFlairGet.yml", methods=["GET"])
def user_flair(username) -> Response:
    """
    Endpoint for retrieving a user's flair.
    :param username: Username (or email) of a User
    :return: JSON representation of a list of flair objects
    """
    if request.method == "GET":
        """[GET] /demo/users/flair/<username>"""
        return user_flair_by_username_get(username)


@user_demo_route.route("/statistics/<username>", methods=["GET"])
@auth_required()
@swag_from("swagger/userRoute/userStatisticsGet.yml", methods=["GET"])
def user_statistics(username) -> Response:
    """
    Endpoint for retrieving a user's statistics.
    :param username: Username (or email) of a User
    :return: JSON representation of a users exercise statistics.
    """
    if request.method == "GET":
        """[GET] /demo/users/statistics/<username>"""
        return user_statistics_by_username_get(username)


@user_demo_route.route("/<username>/change_password", methods=["PUT"])
@swag_from("swagger/userRoute/userChangePasswordPut.yml", methods=["PUT"])
def user_change_password(username) -> Response:
    """
    Endpoint for changing a users password.
    :param username: Username which uniquely identifies a user.
    :return: JSON with the result of the password change.
    """
    if request.method == "PUT":
        """[GET] /demo/users/<username>/change_password"""
        return user_change_password_by_username_put(username)


@user_demo_route.route("/<username>/update_last_login", methods=["PUT"])
@auth_required()
@swag_from("swagger/userRoute/userUpdateLastLoginPut.yml", methods=["PUT"])
def user_update_last_login(username) -> Response:
    """
    Update the date of a users previous sign in.
    :param username: Username which uniquely identifies a user.
    :return: JSON with the result of the last login update
    """
    if request.method == "PUT":
        """[PUT] /demo/users/<username>/update_last_login"""
        return user_update_last_login_by_username_put(username)


@user_demo_route.route("/lookup/<username>", methods=["GET"])
@swag_from("swagger/userRoute/userLookupGet.yml", methods=["GET"])
def user_lookup(username) -> Response:
    """
    Endpoint for looking up a username/email to see if its currently in use.  This endpoint is used while a user is
    registering, before they have access to view other user's details.
    :param username: Username (or email) of a User.
    :return: JSON representation of the result of a user lookup.
    """
    if request.method == "GET":
        """[GET] /demo/users/lookup/<username>"""
        return user_lookup_by_username_get(username)


@user_demo_route.route("/links", methods=["GET"])
@swag_from("swagger/userRoute/userLinks.yml", methods=["GET"])
def user_links() -> Response:
    """
    Endpoint for information about the user API endpoints.
    :return: Metadata about the user API.
    """
    if request.method == "GET":
        """[GET] /demo/users/links"""
        return user_links_get()


def users_get() -> Response:
    """
    Retrieve all the users in the database.
    :return: A response object for the GET API request.
    """
    return R.users_get(APIVersion.demo.value, UserDemoDao)


def user_post() -> Response:
    """
    Create a new user.
    :return: A response object for the POST API request.
    """
    response = jsonify(
        {
            "self": "/demo/users",
            "added": True,
            "user": {},
            "new_user": f'/demo/users/{request.get_json().get("username")}',
        }
    )
    response.status_code = 201
    return response


def user_by_username_get(username) -> Response:
    """
    Retrieve a user based on its username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    return R.user_by_username_get(username, APIVersion.demo.value, UserDemoDao)


def user_by_username_put(username) -> Response:
    """
    Update an existing user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the PUT API request.
    """
    response = jsonify({"self": f"/demo/users/{username}", "updated": True, "user": {}})
    response.status_code = 200
    return response


def user_by_username_delete(username) -> Response:
    """
    Hard delete an existing user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the DELETE API request.
    """
    response = jsonify(
        {
            "self": f"/demo/users/{username}",
            "deleted": True,
        }
    )
    response.status_code = 204
    return response


def user_by_username_soft_delete(username) -> Response:
    """
    Soft delete an existing user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the DELETE API request.
    """
    response = jsonify(
        {
            "self": f"/demo/users/soft/{username}",
            "deleted": True,
        }
    )
    response.status_code = 204
    return response


def user_snapshot_by_username_get(username) -> Response:
    """
    Get a snapshot with information about a user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    return R.user_snapshot_by_username_get(
        username=username,
        version=APIVersion.demo.value,
        user_dao=UserDemoDao,
        group_member_dao=GroupMemberDemoDao,
        group_dao=GroupDemoDao,
        forgot_password_dao=ForgotPasswordDemoDao,
        flair_dao=FlairDemoDao,
        notification_dao=NotificationDemoDao,
        log_dao=LogDemoDao,
    )


def user_groups_by_username_get(username) -> Response:
    """
    Get the group memberships for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    return R.user_groups_by_username_get(
        username, APIVersion.demo.value, GroupMemberDemoDao
    )


def user_teams_by_username_get(username) -> Response:
    """
    Get the team memberships for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    return R.user_teams_by_username_get(
        username, APIVersion.demo.value, TeamMemberDemoDao
    )


def user_memberships_by_username_get(username) -> Response:
    """
    Get the team and group memberships for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    return R.user_memberships_by_username_get(
        username, APIVersion.demo.value, TeamMemberDemoDao, GroupMemberDemoDao
    )


def user_memberships_by_username_put(username) -> Response:
    """
    Update the team and group memberships of a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the PUT API request.
    """
    response = jsonify(
        {
            "self": f"/demo/users/memberships/{username}",
            "updated": True,
        }
    )
    response.status_code = 201
    return response


def user_notifications_by_username_get(username) -> Response:
    """
    Get the notifications for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    return R.user_notifications_by_username_get(
        username, APIVersion.demo.value, NotificationDemoDao
    )


def user_flair_by_username_get(username) -> Response:
    """
    Get the flair for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    return R.user_flair_by_username_get(username, APIVersion.demo.value, FlairDemoDao)


def user_statistics_by_username_get(username) -> Response:
    """
    Get exercise statistics for a user.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    return R.user_statistics_by_username_get(
        username, APIVersion.demo.value, UserDemoDao, LogDemoDao
    )


def user_change_password_by_username_put(username) -> Response:
    """
    Change the password of a user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    response = jsonify(
        {
            "self": f"/demo/users/{username}/change_password",
            "password_updated": True,
            "forgot_password_code_deleted": {},
        }
    )
    response.status_code = 200
    return response


def user_update_last_login_by_username_put(username) -> Response:
    """
    Change the last login date of a user with a given username.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the PUT API request.
    """
    response = jsonify(
        {
            "self": f"/demo/users/{username}/update_last_login",
            "last_login_updated": True,
        }
    )
    response.status_code = 200
    return response


def user_lookup_by_username_get(username: str) -> Response:
    """
    Check if a user exists based on its username or email.
    :param username: Username that uniquely identifies a user.
    :return: A response object for the GET API request.
    """
    response = jsonify({"self": f"/demo/users/lookup/{username}", "exists": True})
    response.status_code = 200
    return response


def user_links_get() -> Response:
    """
    Get all the other user API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify(user_links(APIVersion.demo.value))
    response.status_code = 200
    return response
