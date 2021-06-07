"""
Group data access from the SaintsXCTF MySQL database.  Contains SQL queries related to group information.
Most membership data is accessed from a separate GroupMemberDao.
Author: Andrew Jarombek
Date: 7/2/2019
"""

from typing import Optional, Literal

from sqlalchemy.engine.cursor import ResultProxy
from sqlalchemy.engine.row import RowProxy
from sqlalchemy.schema import Column

from database import db
from dao.basicDao import BasicDao
from model.Group import Group
from utils import dates

WeekStart = Literal['monday', 'sunday']


class GroupDao:

    @staticmethod
    def get_groups() -> list:
        """
        Retrieve all the groups in the database
        :return: The result of the query.
        """
        return Group.query\
            .filter(Group.deleted.is_(False))\
            .all()

    @staticmethod
    def get_group_by_id(group_id: int) -> Group:
        """
       Retrieve a group with a given id from the database.
       :param group_id: Unique id which identifies a group.
       :return: A Group object which is the result of the query.
       """
        return Group.query\
            .filter_by(id=group_id)\
            .filter(Group.deleted.is_(False))\
            .first()

    @staticmethod
    def get_group(team_name: str, group_name: str) -> Optional[RowProxy]:
        """
        Retrieve a group with a given name from the database.
        :param team_name: Unique name which identifies a team.
        :param group_name: Unique name which identifies a group within a team.
        :return: The result of the query.
        """
        result: ResultProxy = db.session.execute(
            '''
            SELECT `groups`.id, `groups`.group_name, group_title, grouppic_name, description, week_start
            FROM `groups` 
            INNER JOIN teamgroups ON `groups`.group_name = teamgroups.group_name
            WHERE `groups`.group_name=:group_name
            AND team_name=:team_name
            AND `groups`.deleted IS FALSE
            AND teamgroups.deleted IS FALSE
            ''',
            {'team_name': team_name, 'group_name': group_name}
        )
        return result.first()

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
            AND logs.deleted IS FALSE
            AND groupmembers.deleted IS FALSE
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
            AND deleted IS FALSE
            ''',
            {'group_name': group_name}
        )
        return result.first()

    @staticmethod
    def get_group_leaderboard(group_id: int, interval: str = None, week_start: WeekStart = 'monday') -> ResultProxy:
        """
        Get exercise statistics from users in a specific group.  These statistics are used to build a leaderboard in the
        application.
        :param group_id: The unique id for the group.
        :param interval: A string representing a time interval (week, month, or year).
        :param week_start: Day of the week that is used to signify the start of the week.
        :return: Records with a users exercise statistics over an interval.
        """
        date = dates.get_start_date_interval(interval=interval, week_start=week_start)

        if date is None:
            return db.session.execute(
                """
                SELECT 
                    groupmembers.username,
                    MAX(logs.first) AS first,
                    MAX(logs.last) AS last,
                    COALESCE(SUM(miles), 0) AS miles, 
                    COALESCE(SUM(CASE WHEN type = 'run' THEN miles END), 0) AS miles_run,
                    COALESCE(SUM(CASE WHEN type = 'bike' THEN miles END), 0) AS miles_biked,
                    COALESCE(SUM(CASE WHEN type = 'swim' THEN miles END), 0) AS miles_swam,
                    COALESCE(SUM(CASE WHEN type = 'other' THEN miles END), 0) AS miles_other 
                FROM logs 
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_id = :group_id 
                AND status = 'accepted' 
                AND logs.deleted IS FALSE
                AND groupmembers.deleted IS FALSE
                GROUP BY groupmembers.username 
                ORDER BY miles DESC
                """,
                {'group_id': group_id}
            )
        else:
            return db.session.execute(
                """
                SELECT 
                    groupmembers.username,
                    MAX(logs.first) AS first,
                    MAX(logs.last) AS last,
                    COALESCE(SUM(miles), 0) AS miles, 
                    COALESCE(SUM(CASE WHEN type = 'run' THEN miles END), 0) AS miles_run,
                    COALESCE(SUM(CASE WHEN type = 'bike' THEN miles END), 0) AS miles_biked,
                    COALESCE(SUM(CASE WHEN type = 'swim' THEN miles END), 0) AS miles_swam,
                    COALESCE(SUM(CASE WHEN type = 'other' THEN miles END), 0) AS miles_other 
                FROM logs 
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_id = :group_id 
                AND date >= :date 
                AND status = 'accepted' 
                AND logs.deleted IS FALSE
                AND groupmembers.deleted IS FALSE
                GROUP BY groupmembers.username 
                ORDER BY miles DESC
                """,
                {'group_id': group_id, 'date': date}
            )

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
                modified_date=:modified_date,
                modified_app=:modified_app
            WHERE group_name=:group_name
            AND deleted IS FALSE
            ''',
            {
                'grouppic': group.grouppic,
                'grouppic_name': group.grouppic_name,
                'description': group.description,
                'week_start': group.week_start,
                'group_name': group.group_name,
                'modified_date': group.modified_date,
                'modified_app': group.modified_app
            }
        )
        return BasicDao.safe_commit()
