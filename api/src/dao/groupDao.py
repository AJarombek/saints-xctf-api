"""
Group data access from the SaintsXCTF MySQL database.  Contains SQL queries related to group information.
Most membership data is accessed from a separate GroupMemberDao.
Author: Andrew Jarombek
Date: 7/2/2019
"""

from sqlalchemy.engine import ResultProxy
from sqlalchemy.schema import Column
from database import db
from dao.basicDao import BasicDao
from model.Group import Group


class GroupDao:

    @staticmethod
    def get_groups() -> list:
        """
        Retrieve all the groups in the database
        :return: The result of the query.
        """
        return Group.query.all()

    @staticmethod
    def get_group(group_name: str) -> Group:
        """
        Retrieve a group with a given name from the database.
        :param group_name: A name which uniquely identifies a group.
        :return: The result of the query.
        """
        return Group.query.filter_by(group_name=group_name).first()

    @staticmethod
    def get_newest_log_date(group_name: str) -> Column:
        """
        Get the date of the newest exercise log in the group
        :param group_name: The unique name for the group
        :return: A date of an exercise log
        """
        result: ResultProxy = db.session.execute(
            '''
            SELECT MAX(time_created) AS newest 
            FROM logs 
            INNER JOIN groupmembers ON logs.username = groupmembers.username 
            WHERE group_name=:group_name and status='accepted'
            ''',
            {'group_name': group_name}
        )
        return result.first()

    @staticmethod
    def get_newest_message_date(group_name: str) -> Column:
        """
        Get the date of the newest message in the group
        :param group_name: The unique name for the group
        :return: A date of a message
        """
        result: ResultProxy = db.session.execute(
            '''
            SELECT MAX(time) AS newest 
            FROM messages 
            WHERE group_name=:group_name
            ''',
            {'group_name': group_name}
        )
        return result.first()

    @staticmethod
    def update_group(group: Group) -> bool:
        """
        Update a group in the database. Certain fields (group_name, group_title) can't be modified.
        :param group: Object representing an updated group.
        :return: True if the group is updated in the database, False otherwise.
        """
        db.session.execute(
            '''
            UPDATE groups SET 
                grouppic=:grouppic, 
                grouppic_name=:grouppic_name, 
                description=:description, 
                week_start=:week_start,
                deleted=:deleted,
                modified_date=:modified_date,
                modified_app=:modified_app
            WHERE group_name=:group_name
            ''',
            {
                'grouppic': group.grouppic,
                'grouppic_name': group.grouppic_name,
                'description': group.description,
                'week_start': group.week_start,
                'deleted': group.deleted,
                'group_name': group.group_name,
                'modified_app': group.modified_app
            }
        )
        return BasicDao.safe_commit()
