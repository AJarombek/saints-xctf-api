"""
GroupMember data access from the SaintsXCTF demo database.  Contains SQL queries related to users
who are members of a group.  Most group data is accessed from a separate GroupDao.
Author: Andrew Jarombek
Date: 9/12/2022
"""

from sqlalchemy.engine.cursor import ResultProxy

from app import app
from database import db


class GroupMemberDemoDao:
    engine = db.get_engine(app=app, bind="demo")

    @staticmethod
    def get_user_groups(username: str) -> ResultProxy:
        """
        Get information about all the groups a user is a member of
        :param username: Unique identifier for the user
        :return: A list of groups
        """
        return db.session.execute(
            """
            SELECT `groups`.id, groupmembers.group_name, group_title, status, user
            FROM groupmembers 
            INNER JOIN `groups` ON `groups`.group_name=groupmembers.group_name 
            WHERE username=:username
            AND groupmembers.deleted IS FALSE 
            AND `groups`.deleted IS FALSE 
            """,
            {"username": username},
            bind=GroupMemberDemoDao.engine,
        )
