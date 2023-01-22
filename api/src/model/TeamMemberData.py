"""
TeamMember model that only includes data columns.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from .TeamMember import TeamMember


class TeamMemberData:
    def __init__(self, team_member: TeamMember):
        """
        Create a team membership object without any auditing fields.
        :param team_member: The original TeamMember object with auditing fields.
        """
        if team_member is not None:
            self.id = team_member.id
            self.team_name = team_member.team_name
            self.username = team_member.username
            self.status = team_member.status
            self.user = team_member.user
            self.deleted = team_member.deleted

    def __str__(self):
        """
        String representation of a team membership.  This representation is meant to be human-readable.
        :return: The team membership in string form.
        """
        return (
            f"TeamMemberData: [team_name: {self.team_name}, username: {self.username}, status: {self.status}, "
            f"user: {self.user}, deleted: {self.deleted}]"
        )

    def __repr__(self):
        """
        String representation of a team membership.  This representation is meant to be machine-readable.
        :return: The team membership in string form.
        """
        return f"<TeamMemberData {self.team_name}, {self.username}>"

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this team membership.
        :return: True if the objects are equal, False otherwise.
        """
        return TeamMember.compare(self, other)
