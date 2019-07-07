"""
Comment data access from the SaintsXCTF MySQL database.  Contains comments posted on exercise logs.
Author: Andrew Jarombek
Date: 7/3/2019
"""

from database import db
from model.Comment import Comment


class CommentDao:

    @staticmethod
    def get_comment_by_log_id(log_id: int) -> list:
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
