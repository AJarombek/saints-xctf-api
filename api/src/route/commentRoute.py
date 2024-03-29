"""
Comment routes in the SaintsXCTF API.  Used for retrieving, adding, updating, and deleting comments on exercise logs.
Author: Andrew Jarombek
Date: 7/12/2019
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
from dao.commentDao import CommentDao
from model.Comment import Comment
from model.CommentData import CommentData

comment_route = Blueprint("comment_route", __name__, url_prefix="/v2/comments")


@comment_route.route("", methods=["GET", "POST"])
@auth_required()
def comments_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'comments' to the comment routes.
    :return: Response object letting the browser know where to redirect the request to.
    """
    if request.method == "GET":
        """[GET] /v2/comments"""
        return redirect(url_for("comment_route.comments"), code=302)

    if request.method == "POST":
        """[POST] /v2/comments"""
        return redirect(url_for("comment_route.comments"), code=307)

    return abort(404)


@comment_route.route("/", methods=["GET", "POST"])
@auth_required()
@swag_from("swagger/commentRoute/commentsGet.yml", methods=["GET"])
@swag_from("swagger/commentRoute/commentPost.yml", methods=["POST"])
def comments() -> Response:
    """
    Endpoints for retrieving all the comments and creating new comments.
    :return: JSON representation of comments on exercise logs and relevant metadata.
    """
    if request.method == "GET":
        """[GET] /v2/comments"""
        return comments_get()

    if request.method == "POST":
        """[POST] /v2/comments"""
        return comment_post()

    return abort(404)


@comment_route.route("/<comment_id>", methods=["GET", "PUT", "DELETE"])
@auth_required()
@swag_from("swagger/commentRoute/commentGet.yml", methods=["GET"])
@swag_from("swagger/commentRoute/commentPut.yml", methods=["PUT"])
@swag_from("swagger/commentRoute/commentDelete.yml", methods=["DELETE"])
def comment_with_id(comment_id) -> Response:
    """
    Endpoints for retrieving a single comments, editing an existing comment, and deleting a comment.
    :param comment_id: Unique identifier for a comment.
    :return: JSON representation of a comment and relevant metadata.
    """
    if request.method == "GET":
        """[GET] /v2/comments/<comment_id>"""
        return comment_with_id_get(comment_id)

    if request.method == "PUT":
        """[PUT] /v2/comments/<comment_id>"""
        return comment_with_id_put(comment_id)

    if request.method == "DELETE":
        """[DELETE] /v2/comments/<comment_id>"""
        return comment_with_id_delete(comment_id)

    return abort(404)


@comment_route.route("/soft/<comment_id>", methods=["DELETE"])
@auth_required()
@swag_from("swagger/commentRoute/commentSoftDelete.yml", methods=["DELETE"])
def comment_soft_by_code(comment_id) -> Response:
    """
    Endpoints for soft deleting comments.
    :param comment_id: Unique identifier for a comment.
    :return: JSON representation of comments and relevant metadata.
    """
    if request.method == "DELETE":
        """[DELETE] /v2/comments/soft/<code>"""
        return comment_with_id_soft_delete(comment_id)

    return abort(404)


@comment_route.route("/links", methods=["GET"])
@swag_from("swagger/commentRoute/commentLinks.yml", methods=["GET"])
def comment_links() -> Response:
    """
    Endpoint for information about the comment API endpoints.
    :return: Metadata about the comment API.
    """
    if request.method == "GET":
        """[GET] /v2/comments/links"""
        return comment_links_get()

    return abort(404)


def comments_get():
    """
    Get all the comments in the database.
    :return: A response object for the GET API request.
    """
    comments_data: list = CommentDao.get_comments()

    if comments_data is None:
        response = jsonify(
            {
                "self": "/v2/comments",
                "comments": None,
                "error": "an unexpected error occurred retrieving comments",
            }
        )
        response.status_code = 500
        return response

    comment_dicts = [CommentData(comment).__dict__ for comment in comments_data]

    for comment_dict in comment_dicts:
        comment_dict["log"] = f'/v2/logs/{comment_dict.get("log_id")}'

    response = jsonify({"self": "/v2/comments", "comments": comment_dicts})
    response.status_code = 200
    return response


