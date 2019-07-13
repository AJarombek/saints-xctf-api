"""
Comment routes in the SaintsXCTF API.  Used for retrieving, adding, updating, and deleting comments on exercise logs.
Author: Andrew Jarombek
Date: 7/12/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.logDao import LogDao
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
            response = jsonify({
                'self': '/v2/comments',
                'comments': comments
            })
            response.status_code = 200
            return response

    elif request.method == 'POST':
        ''' [POST] /v2/comments '''
        pass


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
    elif request.method == 'PUT':
        ''' [PUT] /v2/comments/<comment_id> '''
        pass
    elif request.method == 'DELETE':
        ''' [DELETE] /v2/comments/<comment_id> '''
        pass
