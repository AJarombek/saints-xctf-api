"""
Team data access from the SaintsXCTF demo SQLite database.  Contains SQL queries related to teams
that users are members of.
Author: Andrew Jarombek
Date: 8/27/2022
"""

from typing import List

from sqlalchemy import or_

from model.TeamDemo import TeamDemo


class TeamDemoDao:

    @staticmethod
    def get_teams() -> List[TeamDemo]:
        """
        Get a list of all the teams in the database.
        :return: A list containing Team model objects.
        """
        return TeamDemo.query \
            .filter(TeamDemo.deleted.is_(False)) \
            .all()

    @staticmethod
    def get_team_by_name(name: str) -> TeamDemo:
        """
        Get a single team from the database based on its name.
        :param name: Name which uniquely identifies a team.
        :return: The result of the database query.
        """
        return TeamDemo.query \
            .filter_by(name=name) \
            .filter(TeamDemo.deleted.is_(False)) \
            .first()

    @staticmethod
    def search_teams(text: str, limit: int) -> List[TeamDemo]:
        """
        Perform a text search for teams
        :param text: Text that can be a partial match for the team name or title.
        :param limit: The maximum number of teams to return.
        :return: The result of the database query.
        """
        return TeamDemo.query \
            .filter(or_(TeamDemo.name.like(f'%{text}%'), TeamDemo.title.like(f'%{text}%'))) \
            .filter(TeamDemo.deleted.is_(False)) \
            .limit(limit) \
            .all()
