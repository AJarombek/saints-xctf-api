"""
TeamMember data access from the SaintsXCTF MySQL database.  Contains SQL queries related to users
who are members of a team.  Most team data is accessed from a separate TeamDao.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from typing import List, Tuple
from datetime import datetime

from sqlalchemy.engine import ResultProxy

from database import db
from dao.basicDao import BasicDao
from model.TeamMember import TeamMember


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

    @staticmethod
    def update_user_memberships(username: str, teams_joined: List[str], teams_left: List[str],
                                groups_joined: List[Tuple[str, str]], groups_left: List[Tuple[str, str]]):
        """
        Update the team and group memberships of a user.
        :param username: The username of the user who is updating their team memberships.
        :param teams_joined: A list of team names that the user is requesting to join.
        :param teams_left: A list of team names that the user is requesting to leave.
        :param groups_joined: A list tuples containing a team name and a group name.  Each tuple represents a group that
        the user is requesting to join.
        :param groups_left: A list tuples containing a team name and a group name.  Each tuple represents a group that
        the user is requesting to leave.
        """
        teams_joined_dict = [TeamMember({
            'team_name': team_name,
            'username': username,
            'status': 'pending',
            'user': 'user',
            'deleted': 'N',
            'created_date': datetime.now(),
            'created_user': username,
            'created_app': 'saints-xctf-api'
        }) for team_name in teams_joined]

        teams_left_dict = [{'username': username, 'team_name': team_name} for team_name in teams_left]

        if len(teams_joined_dict) > 0:
            for team_membership in teams_joined_dict:
                db.session.add(team_membership)

        if len(teams_left_dict) > 0:
            db.session.execute(
                '''
                UPDATE teammembers SET 
                    deleted = 'Y',
                    deleted_date=CURRENT_TIMESTAMP(),
                    deleted_user=:username,
                    deleted_app='saints-xctf-api'
                WHERE username=:username
                AND team_name=:team_name;
                ''',
                teams_left_dict
            )
        return BasicDao.safe_commit()
