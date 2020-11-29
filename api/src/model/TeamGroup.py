"""
TeamGroup ORM model for the 'teamgroups' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from app import db
from sqlalchemy import Column


class TeamGroup(db.Model):

    def __init__(self, team: dict):
        """
        Initialize a TeamGroup object by passing in a dictionary.
        :param team: A dictionary with fields matching the TeamGroup fields
        """
        self.team_name = team.get('team_name')
        self.group_id = team.get('group_id')
        self.group_name = team.get('group_name')
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

    __tablename__ = 'teamgroups'

    # Data Columns
    team_name = Column(db.VARCHAR(31), db.ForeignKey('teams.name'))
    group_id = Column(db.INTEGER, db.ForeignKey('groups.id'))
    group_name = Column(db.INTEGER, db.ForeignKey('groups.name'))
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
        String representation of a team and group binding.  This representation is meant to be human readable.
        :return: The team/group binding in string form.
        """
        return f'TeamGroup: [team_name: {self.team_name}, group_id: {self.group_id}, group_name: {self.group_name}, ' \
            f'deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of a team and group binding.  This representation is meant to be machine readable.
        :return: The team/group binding in string form.
        """
        return '<TeamGroup %r, %r>' % self.team_name, self.group_name

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this team/group binding.
        :return: True if the objects are equal, False otherwise.
        """
        return TeamGroup.compare(self, other)

    @classmethod
    def compare(cls, team_group_1, team_group_2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be team/group bindings.
        :param team_group_1: The first team/group binding object.
        :param team_group_2: The second team/group binding object.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            team_group_1.team_name == team_group_2.team_name,
            team_group_1.group_id == team_group_2.group_id,
            team_group_1.group_name == team_group_2.group_name,
            team_group_1.deleted == team_group_2.deleted
        ])
