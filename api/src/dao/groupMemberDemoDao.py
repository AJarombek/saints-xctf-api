"""
GroupMember data access from the SaintsXCTF demo database.  Contains SQL queries related to users
who are members of a group.  Most group data is accessed from a separate GroupDao.
Author: Andrew Jarombek
Date: 9/12/2022
"""

from sqlalchemy.engine.cursor import ResultProxy

from app import app
from database import db
from dao.common.groupMemberDao import GroupMemberCommonDao


class GroupMemberDemoDao:
    engine = db.get_engine(app=app, bind="demo")

    @staticmethod
    def get_user_groups(username: str) -> ResultProxy:
        """
        Get information about all the groups a user is a member of
        :param username: Unique identifier for the user
        :return: A list of groups
        """
        return GroupMemberCommonDao.get_user_groups(GroupMemberDemoDao.engine, username)

    @staticmethod
    def get_user_groups_in_team(username: str, team_name: str) -> ResultProxy:
        """
        Get information about all the groups a user is a member of within a team
        :param username: Unique identifier for the user
        :param team_name: Unique name for a team
        :return: A list of groups
        """
        return GroupMemberCommonDao.get_user_groups_in_team(
            GroupMemberDemoDao.engine, username, team_name
        )
