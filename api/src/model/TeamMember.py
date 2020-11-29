"""
TeamMember ORM model for the 'teammembers' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from app import db
from sqlalchemy import Column


class TeamMember(db.Model):

    def __init__(self, team: dict):
        """
        Initialize a TeamMember object by passing in a dictionary.
        :param team: A dictionary with fields matching the TeamMember fields
        """
        self.id = team.get('id')
        self.team_name = team.get('team_name')
        self.username = team.get('username')
        self.status = team.get('status')
        self.user = team.get('user')
        self.deleted = team.get('deleted')
        self.created_date = team.get('created_date')
        self.created_user = team.get('created_user')
        self.created_app = team.get('created_app')
        self.modified_date = team.get('modified_date')
        self.modified_user = team.get('modified_user')
        self.modified_app = team.get('modified_app')
        self.deleted_date = team.get('deleted_date')
        self.deleted_user = team.get('deleted_user')
        self.deleted_app = team.get('deleted_app')

    __tablename__ = 'teammembers'

    # Data Columns
    id = Column(db.INTEGER, primary_key=True)
    team_name = Column(db.VARCHAR(31), db.ForeignKey('teams.name'))
    username = Column(db.VARCHAR(20), db.ForeignKey('users.username'))
    status = Column(db.VARCHAR(10))
    user = Column(db.VARCHAR(10))
    deleted = Column(db.CHAR(1))

    # Audit Columns
    created_date = Column(db.DATETIME)
    created_user = Column(db.VARCHAR(31))
    created_app = Column(db.VARCHAR(31))
    modified_date = Column(db.DATETIME)
    modified_user = Column(db.VARCHAR(31))
    modified_app = Column(db.VARCHAR(31))
    deleted_date = Column(db.DATETIME)
    deleted_user = Column(db.VARCHAR(31))
    deleted_app = Column(db.VARCHAR(31))

    def __str__(self):
        """
        String representation of a team membership.  This representation is meant to be human readable.
        :return: The team membership in string form.
        """
        return f'TeamMember: [team_name: {self.team_name}, username: {self.username}, status: {self.status}, ' \
            f'user: {self.user}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of a team membership.  This representation is meant to be machine readable.
        :return: The team membership in string form.
        """
        return '<TeamMember %r, %r>' % (self.team_name, self.username)

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this team membership.
        :return: True if the objects are equal, False otherwise.
        """
        return TeamMember.compare(self, other)

    @classmethod
    def compare(cls, team_membership_1, team_membership_2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be team memberships.
        :param team_membership_1: The first team membership object.
        :param team_membership_2: The second team membership object.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            team_membership_1.team_name == team_membership_2.team_name,
            team_membership_1.username == team_membership_2.username,
            team_membership_1.status == team_membership_2.status,
            team_membership_1.user == team_membership_2.user,
            team_membership_1.deleted == team_membership_2.deleted
        ])
