"""
Comment data access from the SaintsXCTF MySQL database.  Contains comments posted on exercise logs.
Author: Andrew Jarombek
Date: 7/3/2019
"""

from database import db
from dao.basicDao import BasicDao
from model.Comment import Comment


class CommentDao:

    @staticmethod
    def get_comments() -> list:
        """
        Retrieve all the comments in the database.
        :return: The result of the query.
        """
        return Comment.query.order_by(Comment.time).all()

    @staticmethod
    def get_comment_by_id(comment_id: int) -> dict:
        """
        Retrieve a single comment by its unique id
        :param comment_id: The unique identifier for a comment.
        :return: The result of the query.
        """
        return Comment.query.filter_by(comment_id=comment_id).first()

    @staticmethod
    def get_comments_by_log_id(log_id: int) -> list:
        """
        Retrieve all the comments on a specific exercise log.
        :param log_id: Unique identifier for an exercise log.
        :return: The result of the query.
        """
        return db.session.query(
            '''
            SELECT * FROM comments 
            WHERE log_id=:log_id 
            ORDER BY time DESC
            ''',
            {'log_id': log_id}
        )

    @staticmethod
    def add_comment(new_comment: Comment) -> bool:
        """
        Add a comment for an exercise log to the database.
        :param new_comment: Object representing a comment for an exercise log.
        :return: True if the comment is inserted into the database, False otherwise.
        """
        db.session.add(new_comment)
        return BasicDao.safe_commit()

    @staticmethod
    def delete_comments_by_log_id(log_id: int) -> bool:
        """
        Delete comments from the database based on the log they are bound 2.
        :param log_id: ID which uniquely identifies the log.
        :return: True if the deletions were successful without error, False otherwise.
        """
        db.session.execute(
            'DELETE FROM comments WHERE log_id=:log_id',
            {'log_id': log_id}
        )
        return BasicDao.safe_commit()
