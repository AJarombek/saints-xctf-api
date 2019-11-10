"""
Group Member model that only includes data columns.
Author: Andrew Jarombek
Date: 11/9/2019
"""

from .GroupMember import GroupMember


class GroupMemberData:
    def __init__(self, group_member: GroupMember):
        """
        Create a group member object without any auditing fields.
        :param group_member: The original GroupMember object with auditing fields.
        """
        if group_member is not None:
            self.id = group_member.id
            self.group_name = group_member.group_name
            self.username = group_member.username
            self.status = group_member.status
            self.user = group_member.user
            self.deleted = group_member.deleted

    def __str__(self):
        """
        String representation of information about a user who is a member of a group.  This representation is meant
        to be human readable.
        :return: The group member in string form.
        """
        return f'GroupMemberData: [id: {self.id}, group_name: {self.group_name}, username: {self.username}, ' \
            f'status: {self.status}, user: {self.user}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of information about a user who is a member of a group.  This representation is meant
        to be machine readable.
        :return: The group member in string form.
        """
        return '<GroupMemberData %r,%r>' % (self.group_name, self.username)

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
