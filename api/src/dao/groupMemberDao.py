"""
GroupMember data access from the SaintsXCTF MySQL database.  Contains SQL queries related to users
who are members of a group.  Most group data is accessed from a separate GroupDao.
Author: Andrew Jarombek
Date: 7/2/2019
"""

from database import db
from dao.basicDao import BasicDao
from model.Group import Group
from model.GroupMember import GroupMember


class GroupMemberDao:

    @staticmethod
    def get_user_groups(username: str) -> list:
        """
        Get information about all the groups a user is a member of
        :param username: Unique identifier for the user
        :return: A list of groups
        """
        return db.session.execute(
            '''
            SELECT groupmembers.group_name,group_title,status,user 
            FROM groupmembers 
            INNER JOIN groups ON groups.group_name=groupmembers.group_name 
            WHERE username=:username
            ''',
            {'username': username}
        )