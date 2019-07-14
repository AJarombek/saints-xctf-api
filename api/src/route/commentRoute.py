"""
Comment routes in the SaintsXCTF API.  Used for retrieving, adding, updating, and deleting comments on exercise logs.
Author: Andrew Jarombek
Date: 7/12/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.commentDao import CommentDao
from model.Comment import Comment

comment_route = Blueprint('comment_route', __name__, url_prefix='/v2/comments')


@comment_route.route('/', methods=['GET', 'POST'])
def comments():
    """
    Endpoints for retrieving all the comments and creating new comments.
    :return: JSON representation of comments on exercise logs and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/comments '''
        comments = CommentDao.get_comments()

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

    elif request.method == 'POST':
        ''' [POST] /v2/comments '''
        comment_data: dict = request.get_json()
        comment_to_add = Comment(comment_data)
        comment_added_successfully = CommentDao.add_comment(new_comment=comment_to_add)

        if comment_added_successfully:
            comment_added = CommentDao.get_comment_by_id(comment_to_add.comment_id)

            response = jsonify({
                'self': '/v2/comments',
                'added': True,
                'comment': comment_added
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


@comment_route.route('/<comment_id>', methods=['GET', 'PUT', 'DELETE'])
def comment_with_id(comment_id):
    """
    Endpoints for retrieving a single comments, editing an existing comment, and deleting a comment.
    :param comment_id: Unique identifier for a comment.
    :return: JSON representation of a comment and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/comments/<comment_id> '''
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

    elif request.method == 'PUT':
        ''' [PUT] /v2/comments/<comment_id> '''
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
                updated_comment = CommentDao.get_comment_by_id(comment_id=new_comment.comment_id)

                response = jsonify({
                    'self': f'/v2/comments/{comment_id}',
                    'updated': True,
                    'comment': updated_comment
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

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/comments/<comment_id> '''
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
