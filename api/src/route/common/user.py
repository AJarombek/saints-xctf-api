"""
Common code for the User routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

from typing import Dict, Any, Union, Type, List

from flask import Response, jsonify
from sqlalchemy.schema import Column
from sqlalchemy.engine.cursor import ResultProxy

from model.User import User
from model.UserData import UserData
from model.FlairData import FlairData
from model.Flair import Flair
from dao.flairDao import FlairDao
from dao.flairDemoDao import FlairDemoDao
from dao.forgotPasswordDao import ForgotPasswordDao
from dao.forgotPasswordDemoDao import ForgotPasswordDemoDao
from dao.groupDao import GroupDao
from dao.groupDemoDao import GroupDemoDao
from dao.groupMemberDao import GroupMemberDao
from dao.groupMemberDemoDao import GroupMemberDemoDao
from dao.logDao import LogDao
from dao.logDemoDao import LogDemoDao
from dao.notificationDao import NotificationDao
from dao.notificationDemoDao import NotificationDemoDao
from dao.teamMemberDao import TeamMemberDao
from dao.teamMemberDemoDao import TeamMemberDemoDao
from dao.userDao import UserDao
from dao.userDemoDao import UserDemoDao
from route.common.versions import APIVersion


def user_links(version: str) -> Dict[str, Any]:
    """
    Get all the user API endpoints.
    :return: A dictionary describing all user API endpoints.
    """
    return {
        "self": f"/{version}/users/links",
        "endpoints": [
            {
                "link": f"/{version}/users",
                "verb": "GET",
                "description": "Get all the users in the database.",
            },
            {
                "link": f"/{version}/users",
                "verb": "POST",
                "description": "Create a new user.",
            },
            {
                "link": f"/{version}/users/<username>",
                "verb": "GET",
                "description": "Retrieve a single user with a given username.",
            },
            {
                "link": f"/{version}/users/<username>",
                "verb": "PUT",
                "description": "Update a user with a given username.",
            },
            {
                "link": f"/{version}/users/<username>",
                "verb": "DELETE",
                "description": "Delete a user with a given username.",
            },
            {
                "link": f"/{version}/users/soft/<username>",
                "verb": "DELETE",
                "description": "Soft delete a user with a given username.",
            },
            {
                "link": f"/{version}/users/snapshot/<username>",
                "verb": "GET",
                "description": "Get a snapshot about a user and their exercise statistics with a given username.",
            },
            {
                "link": f"/{version}/users/groups/<username>",
                "verb": "GET",
                "description": "Get a list of groups that a user with a given username is a member of.",
            },
            {
                "link": f"/{version}/users/teams/<username>",
                "verb": "GET",
                "description": "Get a list of teams that a user with a given username is a member of.",
            },
            {
                "link": f"/{version}/users/memberships/<username>",
                "verb": "GET",
                "description": "Get a list of teams with nested lists of groups that a user is a member of.",
            },
            {
                "link": f"/{version}/users/memberships/<username>",
                "verb": "PUT",
                "description": "Update a user's group and team memberships.",
            },
            {
                "link": f"/{version}/users/notifications/<username>",
                "verb": "GET",
                "description": "Get a list of notifications for a user with a given username.",
            },
            {
                "link": f"/{version}/users/flair/<username>",
                "verb": "GET",
                "description": "Get a list of flair objects assigned to a user with a given username.",
            },
            {
                "link": f"/{version}/users/statistics/<username>",
                "verb": "GET",
                "description": "Get exercise statistics for a user with a given username.",
            },
            {
                "link": f"/{version}/users/<username>/change_password",
                "verb": "PUT",
                "description": "Update a user with a given username.  Specifically, alter the users password.",
            },
            {
                "link": f"/{version}/users/<username>/update_last_login",
                "verb": "PUT",
                "description": "Update a user with a given username.  Specifically, change the users last login date.",
            },
            {
                "link": f"/{version}/users/lookup/<username>",
                "verb": "GET",
                "description": "Check if a user exists with a username or email.",
            },
        ],
    }


def users_get(
    version: Union[APIVersion.v2, APIVersion.demo],
    dao: Union[Type[UserDao], Type[UserDemoDao]],
) -> Response:
    """
    Retrieve all the users in the database.
    :param version: Version of the API to use for the request.
    :param dao: Data access object to use for database access.
    :return: A response object for the GET API request.
    """
    all_users: list = dao.get_users()

    if all_users is None:
        response = jsonify(
            {
                "self": f"/{version}/users",
                "users": None,
                "error": "an unexpected error occurred retrieving users",
            }
        )
        response.status_code = 500
        return response
    else:
        user_dicts = []

        for user in all_users:
            user_dict = UserData(user).__dict__
            user_dict["this_user"] = f'/{version}/users/{user_dict["username"]}'

            if user_dict.get("member_since") is not None:
                user_dict["member_since"] = str(user_dict["member_since"])
            if user_dict.get("last_signin") is not None:
                user_dict["last_signin"] = str(user_dict["last_signin"])

            user_dicts.append(user_dict)

        response = jsonify({"self": f"/{version}/users", "users": user_dicts})
        response.status_code = 200
        return response


def user_by_username_get(
    username: str,
    version: Union[APIVersion.v2, APIVersion.demo],
    dao: Union[Type[UserDao], Type[UserDemoDao]],
) -> Response:
    """
    Retrieve a user based on its username.
    :param username: Username that uniquely identifies a user.
    :param version: Version of the API to use for the request.
    :param dao: Data access object to use for database access.
    :return: A response object for the GET API request.
    """
    user: User = dao.get_user_by_username(username=username)

    # If the user cant be found, try searching the email column in the database
    if user is None:
        email = username
        user: User = dao.get_user_by_email(email=email)

    # If the user still can't be found, return with an error code
    if user is None:
        response = jsonify(
            {
                "self": f"/{version}/users/{username}",
                "user": None,
                "error": "there is no user with this username",
            }
        )
        response.status_code = 400
        return response
    else:
        user_dict: dict = UserData(user).__dict__

        if user_dict.get("member_since") is not None:
            user_dict["member_since"] = str(user_dict["member_since"])
        if user_dict.get("last_signin") is not None:
            user_dict["last_signin"] = str(user_dict["last_signin"])

        response = jsonify({"self": f"/{version}/users/{username}", "user": user_dict})
        response.status_code = 200
        return response


def user_groups_by_username_get(
    username,
    version: Union[APIVersion.v2, APIVersion.demo],
    dao: Union[Type[GroupMemberDao], Type[GroupMemberDemoDao]],
) -> Response:
    """
    Get the group memberships for a user.
    :param username: Username that uniquely identifies a user.
    :param version: Version of the API to use for the request.
    :param dao: Data access object to use for database access.
    :return: A response object for the GET API request.
    """
    groups: ResultProxy = dao.get_user_groups(username=username)
    group_list = []

    for group in groups:
        group_list.append(
            {
                "id": group["id"],
                "group_name": group["group_name"],
                "group_title": group["group_title"],
                "status": group["status"],
                "user": group["user"],
            }
        )

    response = jsonify(
        {"self": f"/{version}/users/groups/{username}", "groups": group_list}
    )
    response.status_code = 200
    return response


def user_teams_by_username_get(
    username,
    version: Union[APIVersion.v2, APIVersion.demo],
    dao: Union[Type[TeamMemberDao], Type[TeamMemberDemoDao]],
) -> Response:
    """
    Get the team memberships for a user.
    :param username: Username that uniquely identifies a user.
    :param version: Version of the API to use for the request.
    :param dao: Data access object to use for database access.
    :return: A response object for the GET API request.
    """
    teams: ResultProxy = dao.get_user_teams(username=username)
    team_list = []

    for team in teams:
        team_list.append(
            {
                "team_name": team["team_name"],
                "title": team["title"],
                "status": team["status"],
                "user": team["user"],
            }
        )

    response = jsonify(
        {"self": f"/{version}/users/teams/{username}", "teams": team_list}
    )
    response.status_code = 200
    return response


def user_memberships_by_username_get(
    username,
    version: Union[APIVersion.v2, APIVersion.demo],
    team_member_dao: Union[Type[TeamMemberDao], Type[TeamMemberDemoDao]],
    group_member_dao: Union[Type[GroupMemberDao], Type[GroupMemberDemoDao]],
) -> Response:
    """
    Get the team and group memberships for a user.
    :param username: Username that uniquely identifies a user.
    :param version: Version of the API to use for the request.
    :param team_member_dao: Data access object to use for database access for team members.
    :param group_member_dao: Data access object to use for database access for group members.
    :return: A response object for the GET API request.
    """
    teams: ResultProxy = team_member_dao.get_user_teams(username=username)
    membership_list = []

    for team in teams:
        groups: ResultProxy = group_member_dao.get_user_groups_in_team(
            username=username, team_name=team["team_name"]
        )
        membership_list.append(
            {
                "team_name": team["team_name"],
                "title": team["title"],
                "status": team["status"],
                "user": team["user"],
                "groups": [
                    {
                        "group_name": group["group_name"],
                        "group_title": group["group_title"],
                        "group_id": group["group_id"],
                        "status": group["status"],
                        "user": group["user"],
                    }
                    for group in groups
                ],
            }
        )

    response = jsonify(
        {
            "self": f"/{version}/users/memberships/{username}",
            "memberships": membership_list,
        }
    )
    response.status_code = 200
    return response


def user_snapshot_by_username_get(
    username: str,
    version: Union[APIVersion.v2, APIVersion.demo],
    user_dao: Union[Type[UserDao], Type[UserDemoDao]],
    group_member_dao: Union[Type[GroupMemberDao], Type[GroupMemberDemoDao]],
    group_dao: Union[Type[GroupDao], Type[GroupDemoDao]],
    forgot_password_dao: Union[Type[ForgotPasswordDao], Type[ForgotPasswordDemoDao]],
    flair_dao: Union[Type[FlairDao], Type[FlairDemoDao]],
    notification_dao: Union[Type[NotificationDao], Type[NotificationDemoDao]],
    log_dao: Union[Type[LogDao], Type[LogDemoDao]],
) -> Response:
    """
    Get a snapshot with information about a user with a given username.
    :param username: Username that uniquely identifies a user.
    :param version: Version of the API to use for the request.
    :param user_dao: Data access object to use for user related database access.
    :param group_member_dao: Data access object to use for group member related database access.
    :param group_dao: Data access object to use for group related database access.
    :param forgot_password_dao: Data access object to use for forgot password related database access.
    :param flair_dao: Data access object to use for flair related database access.
    :param notification_dao: Data access object to use for notification related database access.
    :param log_dao: Data access object to use for exercise log related database access.
    :return: A response object for the GET API request.
    """
    user: User = user_dao.get_user_by_username(username=username)

    # If the user cant be found, try searching the email column in the database
    if user is None:
        email = username
        user: User = user_dao.get_user_by_email(email=email)

    # If the user still can't be found, return with an error code
    if user is None:
        response = jsonify(
            {
                "self": f"/{version}/users/snapshot/{username}",
                "user": None,
                "error": "there is no user with this username",
            }
        )
        response.status_code = 400
        return response
    else:
        user_dict: dict = UserData(user).__dict__

        if user_dict.get("member_since") is not None:
            user_dict["member_since"] = str(user_dict["member_since"])
        if user_dict.get("last_signin") is not None:
            user_dict["last_signin"] = str(user_dict["last_signin"])

        username = user_dict["username"]
        groups: ResultProxy = group_member_dao.get_user_groups(username=username)
        group_list = []

        for group in groups:
            group_dict = {
                "id": group["id"],
                "group_name": group["group_name"],
                "group_title": group["group_title"],
                "status": group["status"],
                "user": group["user"],
            }
            newest_log: Column = group_dao.get_newest_log_date(group["group_name"])
            group_dict["newest_log"] = newest_log["newest"]

            group_list.append(group_dict)

        user_dict["groups"] = group_list

        forgot_password_codes: ResultProxy = (
            forgot_password_dao.get_forgot_password_codes(username=username)
        )

        forgot_password_list = []
        for forgot_password_code in forgot_password_codes:
            forgot_password_list.append(
                {
                    "forgot_code": forgot_password_code["forgot_code"],
                    "username": forgot_password_code["username"],
                    "expires": forgot_password_code["expires"],
                    "deleted": forgot_password_code["deleted"],
                }
            )

        user_dict["forgotpassword"] = forgot_password_list

        flairs: List[Flair] = flair_dao.get_flair_by_username(username=username)
        flair_dicts = []

        for flair in flairs:
            flair_dicts.append(FlairData(flair).__dict__)

        user_dict["flair"] = flair_dicts

        notifications: ResultProxy = notification_dao.get_notification_by_username(
            username=username
        )

        notification_dicts = []
        for notification in notifications:
            notification_dicts.append(
                {
                    "notification_id": notification["notification_id"],
                    "username": notification["username"],
                    "time": notification["time"],
                    "link": notification["link"],
                    "viewed": notification["viewed"],
                    "description": notification["description"],
                }
            )

        user_dict["notifications"] = notification_dicts

        stats = compile_user_statistics(user, username, log_dao)
        user_dict["statistics"] = stats

        response = jsonify(
            {"self": f"/{version}/users/snapshot/{username}", "user": user_dict}
        )
        response.status_code = 200
        return response


def user_statistics_by_username_get(
    username: str,
    version: Union[APIVersion.v2, APIVersion.demo],
    user_dao: Union[Type[UserDao], Type[UserDemoDao]],
    log_dao: Union[Type[LogDao], Type[LogDemoDao]],
) -> Response:
    """
    Get exercise statistics for a user.
    :param username: Username that uniquely identifies a user.
    :param version: Version of the API to use for the request.
    :param user_dao: Data access object to use for database access related to users.
    :param log_dao: Data access object to use for database access related to logs.
    :return: A response object for the GET API request.
    """
    user: User = user_dao.get_user_by_username(username=username)

    # If the user cant be found, try searching the email column in the database
    if user is None:
        email = username
        user: User = user_dao.get_user_by_email(email=email)

    # If the user still can't be found, return with an error code
    if user is None:
        response = jsonify(
            {
                "self": f"/{version}/users/statistics/{username}",
                "stats": None,
                "error": "there is no user with this username",
            }
        )
        response.status_code = 400
        return response

    response = jsonify(
        {
            "self": f"/{version}/users/statistics/{username}",
            "stats": compile_user_statistics(user, username, log_dao),
        }
    )
    response.status_code = 200
    return response


"""
Helper Methods
"""


def compile_user_statistics(
    user: UserData, username: str, dao: Union[Type[LogDao], Type[LogDemoDao]]
) -> dict:
    """
    Query user statistics and combine them into a single map.
    :param user: A user object containing information such as their preferred week start date.
    :param username: The username of the user to get statistics for.
    :param dao: Data access object to use for database access.
    """
    miles: Column = dao.get_user_miles(username)
    miles_past_year: Column = dao.get_user_miles_interval(username, "year")
    miles_past_month: Column = dao.get_user_miles_interval(username, "month")
    miles_past_week: Column = dao.get_user_miles_interval(
        username, "week", week_start=user.week_start
    )
    run_miles: Column = dao.get_user_miles_interval_by_type(username, "run")
    run_miles_past_year: Column = dao.get_user_miles_interval_by_type(
        username, "run", "year"
    )
    run_miles_past_month: Column = dao.get_user_miles_interval_by_type(
        username, "run", "month"
    )
    run_miles_past_week: Column = dao.get_user_miles_interval_by_type(
        username, "run", "week"
    )
    all_time_feel: Column = dao.get_user_avg_feel(username)
    year_feel: Column = dao.get_user_avg_feel_interval(username, "year")
    month_feel: Column = dao.get_user_avg_feel_interval(username, "month")
    week_feel: Column = dao.get_user_avg_feel_interval(
        username, "week", week_start=user.week_start
    )

    return {
        "miles_all_time": float(miles["total"]),
        "miles_past_year": float(
            0 if miles_past_year["total"] is None else miles_past_year["total"]
        ),
        "miles_past_month": float(
            0 if miles_past_month["total"] is None else miles_past_month["total"]
        ),
        "miles_past_week": float(
            0 if miles_past_week["total"] is None else miles_past_week["total"]
        ),
        "run_miles_all_time": float(
            0 if run_miles["total"] is None else run_miles["total"]
        ),
        "run_miles_past_year": float(
            0 if run_miles_past_year["total"] is None else run_miles_past_year["total"]
        ),
        "run_miles_past_month": float(
            0
            if run_miles_past_month["total"] is None
            else run_miles_past_month["total"]
        ),
        "run_miles_past_week": float(
            0 if run_miles_past_week["total"] is None else run_miles_past_week["total"]
        ),
        "feel_all_time": float(
            0 if all_time_feel["average"] is None else all_time_feel["average"]
        ),
        "feel_past_year": float(
            0 if year_feel["average"] is None else year_feel["average"]
        ),
        "feel_past_month": float(
            0 if month_feel["average"] is None else month_feel["average"]
        ),
        "feel_past_week": float(
            0 if week_feel["average"] is None else week_feel["average"]
        ),
    }
