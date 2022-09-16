"""
TeamMember data access from the SaintsXCTF demo database.  Contains SQL queries related to users
who are members of a team.  Most team data is accessed from a separate TeamDemoDao.
Author: Andrew Jarombek
Date: 9/15/2022
"""

from sqlalchemy.engine.cursor import ResultProxy

from app import app
from database import db


class TeamMemberDemoDao:
    engine = db.get_engine(app=app, bind='demo')

    @staticmethod
    def get_user_teams(username: str) -> ResultProxy:
        """
        Get information about all the teams a user is a member of
        :param username: Unique identifier for the user
        :return: A list of teams
        """
        return db.session.execute(
            '''
            SELECT team_name,title,status,user 
            FROM teammembers 
            INNER JOIN teams ON teams.name=teammembers.team_name 
            WHERE username=:username
            AND teammembers.deleted IS FALSE
            AND teams.deleted IS FALSE
            ''',
            {'username': username},
            bind=TeamMemberDemoDao.engine
        )
