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
        self.group_id = group_member.get('group_id')
        self.username = group_member.get('username')
        self.status = group_member.get('status')
        self.user = group_member.get('user')
        self.deleted = group_member.get('deleted')
        self.created_date = group_member.get('created_date')
        self.created_user = group_member.get('created_user')
        self.created_app = group_member.get('created_app')
        self.modified_date = group_member.get('modified_date')
        self.modified_user = group_member.get('modified_user')
        self.modified_app = group_member.get('modified_app')
        self.deleted_date = group_member.get('deleted_date')
        self.deleted_user = group_member.get('deleted_user')
        self.deleted_app = group_member.get('deleted_app')

    __tablename__ = 'groupmembers'

    # Data Columns
    id = Column(db.INTEGER, primary_key=True)
    group_name = Column(db.VARCHAR(20), db.ForeignKey('groups.group_name'), index=True)
    group_id = Column(db.INTEGER, db.ForeignKey('groups.id'))
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
        return f'GroupMember: [id: {self.id}, group_name: {self.group_name}, group_id: {self.group_id}, ' \
            f'username: {self.username}, status: {self.status}, user: {self.user}, deleted: {self.deleted}]'

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
        return GroupMember.compare(self, other)

    @classmethod
    def compare(cls, group_member_1, group_member_2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be group members.
        :param group_member_1: The first group member object.
        :param group_member_2: The second group member object.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            group_member_1.group_name == group_member_2.group_name,
            group_member_1.group_id == group_member_2.group_id,
            group_member_1.username == group_member_2.username,
            group_member_1.status == group_member_2.status,
            group_member_1.user == group_member_2.user,
            group_member_1.deleted == group_member_2.deleted
        ])
