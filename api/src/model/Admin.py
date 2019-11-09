"""
Admin ORM model for the 'admins' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Admin(db.Model):
    __tablename__ = 'admins'

    user = Column(db.VARCHAR(10), primary_key=True)

    group_members = db.relationship('GroupMember', backref='group_member')

    def __str__(self):
        """
        String representation of a type of group member.  This representation is meant to be human readable.
        :return: Either a 'user' or 'admin' type of group member.
        """
        return f'Admin: [user: {self.user}]'

    def __repr__(self):
        """
        String representation of a type of group member.  This representation is meant to be machine readable.
        :return: Either a 'user' or 'admin' type of group member.
        """
        return '<Admin %r>' % self.user

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this object.
        :return: True if the objects are equal, False otherwise.
        """
        return self.user == other.user
