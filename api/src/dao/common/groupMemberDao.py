"""
Common GroupMember data access functions.  Contains SQL queries related to users who are members of a group.
Most group data is accessed from a separate GroupDao.
Author: Andrew Jarombek
Date: 10/9/2022
"""

from sqlalchemy.engine.cursor import ResultProxy
from sqlalchemy.engine import Engine

from database import db


class GroupMemberCommonDao:
    @staticmethod
    def get_user_groups(engine: Engine, username: str) -> ResultProxy:
        """
        Get information about all the groups a user is a member of
        :param engine: Engine (database connection details) to use for the database request
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
            bind=engine,
        )

    @staticmethod
    def get_user_groups_in_team(
        engine: Engine, username: str, team_name: str
    ) -> ResultProxy:
        """
        Get information about all the groups a user is a member of within a team
        :param engine: Engine (database connection details) to use for the database request
        :param username: Unique identifier for the user
        :param team_name: Unique name for a team
        :return: A list of groups
        """
        return db.session.execute(
            """
            SELECT groupmembers.group_name,groupmembers.group_id,group_title,status,user 
            FROM groupmembers 
            INNER JOIN `groups` ON `groups`.group_name=groupmembers.group_name 
            INNER JOIN teamgroups ON teamgroups.group_id=`groups`.id
            INNER JOIN teams ON teams.name=teamgroups.team_name 
            WHERE username=:username
            AND teams.name=:team_name
            AND groupmembers.deleted IS FALSE 
            AND `groups`.deleted IS FALSE 
            AND teamgroups.deleted IS FALSE 
            AND teams.deleted IS FALSE 
            """,
            {"username": username, "team_name": team_name},
            bind=engine,
        )
