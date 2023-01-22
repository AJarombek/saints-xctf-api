"""
Team model that only includes data columns.
Author: Andrew Jarombek
Date: 11/28/2020
"""

from .Team import Team


class TeamData:
    def __init__(self, team: Team):
        """
        Create a team object without any auditing fields.
        :param team: The original Team object with auditing fields.
        """
        if team is not None:
            self.name = team.name
            self.title = team.title
            self.picture_name = team.picture_name
            self.week_start = team.week_start
            self.description = team.description
            self.deleted = team.deleted

    def __str__(self):
        """
        String representation of a team.  This representation is meant to be human-readable.
        :return: The team in string form.
        """
        return (
            f"TeamData: [name: {self.name}, title: {self.title}, picture_name: {self.picture_name}, "
            f"week_start: {self.week_start}, description: {self.description}, deleted: {self.deleted}]"
        )

    def __repr__(self):
        """
        String representation of a team.  This representation is meant to be machine-readable.
        :return: The team in string form.
        """
        return f"<TeamData '{self.name}'>"

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this team.
        :return: True if the objects are equal, False otherwise.
        """
        return Team.compare(self, other)
