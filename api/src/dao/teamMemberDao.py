"""
TeamMember data access from the SaintsXCTF MySQL database.  Contains SQL queries related to users
who are members of a team.  Most team data is accessed from a separate TeamDao.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from sqlalchemy.engine import ResultProxy
from database import db


class TeamMemberDao:

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
            AND (teammembers.deleted IS NULL OR teammembers.deleted <> 'Y')
            AND (teams.deleted IS NULL OR teams.deleted <> 'Y')
            ''',
            {'username': username}
        )

    @staticmethod
    def get_team_members(team_name: str) -> ResultProxy:
        """
        Get the users who are members of a team.
        :param team_name: Unique name of a team.
        :return: A list of team members.
        """
        return db.session.execute(
            '''
            SELECT users.username,first,last,member_since,user,status,teammembers.deleted 
            FROM teammembers 
            INNER JOIN teams ON teams.name=teammembers.team_name 
            INNER JOIN users ON teammembers.username=users.username 
            WHERE teammembers.team_name=:team_name
            AND (teammembers.deleted IS NULL OR teammembers.deleted <> 'Y')
            AND (teams.deleted IS NULL OR teams.deleted <> 'Y')
            AND (users.deleted IS NULL OR users.deleted <> 'Y')
            ''',
            {'team_name': team_name}
        )