def comment_post():
    """
    Create a new comment.
    :return: A response object for the POST API request.
    """
    comment_data: dict = request.get_json(silent=True)

    if comment_data is None:
        response = jsonify(
            {
                "self": "/v2/comments",
                "added": False,
                "comment": None,
                "error": "the request body isn't populated",
            }
        )
        response.status_code = 400
        return response

    comment_to_add = Comment(comment_data)

    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get("sub")

    if comment_to_add.username == jwt_username:
        # You are so loved.
        current_app.logger.info(
            f"User {jwt_username} is creating a comment on log {comment_to_add.log_id}."
        )
    else:
        current_app.logger.info(
            f"User {jwt_username} is not authorized to create a comment for user {comment_to_add.username}."
        )
        response = jsonify(
            {
                "self": "/v2/comments",
                "added": False,
                "comment": None,
                "error": f"User {jwt_username} is not authorized to create a comment for user {comment_to_add.username}.",
            }
        )
        response.status_code = 400
        return response

    if None in [
        comment_to_add.username,
        comment_to_add.first,
        comment_to_add.last,
        comment_to_add.log_id,
    ]:
        response = jsonify(
            {
                "self": "/v2/comments",
                "added": False,
                "comment": None,
                "error": "'username', 'first', 'last', and 'log_id' are required fields",
            }
        )
        response.status_code = 400
        return response

    comment_to_add.time = datetime.now()
    comment_to_add.created_date = datetime.now()
    comment_to_add.created_app = "saints-xctf-api"
    comment_to_add.created_user = None
    comment_to_add.modified_date = None
    comment_to_add.modified_app = None
    comment_to_add.modified_user = None
    comment_to_add.deleted_date = None
    comment_to_add.deleted_app = None
    comment_to_add.deleted_user = None
    comment_to_add.deleted = False

    comment_added_successfully: bool = CommentDao.add_comment(
        new_comment=comment_to_add
    )

    if comment_added_successfully:
        comment_added = CommentDao.get_comment_by_id(comment_to_add.comment_id)
        comment_added_dict: dict = CommentData(comment_added).__dict__

        response = jsonify(
            {"self": "/v2/comments", "added": True, "comment": comment_added_dict}
        )
        response.status_code = 200
        return response

    response = jsonify(
        {
            "self": "/v2/comments",
            "added": False,
            "comment": None,
            "error": "failed to create a new comment",
        }
    )
    response.status_code = 500
    return response


def comment_with_id_get(comment_id):
    """
    Get a single comment with a unique ID.
    :param comment_id: The unique identifier for a comment.
    :return: A response object for the GET API request.
    """
    comment = CommentDao.get_comment_by_id(comment_id=comment_id)

    if comment is None:
        response = jsonify(
            {
                "self": f"/v2/comments/{comment_id}",
                "comment": None,
                "log": None,
                "error": "there is no comment with this identifier",
            }
        )
        response.status_code = 400
        return response

    comment_dict: dict = CommentData(comment).__dict__
    comment_dict["time"] = str(comment_dict["time"])

    response = jsonify(
        {
            "self": f"/v2/comments/{comment_id}",
            "comment": comment_dict,
            "log": f'/v2/logs/{comment_dict.get("log_id")}',
        }
    )
    response.status_code = 200
    return response


def comment_with_id_put(comment_id):
    """
    Update an existing comment.
    :param comment_id: The unique identifier for a comment.
    :return: A response object for the PUT API request.
    """
    old_comment: Comment = CommentDao.get_comment_by_id(comment_id=comment_id)

    if old_comment is None:
        response = jsonify(
            {
                "self": f"/v2/comments/{comment_id}",
                "updated": False,
                "comment": None,
                "error": "there is no existing comment with this id",
            }
        )
        response.status_code = 400
        return response

    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get("sub")

    if old_comment.username == jwt_username:
        current_app.logger.info(
            f"User {jwt_username} is updating a comment with id {old_comment.comment_id}."
        )
    else:
        current_app.logger.info(
            f"User {jwt_username} is not authorized to update a comment with id {old_comment.comment_id}."
        )
        response = jsonify(
            {
                "self": f"/v2/comments/{comment_id}",
                "updated": False,
                "comment": None,
                "error": f"User {jwt_username} is not authorized to update a comment with id {old_comment.comment_id}.",
            }
        )
        response.status_code = 400
        return response

    comment_data: dict = request.get_json()
    new_comment = Comment(comment_data)

    if old_comment != new_comment:
        new_comment.modified_date = datetime.now()
        new_comment.modified_app = "saints-xctf-api"

        is_updated = CommentDao.update_comment(comment=new_comment)

        if is_updated:
            updated_comment: Comment = CommentDao.get_comment_by_id(
                comment_id=new_comment.comment_id
            )
            updated_comment_dict: dict = CommentData(updated_comment).__dict__

            response = jsonify(
                {
                    "self": f"/v2/comments/{comment_id}",
                    "updated": True,
                    "comment": updated_comment_dict,
                }
            )
            response.status_code = 200
            return response

        response = jsonify(
            {
                "self": f"/v2/comments/{comment_id}",
                "updated": False,
                "comment": None,
                "error": "the comment failed to update",
            }
        )
        response.status_code = 500
        return response

    response = jsonify(
        {
            "self": f"/v2/comments/{comment_id}",
            "updated": False,
            "comment": None,
            "error": "the comment submitted is equal to the existing comment with the same id",
        }
    )
    response.status_code = 400
    return response


