"""
Group data access from the SaintsXCTF MySQL database.  Contains SQL queries related to group information.
Most membership data is accessed from a separate GroupMemberDao.
Author: Andrew Jarombek
Date: 7/2/2019
"""

from database import db
from dao.basicDao import BasicDao
from model.Group import Group
from model.GroupMember import GroupMember


class GroupDao:

    @staticmethod
    def get_newest_log_date(group_name: str) -> str:
        """
        Get the date of the newest exercise log in the group
        :param group_name: The unique name for the group
        :return: A date of an exercise log
        """
        return db.session.execute(
            '''
            SELECT MAX(time_created) AS newest 
            FROM logs 
            INNER JOIN groupmembers ON logs.username = groupmembers.username 
            WHERE group_name=:group_name and status='accepted'
            ''',
            {'group_name': group_name}
        )

    @staticmethod
    def get_newest_message_date(group_name: str) -> str:
        """
        Get the date of the newest message in the group
        :param group_name: The unique name for the group
        :return: A date of a message
        """
        return db.session.execute(
            '''
            SELECT MAX(time) AS newest 
            FROM messages 
            WHERE group_name=:group_name
            ''',
            {'group_name': group_name}
        )