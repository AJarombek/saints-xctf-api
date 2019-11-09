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
        :param comment: The original Comment object with auditing fields.
        """
        if comment is not None:
            self.comment_id = comment.comment_id
            self.username = comment.username
            self.first = comment.first
            self.last = comment.last
            self.log_id = comment.log_id
            self.time = comment.time
            self.content = comment.content
            self.deleted = comment.deleted

    def __str__(self):
        """
        String representation of the comment.  This representation is meant to be human readable.
        :return: The comment string.
        """
        return f"Comment: [comment_id: {self.comment_id}, username: {self.username}, first: {self.first}, " \
            f"last: {self.last}, log_id: {self.log_id}, time: {self.time}, content: {self.content}, " \
            f"deleted: {self.deleted}]"

    def __repr__(self):
        """
        String representation of the comment.  This representation is meant to be machine readable.
        :return: The comment string.
        """
        return '<Comment %r>' % self.comment_id

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this Comment.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            self.comment_id == other.comment_id,
            self.username == other.username,
            self.first == other.first,
            self.last == other.last,
            self.log_id == other.log_id,
            str(self.time) == str(other.time),
            self.content == other.content,
            self.deleted == other.deleted
        ])
