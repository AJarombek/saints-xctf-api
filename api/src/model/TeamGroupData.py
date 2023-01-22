"""
TeamGroup model that only includes data columns.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from .TeamGroup import TeamGroup


class TeamGroupData:
    def __init__(self, team_group: TeamGroup):
        """
        Create a team/group binding object without any auditing fields.
        :param team_group: The original TeamGroup object with auditing fields.
        """
        if team_group is not None:
            self.id = team_group.id
            self.team_name = team_group.team_name
            self.group_id = team_group.group_id
            self.group_name = team_group.group_name
            self.deleted = team_group.deleted

    def __str__(self):
        """
        String representation of a team and group binding.  This representation is meant to be human-readable.
        :return: The team/group binding in string form.
        """
        return (
            f"TeamGroupData: [team_name: {self.team_name}, group_id: {self.group_id}, "
            f"group_name: {self.group_name}, deleted: {self.deleted}]"
        )

    def __repr__(self):
        """
        String representation of a team/group binding.  This representation is meant to be machine-readable.
        :return: The team/group binding in string form.
        """
        return f"<TeamGroupData '{self.team_name}', '{self.group_name}'>"

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this team/group binding.
        :return: True if the objects are equal, False otherwise.
        """
        return TeamGroup.compare(self, other)
