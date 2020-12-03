"""
TeamGroup data access from the SaintsXCTF MySQL database.  Contains SQL queries related to groups
which are in a team.  Most team data is accessed from a separate TeamDao.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from sqlalchemy.engine import ResultProxy
from database import db


class TeamGroupDao:

    @staticmethod
    def get_team_groups(team_name: str) -> ResultProxy:
        """
        Get all the groups which are in a team
        :param team_name: Unique name for the team
        :return: A list of teams
        """
        print(team_name)
        return db.session.execute(
            '''
            SELECT id,`groups`.group_name,group_title,grouppic_name,description,week_start,`groups`.deleted
            FROM teamgroups 
            INNER JOIN `groups` ON teamgroups.group_name=`groups`.group_name 
            WHERE team_name=:team_name
            AND (teamgroups.deleted IS NULL OR teamgroups.deleted <> 'Y')
            AND (`groups`.deleted IS NULL OR `groups`.deleted <> 'Y')
            ''',
            {'team_name': team_name}
        )
