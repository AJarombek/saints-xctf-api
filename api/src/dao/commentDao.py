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
    def get_comment_by_id(comment_id: int) -> Comment:
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
        return db.session.execute(
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
    def update_comment(comment: Comment) -> bool:
        """
        Update a comment in the database. Certain fields (log_id, username, first, last) can't be modified.
        :param comment: Object representing an updated comment.
        :return: True if the comment is updated in the database, False otherwise.
        """
        db.session.execute(
            '''
            UPDATE comments SET 
                time=:time, 
                content=:content 
            WHERE comment_id=:comment_id
            ''',
            {
                'comment_id': comment.comment_id,
                'time': comment.time,
                'content': comment.content
            }
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_comment_by_id(comment_id: int) -> bool:
        """
        Delete a comment from the database based on its id.
        :param comment_id: ID which uniquely identifies the comment.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            'DELETE FROM comments WHERE comment_id=:comment_id',
            {'comment_id': comment_id}
        )
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

    @staticmethod
    def soft_delete_comment_by_id(comment: Comment) -> bool:
        """
        Soft Delete a comment from the database.
        :param comment: Object representing a comment to soft delete.
        :return: True if the soft deletion was successful without error, False otherwise.
        """
        db.session.add(comment)
        return BasicDao.safe_commit()
