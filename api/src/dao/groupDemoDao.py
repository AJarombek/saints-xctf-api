"""
Group data access from the SaintsXCTF demo database.  Contains SQL queries related to group information.
Most membership data is accessed from a separate GroupMemberDemoDao.
Author: Andrew Jarombek
Date: 9/13/2022
"""

from sqlalchemy.engine.cursor import ResultProxy
from sqlalchemy.schema import Column

from app import app
from database import db
from utils.literals import WeekStart


class GroupDemoDao:
    engine = db.get_engine(app=app, bind="demo")

    @staticmethod
    def get_newest_log_date(group_name: str) -> Column:
        """
        Get the date of the newest exercise log in the group
        :param group_name: The unique name for the group
        :return: A date of an exercise log
        """
        result: ResultProxy = db.session.execute(
            """
            SELECT MAX(time_created) AS newest 
            FROM logs 
            INNER JOIN groupmembers ON logs.username = groupmembers.username 
            WHERE group_name=:group_name and status='accepted'
            AND logs.deleted IS FALSE
            AND groupmembers.deleted IS FALSE
            """,
            {"group_name": group_name},
            bind=GroupDemoDao.engine,
        )
        return result.first()
