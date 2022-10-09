"""
Team data access from the SaintsXCTF MySQL database.  Contains SQL queries related to teams that users are members of.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from typing import List

from sqlalchemy import or_

from model.Team import Team
from model.TeamGroup import TeamGroup
from model.Group import Group


class TeamDao:
    @staticmethod
    def get_teams() -> List[Team]:
        """
        Get a list of all the teams in the database.
        :return: A list containing Team model objects.
        """
        return Team.query.filter(Team.deleted.is_(False)).all()

    @staticmethod
    def get_team_by_name(name: str) -> Team:
        """
        Get a single team from the database based on its name.
        :param name: Name which uniquely identifies a team.
        :return: The result of the database query.
        """
        return Team.query.filter_by(name=name).filter(Team.deleted.is_(False)).first()

    @staticmethod
    def get_team_by_group_id(group_id: int) -> Team:
        """
        Get a single team from the database based on a group id.  This group will be part of the team.
        :param group_id: Unique identifier for a group.
        :return: A Team object which is the result of the database query.
        """
        return (
            Team.query.filter(Team.name == TeamGroup.team_name)
            .filter(TeamGroup.group_id == Group.id)
            .filter(Group.id == group_id)
            .filter(Group.deleted.is_(False))
            .filter(TeamGroup.deleted.is_(False))
            .filter(Team.deleted.is_(False))
            .first()
        )

    @staticmethod
    def search_teams(text: str, limit: int) -> List[Team]:
        """
        Perform a text search for teams
        :param text: Text that can be a partial match for the team name or title.
        :param limit: The maximum number of teams to return.
        :return: The result of the database query.
        """
        return (
            Team.query.filter(
                or_(Team.name.like(f"%{text}%"), Team.title.like(f"%{text}%"))
            )
            .filter(Team.deleted.is_(False))
            .limit(limit)
            .all()
        )