def comment_with_id_delete(comment_id):
    """
    Delete an existing comment.
    :param comment_id: The unique identifier for a comment.
    :return: A response object for the DELETE API request.
    """
    existing_comment: Comment = CommentDao.get_comment_by_id(comment_id=comment_id)

    if existing_comment is None:
        response = jsonify(
            {
                "self": f"/v2/comments/{comment_id}",
                "deleted": False,
                "error": "there is no existing comment with this id",
            }
        )
        response.status_code = 400
        return response

    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get("sub")

    if existing_comment.username == jwt_username:
        current_app.logger.info(
            f"User {jwt_username} is deleting a comment with id {existing_comment.comment_id}."
        )
    else:
        current_app.logger.info(
            f"User {jwt_username} is not authorized to delete a comment with id {existing_comment.comment_id}."
        )
        response = jsonify(
            {
                "self": f"/v2/comments/{comment_id}",
                "deleted": False,
                "error": f"User {jwt_username} is not authorized to delete a comment with id {existing_comment.comment_id}.",
            }
        )
        response.status_code = 400
        return response

    is_deleted = CommentDao.delete_comment_by_id(comment_id=comment_id)

    if is_deleted:
        response = jsonify(
            {
                "self": f"/v2/comments/{comment_id}",
                "deleted": True,
            }
        )
        response.status_code = 204
        return response

    response = jsonify(
        {
            "self": f"/v2/comments/{comment_id}",
            "deleted": False,
            "error": "failed to delete the comment",
        }
    )
    response.status_code = 500
    return response


def comment_with_id_soft_delete(comment_id):
    """
    Soft delete a comment based on a unique id.
    :param comment_id: Unique identifier for a comment.
    :return: A response object for the DELETE API request.
    """
    existing_comment: Comment = CommentDao.get_comment_by_id(comment_id=comment_id)

    if existing_comment is None:
        response = jsonify(
            {
                "self": f"/v2/comments/soft/{comment_id}",
                "deleted": False,
                "error": "there is no existing comment with this id",
            }
        )
        response.status_code = 400
        return response

    jwt_claims: dict = get_claims(request)
    jwt_username = jwt_claims.get("sub")

    if existing_comment.username == jwt_username:
        current_app.logger.info(
            f"User {jwt_username} is soft deleting a comment with id {existing_comment.comment_id}."
        )
    else:
        current_app.logger.info(
            f"User {jwt_username} is not authorized to soft delete a comment with id {existing_comment.comment_id}."
        )
        response = jsonify(
            {
                "self": f"/v2/comments/soft/{comment_id}",
                "deleted": False,
                "error": f"User {jwt_username} is not authorized to soft delete a comment with id "
                f"{existing_comment.comment_id}.",
            }
        )
        response.status_code = 400
        return response

    # Update the comment model to reflect the soft delete
    existing_comment.deleted = True
    existing_comment.deleted_date = datetime.now()
    existing_comment.deleted_app = "saints-xctf-api"
    existing_comment.modified_date = datetime.now()
    existing_comment.modified_app = "saints-xctf-api"

    is_deleted: bool = CommentDao.soft_delete_comment(existing_comment)

    if is_deleted:
        response = jsonify(
            {
                "self": f"/v2/comments/soft/{comment_id}",
                "deleted": True,
            }
        )
        response.status_code = 204
        return response

    response = jsonify(
        {
            "self": f"/v2/comments/soft/{comment_id}",
            "deleted": False,
            "error": "failed to soft delete the comment",
        }
    )
    response.status_code = 500
    return response


def comment_links_get() -> Response:
    """
    Get all the other comment API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify(
        {
            "self": "/v2/comments/links",
            "endpoints": [
                {
                    "link": "/v2/comments",
                    "verb": "GET",
                    "description": "Get all the comments in the database.",
                },
                {
                    "link": "/v2/comments",
                    "verb": "POST",
                    "description": "Create a new comment.",
                },
                {
                    "link": "/v2/comments/<comment_id>",
                    "verb": "GET",
                    "description": "Retrieve a single comment with a given unique id.",
                },
                {
                    "link": "/v2/comments/<comment_id>",
                    "verb": "PUT",
                    "description": "Update a comment with a given unique id.",
                },
                {
                    "link": "/v2/comments/<comment_id>",
                    "verb": "DELETE",
                    "description": "Delete a single comment with a given unique id.",
                },
                {
                    "link": "/v2/comments/soft/<comment_id>",
                    "verb": "DELETE",
                    "description": "Soft delete a single comment with a given unique id.",
                },
            ],
        }
    )
    response.status_code = 200
    return response
