"""
Comment model that only includes data columns.
Author: Andrew Jarombek
Date: 10/8/2019
"""

from . import Comment


class CommentData:
    def __init__(self, comment: Comment):
        """
        Create a comment object without any auditing fields.
        :param comment: A dictionary with fields matching the Comment fields
        """
        self.comment_id = comment.comment_id
        self.username = comment.username
        self.first = comment.first
        self.last = comment.last
        self.log_id = comment.log_id
        self.time = comment.time
        self.content = comment.content
        self.deleted = comment.deleted
