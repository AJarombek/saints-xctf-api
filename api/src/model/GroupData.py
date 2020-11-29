"""
Group model that only includes data columns.
Author: Andrew Jarombek
Date: 11/9/2019
"""

from .Group import Group


class GroupData:
    def __init__(self, group: Group):
        """
        Create a group object without any auditing fields.
        :param group: The original Group object with auditing fields.
        """
        if group is not None:
            self.id = group.id
            self.group_name = group.group_name
            self.group_title = group.group_title
            self.grouppic = group.grouppic
            self.grouppic_name = group.grouppic_name
            self.week_start = group.week_start
            self.description = group.description
            self.deleted = group.deleted

    def __str__(self):
        """
        String representation of a group within a team.  This representation is meant to be human readable.
        :return: The group in string form.
        """
        return f'GroupData: [id: {self.id}, group_name: {self.group_name}, group_title: {self.group_title}, ' \
            f'grouppic: {self.grouppic}, grouppic_name: {self.grouppic_name}, week_start: {self.week_start}, ' \
            f'description: {self.description}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of a group within a team.  This representation is meant to be machine readable.
        :return: The group in string form.
        """
        return '<GroupData %r, %r>' % (self.id, self.group_name)

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this group.
        :return: True if the objects are equal, False otherwise.
        """
        return Group.compare(self, other)
