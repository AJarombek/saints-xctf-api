"""
Team data access from the SaintsXCTF MySQL database.  Contains SQL queries related to teams that users are members of.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from typing import List

from model.Team import Team
from sqlalchemy import or_


class TeamDao:

    @staticmethod
    def get_teams() -> List[Team]:
        """
        Get a list of all the teams in the database.
        :return: A list containing Team model objects.
        """
        return Team.query\
            .filter(or_(Team.deleted.is_(None), Team.deleted.isnot('Y')))\
            .all()

    @staticmethod
    def get_team_by_name(name: str) -> Team:
        """
        Get a single team from the database based on its name.
        :param name: Name which uniquely identifies a team.
        :return: The result of the database query.
        """
        return Team.query\
            .filter_by(name=name)\
            .filter(or_(Team.deleted.is_(None), Team.deleted.isnot('Y')))\
            .first()

    @staticmethod
    def search_teams(text: str, limit: int) -> List[Team]:
        """
        Perform a text search for teams
        :param text: Text that can be a partial match for the team name or title.
        :param limit: The maximum number of teams to return.
        :return: The result of the database query.
        """
        return Team.query\
            .filter(Team.name.like(f'%{text}%'))\
            .filter(Team.title.like(f'%{text}%'))\
            .filter(or_(Team.deleted.is_(None), Team.deleted.isnot('Y')))\
            .limit(limit)\
            .all()
