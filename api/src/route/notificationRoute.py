"""
Notification routes in the SaintsXCTF API.  Used for retrieving, creating, updating and deleting notifications for
comments on logs, references, and group member requests.
Author: Andrew Jarombek
Date: 8/6/2019
"""

from datetime import datetime

from flask import (
    Blueprint,
    abort,
    request,
    jsonify,
    Response,
    redirect,
    url_for,
    current_app,
)
from flasgger import swag_from

from decorators import auth_required
from utils.jwt import get_claims
from model.Notification import Notification
from model.NotificationData import NotificationData
from dao.notificationDao import NotificationDao

notification_route = Blueprint(
    "notification_route", __name__, url_prefix="/v2/notifications"
)


@notification_route.route("", methods=["GET", "POST"])
@auth_required()
def notifications_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'notifications' to the notification routes.
    :return: Response object letting the caller know where to redirect the request to.
    """
    if request.method == "GET":
        """[GET] /v2/notifications"""
        return redirect(url_for("notification_route.notifications"), code=302)

    if request.method == "POST":
        """[POST] /v2/notifications"""
        return redirect(url_for("notification_route.notifications"), code=307)

    return abort(404)


@notification_route.route("/", methods=["GET", "POST"])
@auth_required()
@swag_from("swagger/notificationRoute/notificationsGet.yml", methods=["GET"])
@swag_from("swagger/notificationRoute/notificationPost.yml", methods=["POST"])
def notifications() -> Response:
    """
    Endpoints for retrieving all the notifications and creating new notifications.
    :return: JSON representation of notifications and relevant metadata.
    """
    if request.method == "GET":
        """[GET] /v2/notifications/"""
        return notifications_get()

    if request.method == "POST":
        """[POST] /v2/notifications/"""
        return notification_post()

    return abort(404)


@notification_route.route("/<notification_id>", methods=["GET", "PUT", "DELETE"])
@auth_required()
@swag_from("swagger/notificationRoute/notificationGet.yml", methods=["GET"])
@swag_from("swagger/notificationRoute/notificationPut.yml", methods=["PUT"])
@swag_from("swagger/notificationRoute/notificationDelete.yml", methods=["DELETE"])
def notification_by_id(notification_id) -> Response:
    """
    Endpoints for retrieving a single notification, updating existing notifications, and deleting notifications.
    :param notification_id: Unique identifier for a notification.
    :return: JSON representation of notifications and relevant metadata.
    """
    if request.method == "GET":
        """[GET] /v2/notifications/<notification_id>"""
        return notification_by_id_get(notification_id)

    if request.method == "PUT":
        """[PUT] /v2/notifications/<notification_id>"""
        return notification_by_id_put(notification_id)

    if request.method == "DELETE":
        """[DELETE] /v2/notifications/<notification_id>"""
        return notification_by_id_delete(notification_id)

    return abort(404)


@notification_route.route("/soft/<notification_id>", methods=["DELETE"])
@auth_required()
@swag_from("swagger/notificationRoute/notificationSoftDelete.yml", methods=["DELETE"])
def notification_soft_by_id(notification_id) -> Response:
    """
    Endpoints for soft deleting user notifications.
    :param notification_id: Unique identifier for a notification.
    :return: JSON representation of notifications and relevant metadata.
    """
    if request.method == "DELETE":
        """[DELETE] /v2/notifications/soft/<code>"""
        return notification_by_id_soft_delete(notification_id)

    return abort(404)


@notification_route.route("/links", methods=["GET"])
@swag_from("swagger/notificationRoute/notificationLinks.yml", methods=["GET"])
def notification_links() -> Response:
    """
    Endpoint for information about the notification API endpoints.
    :return: Metadata about the notification API.
    """
    if request.method == "GET":
        """[GET] /v2/notifications/links"""
        return notification_links_get()

    return abort(404)


def notifications_get() -> Response:
    """
    Retrieve all the notifications in the database.
    :return: A response object for the GET API request.
    """
    notifications_data = NotificationDao.get_notifications()

    if notifications_data is None:
        response = jsonify(
            {
                "self": "/v2/notifications",
                "notifications": None,
                "error": "an unexpected error occurred retrieving notifications",
            }
        )
        response.status_code = 500
        return response

    notification_dicts = []
    for notification in notifications_data:
        notification_dict = NotificationData(notification).__dict__
        notification_dict["time"] = str(notification_dict["time"])
        notification_dicts.append(notification_dict)

    response = jsonify(
        {"self": "/v2/notifications", "notifications": notification_dicts}
    )
    response.status_code = 200
    return response


def notification_post() -> Response:
    """
    Create a new notification for a user.
    :return: A response object for the POST API request.
    """
    notification_data: dict = request.get_json(silent=True)

    if notification_data is None:
        response = jsonify(
            {
                "self": "/v2/notifications",
                "added": False,
                "notification": None,
                "error": "the request body isn't populated",
            }
        )
        response.status_code = 400
        return response

    notification_to_add = Notification(notification_data)

    if None in [notification_to_add.username, notification_to_add.description]:
        response = jsonify(
            {
                "self": "/v2/notifications",
                "added": False,
                "notification": None,
                "error": "'username' and 'description' are required fields",
            }
        )
        response.status_code = 400
        return response

    notification_to_add.time = datetime.now()
    notification_to_add.viewed = "N"

    notification_to_add.created_date = datetime.now()
    notification_to_add.created_app = "saints-xctf-api"
    notification_to_add.created_user = None
    notification_to_add.modified_date = None
    notification_to_add.modified_app = None
    notification_to_add.modified_user = None
    notification_to_add.deleted_date = None
    notification_to_add.deleted_app = None
    notification_to_add.deleted_user = None
    notification_to_add.deleted = False

    notification_added_successfully = NotificationDao.add_notification(
        new_notification=notification_to_add
    )

    if notification_added_successfully:
        notification_added = NotificationDao.get_notification_by_id(
            notification_to_add.notification_id
        )
        notification_dict = NotificationData(notification_added).__dict__
        notification_dict["time"] = str(notification_dict["time"])

        response = jsonify(
            {
                "self": "/v2/notifications",
                "added": True,
                "notification": notification_dict,
            }
        )
        response.status_code = 200
        return response

    response = jsonify(
        {
            "self": "/v2/notifications",
            "added": False,
            "notification": None,
            "error": "failed to create a new notification",
        }
    )
    response.status_code = 500
    return response


def notification_by_id_get(notification_id) -> Response:
    """
    Retrieve a notification based on its identifier.
    :param notification_id: Unique identifier for a user's notification.
    :return: A response object for the GET API request.
    """
    notification = NotificationDao.get_notification_by_id(
        notification_id=notification_id
    )

    if notification is None:
        response = jsonify(
            {
                "self": f"/v2/notifications/{notification_id}",
                "notification": None,
                "error": "there is no notification with this identifier",
            }
        )
        response.status_code = 400
        return response

    notification_dict = NotificationData(notification).__dict__
    notification_dict["time"] = str(notification_dict["time"])

    response = jsonify(
        {
            "self": f"/v2/notifications/{notification_id}",
            "notification": notification_dict,
        }
    )
    response.status_code = 200
    return response


def notification_by_id_put(notification_id) -> Response:
    """
    Update an existing notification based on its identifier.
    :param notification_id: Unique identifier for a user's notification.
    :return: A response object for the PUT API request.
    """
    notification_id = int(notification_id)
    old_notification = NotificationDao.get_notification_by_id(
        notification_id=notification_id
    )

    if old_notification is None:
        response = jsonify(
            {
                "self": f"/v2/notifications/{notification_id}",
                "updated": False,
                "notification": None,
                "error": "there is no existing notification with this id",
            }
        )
        response.status_code = 400
        return response

    notification_data: dict = request.get_json()
    new_notification = Notification(notification_data)
    new_notification.notification_id = notification_id

    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get("sub")

    if old_notification.username == jwt_username:
        current_app.logger.info(
            f"User {jwt_username} is updating their notification with id {new_notification.notification_id}."
        )
    else:
        current_app.logger.info(
            f"User {jwt_username} is not authorized to update a notification sent to {old_notification.username}."
        )
        response = jsonify(
            {
                "self": f"/v2/notifications/{notification_id}",
                "updated": False,
                "notification": None,
                "error": f"User {jwt_username} is not authorized to update a notification sent to "
                f"{old_notification.username}.",
            }
        )
        response.status_code = 400
        return response

    if old_notification != new_notification:
        new_notification.modified_date = datetime.now()
        new_notification.modified_app = "saints-xctf-api"

        is_updated = NotificationDao.update_notification(notification=new_notification)

        if is_updated:
            updated_notification = NotificationDao.get_notification_by_id(
                notification_id=notification_id
            )
            notification_dict = NotificationData(updated_notification).__dict__
            notification_dict["time"] = str(notification_dict["time"])

            response = jsonify(
                {
                    "self": f"/v2/notifications/{notification_id}",
                    "updated": True,
                    "notification": notification_dict,
                }
            )
            response.status_code = 200
            return response

        response = jsonify(
            {
                "self": f"/v2/notifications/{notification_id}",
                "updated": False,
                "notification": None,
                "error": "the notification failed to update",
            }
        )
        response.status_code = 500
        return response

    response = jsonify(
        {
            "self": f"/v2/notifications/{notification_id}",
            "updated": False,
            "notification": None,
            "error": "the notification submitted is equal to the existing notification with the same id",
        }
    )
    response.status_code = 400
    return response


def notification_by_id_delete(notification_id) -> Response:
    """
    Hard delete an existing notification with a given unique ID.
    :param notification_id: Unique identifier for a user's notification.
    :return: A response object for the DELETE API request.
    """
    existing_notification: Notification = NotificationDao.get_notification_by_id(
        notification_id=notification_id
    )

    if existing_notification is None:
        response = jsonify(
            {
                "self": f"/v2/notifications/{notification_id}",
                "deleted": False,
                "error": "There is no existing notification with this id.",
            }
        )
        response.status_code = 400
        return response

    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get("sub")

    if existing_notification.username == jwt_username:
        current_app.logger.info(
            f"User {jwt_username} is deleting their notification with id {existing_notification.notification_id}."
        )
    else:
        current_app.logger.info(
            f"User {jwt_username} is not authorized to delete a notification sent to {existing_notification.username}."
        )
        response = jsonify(
            {
                "self": f"/v2/notifications/{notification_id}",
                "deleted": False,
                "error": f"User {jwt_username} is not authorized to delete a notification sent to "
                f"{existing_notification.username}.",
            }
        )
        response.status_code = 400
        return response

    is_deleted = NotificationDao.delete_notification_by_id(
        notification_id=notification_id
    )

    if is_deleted:
        response = jsonify(
            {
                "self": f"/v2/notifications/{notification_id}",
                "deleted": True,
            }
        )
        response.status_code = 204
        return response

    response = jsonify(
        {
            "self": f"/v2/notifications/{notification_id}",
            "deleted": False,
            "error": "failed to delete the notification",
        }
    )
    response.status_code = 500
    return response


def notification_by_id_soft_delete(notification_id) -> Response:
    """
    Soft delete an existing notification with a given unique ID.
    :param notification_id: The unique identifier for a user notification
    :return: A response object for the DELETE API request.
    """
    existing_notification: Notification = NotificationDao.get_notification_by_id(
        notification_id=notification_id
    )

    if existing_notification is None:
        response = jsonify(
            {
                "self": f"/v2/notifications/soft/{notification_id}",
                "deleted": False,
                "error": "there is no existing notification with this id",
            }
        )
        response.status_code = 400
        return response

    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get("sub")

    if existing_notification.username == jwt_username:
        current_app.logger.info(
            f"User {jwt_username} is soft deleting their notification with id {existing_notification.notification_id}."
        )
    else:
        current_app.logger.info(
            f"User {jwt_username} is not authorized to soft delete a notification sent to "
            f"{existing_notification.username}."
        )
        response = jsonify(
            {
                "self": f"/v2/notifications/soft/{notification_id}",
                "deleted": False,
                "error": f"User {jwt_username} is not authorized to soft delete a notification sent to "
                f"{existing_notification.username}.",
            }
        )
        response.status_code = 400
        return response

    # Update the notification model to reflect the soft delete
    existing_notification.deleted = True
    existing_notification.deleted_date = datetime.now()
    existing_notification.deleted_app = "saints-xctf-api"
    existing_notification.modified_date = datetime.now()
    existing_notification.modified_app = "saints-xctf-api"

    is_deleted: bool = NotificationDao.soft_delete_notification(existing_notification)

    if is_deleted:
        response = jsonify(
            {
                "self": f"/v2/notifications/soft/{notification_id}",
                "deleted": True,
            }
        )
        response.status_code = 204
        return response

    response = jsonify(
        {
            "self": f"/v2/notifications/soft/{notification_id}",
            "deleted": False,
            "error": "failed to soft delete the notification",
        }
    )
    response.status_code = 500
    return response


def notification_links_get() -> Response:
    """
    Get all the other notification API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify(
        {
            "self": "/v2/notifications/links",
            "endpoints": [
                {
                    "link": "/v2/notifications",
                    "verb": "GET",
                    "description": "Get all the user notifications in the database.",
                },
                {
                    "link": "/v2/notifications",
                    "verb": "POST",
                    "description": "Create a new user notification.",
                },
                {
                    "link": "/v2/notifications/<notification_id>",
                    "verb": "GET",
                    "description": "Retrieve a single user notification with a given unique id.",
                },
                {
                    "link": "/v2/notifications/<notification_id>",
                    "verb": "PUT",
                    "description": "Update a user notification with a given unique id.",
                },
                {
                    "link": "/v2/notifications/<notification_id>",
                    "verb": "DELETE",
                    "description": "Delete a user notification with a given unique id.",
                },
                {
                    "link": "/v2/notifications/soft/<notification_id>",
                    "verb": "DELETE",
                    "description": "Soft delete a user notification with a given unique id.",
                },
            ],
        }
    )
    response.status_code = 200
    return response
