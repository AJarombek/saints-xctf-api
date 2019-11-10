"""
GroupMember ORM model for the 'groupmembers' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class GroupMember(db.Model):

    def __init__(self, group_member: dict):
        """
        Initialize a GroupMember object by passing in a dictionary.
        :param group_member: A dictionary with fields matching the GroupMember fields
        """
        self.id = group_member.get('id')
        self.group_name = group_member.get('group_name')
        self.username = group_member.get('username')
        self.status = group_member.get('status')
        self.user = group_member.get('user')
        self.deleted = group_member.get('deleted')

    __tablename__ = 'groupmembers'

    # Data Columns
    id = Column(db.INTEGER, primary_key=True)
    group_name = Column(db.VARCHAR(20), db.ForeignKey('groups.group_name'), index=True)
    username = Column(db.VARCHAR(20), index=True)
    status = Column(db.VARCHAR(10), db.ForeignKey('status.status'))
    user = Column(db.VARCHAR(10), db.ForeignKey('admins.user'))
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
        String representation of information about a user who is a member of a group.  This representation is meant
        to be human readable.
        :return: The group member in string form.
        """
        return f'Group: [id: {self.id}, group_name: {self.group_name}, username: {self.username}, ' \
            f'status: {self.status}, user: {self.user}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of information about a user who is a member of a group.  This representation is meant
        to be machine readable.
        :return: The group member in string form.
        """
        return '<GroupMember %r,%r>' % (self.group_name, self.username)

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this group member.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            self.id == other.id,
            self.group_name == other.group_name,
            self.username == other.username,
            self.status == other.status,
            self.user == other.user,
            self.deleted == other.deleted
        ])
