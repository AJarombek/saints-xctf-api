"""
Comment routes in the SaintsXCTF API.  Used for retrieving, adding, updating, and deleting comments on exercise logs.
Author: Andrew Jarombek
Date: 7/12/2019
"""

from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, Response
from dao.commentDao import CommentDao
from model.Comment import Comment

comment_route = Blueprint('comment_route', __name__, url_prefix='/v2/comments')


@comment_route.route('/', methods=['GET', 'POST'])
def comments() -> Response:
    """
    Endpoints for retrieving all the comments and creating new comments.
    :return: JSON representation of comments on exercise logs and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/comments '''
        comments_get()

    elif request.method == 'POST':
        ''' [POST] /v2/comments '''
        comment_post()


@comment_route.route('/<comment_id>', methods=['GET', 'PUT', 'DELETE'])
def comment_with_id(comment_id) -> Response:
    """
    Endpoints for retrieving a single comments, editing an existing comment, and deleting a comment.
    :param comment_id: Unique identifier for a comment.
    :return: JSON representation of a comment and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/comments/<comment_id> '''
        comment_with_id_get(comment_id)

    elif request.method == 'PUT':
        ''' [PUT] /v2/comments/<comment_id> '''
        comment_with_id_put(comment_id)

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/comments/<comment_id> '''
        comment_with_id_delete(comment_id)


@comment_route.route('/soft/<comment_id>', methods=['DELETE'])
def activation_code_soft_by_code(comment_id) -> Response:
    """
    Endpoints for soft deleting comments.
    :param comment_id: Unique identifier for a comment.
    :return: JSON representation of comments and relevant metadata.
    """
    if request.method == 'DELETE':
        ''' [DELETE] /v2/comments/soft/<code> '''
        return comment_with_id_soft_delete(comment_id)


@comment_route.route('/links', methods=['GET'])
def comment_links() -> Response:
    """
    Endpoint for information about the comment API endpoints.
    :return: Metadata about the comment API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/comments/links '''
        return comment_links_get()


def comments_get():
    comments: list = CommentDao.get_comments()

    if comments is None:
        response = jsonify({
            'self': '/v2/comments',
            'comments': None,
            'error': 'an unexpected error occurred retrieving comments'
        })
        response.status_code = 500
        return response
    else:
        for comment in comments:
            comment.log = f'/v2/logs/{comment.log_id}'

        response = jsonify({
            'self': '/v2/comments',
            'comments': comments
        })
        response.status_code = 200
        return response


def comment_post():
    comment_data: dict = request.get_json()
    comment_to_add = Comment(comment_data)
    comment_added_successfully = CommentDao.add_comment(new_comment=comment_to_add)

    if comment_added_successfully:
        comment_added = CommentDao.get_comment_by_id(comment_to_add.comment_id)
        comment_added_dict: dict = comment_added.__dict__
        del comment_added_dict['_sa_instance_state']

        response = jsonify({
            'self': '/v2/comments',
            'added': True,
            'comment': comment_added_dict
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            'self': '/v2/comments',
            'added': False,
            'comment': None,
            'error': 'failed to create a new comment'
        })
        response.status_code = 500
        return response


def comment_with_id_get(comment_id):
    comment = CommentDao.get_comment_by_id(comment_id=comment_id)

    if comment is None:
        response = jsonify({
            'self': f'/v2/comments/{comment_id}',
            'comment': None,
            'log': None,
            'error': 'there is no comment with this identifier'
        })
        response.status_code = 400
        return response
    else:
        response = jsonify({
            'self': f'/v2/comments/{comment_id}',
            'comment': comment,
            'log': f'/v2/logs/{comment.get("log_id")}'
        })
        response.status_code = 200
        return response


def comment_with_id_put(comment_id):
    old_comment = CommentDao.get_comment_by_id(comment_id=comment_id)

    if old_comment is None:
        response = jsonify({
            'self': f'/v2/comments/{comment_id}',
            'updated': False,
            'comment': None,
            'error': 'there is no existing comment with this id'
        })
        response.status_code = 400
        return response

    comment_data: dict = request.get_json()
    new_comment = Comment(comment_data)

    if old_comment != new_comment:
        is_updated = CommentDao.update_comment(comment=new_comment)

        if is_updated:
            updated_comment: Comment = CommentDao.get_comment_by_id(comment_id=new_comment.comment_id)
            updated_comment_dict: dict = updated_comment.__dict__
            del updated_comment_dict['_sa_instance_state']

            response = jsonify({
                'self': f'/v2/comments/{comment_id}',
                'updated': True,
                'comment': updated_comment_dict
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': f'/v2/comments/{comment_id}',
                'updated': False,
                'comment': None,
                'error': 'the comment failed to update'
            })
            response.status_code = 500
            return response
    else:
        response = jsonify({
            'self': f'/v2/comments/{comment_id}',
            'updated': False,
            'comment': None,
            'error': 'the comment submitted is equal to the existing comment with the same id'
        })
        response.status_code = 400
        return response


def comment_with_id_delete(comment_id):
    is_deleted = CommentDao.delete_comment_by_id(comment_id=comment_id)

    if is_deleted:
        response = jsonify({
            'self': f'/v2/comments/{comment_id}',
            'deleted': True,
        })
        response.status_code = 204
        return response
    else:
        response = jsonify({
            'self': f'/v2/comments/{comment_id}',
            'deleted': False,
            'error': 'failed to delete the comment'
        })
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
        response = jsonify({
            'self': f'/v2/comments/soft/{comment_id}',
            'deleted': False,
            'error': 'there is no existing comment with this id'
        })
        response.status_code = 400
        return response

    # Update the comment model to reflect the soft delete
    existing_comment.deleted = True
    existing_comment.deleted_date = datetime.now()
    existing_comment.deleted_app = 'api'
    existing_comment.modified_date = datetime.now()
    existing_comment.modified_app = 'api'

    is_deleted: bool = CommentDao.soft_delete_comment_by_id(existing_comment)

    if is_deleted:
        response = jsonify({
            'self': f'/v2/comments/soft/{comment_id}',
            'deleted': True,
        })
        response.status_code = 204
        return response
    else:
        response = jsonify({
            'self': f'/v2/comments/soft/{comment_id}',
            'deleted': False,
            'error': 'failed to soft delete the comment'
        })
        response.status_code = 500
        return response


def comment_links_get() -> Response:
    """
    Get all the other comment API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/comments/links',
        'endpoints': [
            {
                'link': '/v2/comments',
                'verb': 'GET',
                'description': 'Get all the comments in the database.'
            },
            {
                'link': '/v2/comments',
                'verb': 'POST',
                'description': 'Create a new comment.'
            },
            {
                'link': '/v2/comments/<comment_id>',
                'verb': 'GET',
                'description': 'Retrieve a single comment with a given unique id.'
            },
            {
                'link': '/v2/comments/<comment_id>',
                'verb': 'PUT',
                'description': 'Update a comment with a given unique id.'
            },
            {
                'link': '/v2/comments/<comment_id>',
                'verb': 'DELETE',
                'description': 'Delete a single comment with a given unique id.'
            },
            {
                'link': '/v2/comments/soft/<comment_id>',
                'verb': 'DELETE',
                'description': 'Soft delete a single comment with a given unique id.'
            }
        ],
    })
    response.status_code = 200
    return response
