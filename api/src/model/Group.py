"""
Group ORM model for the 'groups' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import LONGBLOB


class Group(db.Model):

    def __init__(self, group: dict):
        """
        Initialize a Group object by passing in a dictionary.
        :param group: A dictionary with fields matching the Group fields
        """
        self.group_name = group.get('group_name')
        self.group_title = group.get('group_title')
        self.grouppic = group.get('grouppic')
        self.grouppic_name = group.get('grouppic_name')
        self.week_start = group.get('week_start')
        self.description = group.get('description')
        self.deleted = group.get('deleted')

    __tablename__ = 'groups'

    # Data Columns
    group_name = Column(db.VARCHAR(20), primary_key=True)
    group_title = Column(db.VARCHAR(50), index=True)
    grouppic = Column(LONGBLOB)
    grouppic_name = Column(db.VARCHAR(50))
    week_start = Column(db.VARCHAR(15), db.ForeignKey('weekstart.week_start'))
    description = Column(db.VARCHAR(255))
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

    message = db.relationship('Message', backref='group_message')

    def __str__(self):
        """
        String representation of a group within a team.  This representation is meant to be human readable.
        :return: The forgot password code in string form.
        """
        return f'Group: [group_name: {self.group_name}, group_title: {self.group_title}, ' \
            f'grouppic: {self.grouppic}, grouppic_name: {self.grouppic_name}, week_start: {self.week_start}, ' \
            f'description: {self.description}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of a group within a team.  This representation is meant to be machine readable.
        :return: The group in string form.
        """
        return '<Group %r>' % self.group_name

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this group.
        :return: True if the objects are equal, False otherwise.
        """
        if self.grouppic is None:
            self_grouppic = bytes()
        else:
            self_grouppic = self.grouppic
            try:
                self_grouppic = self_grouppic.decode('utf-8')
            except AttributeError:
                pass

        if other.grouppic is None:
            other_grouppic = bytes()
        else:
            other_grouppic = other.grouppic
            try:
                other_grouppic = other_grouppic.decode('utf-8')
            except AttributeError:
                pass

        return all([
            self.group_name == other.group_name,
            self.group_title == other.group_title,
            self_grouppic == other_grouppic,
            self.grouppic_name == other.grouppic_name,
            self.week_start == other.week_start,
            self.description == other.description,
            self.deleted == other.deleted
        ])
