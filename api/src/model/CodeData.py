"""
Comment model that only includes data columns.
Author: Andrew Jarombek
Date: 10/8/2019
"""

from . import Code


class CodeData:
    def __init__(self, code: Code):
        """
        Create an activation code object without any auditing fields.
        :param code: The original Code object with auditing fields.
        """
        self.activation_code = code.activation_code
        self.deleted = code.deleted

    def __str__(self):
        """
        String representation of an activation code.  This representation is meant to be human readable.
        :return: The activation code string.
        """
        return f'Code: [activation_code: {self.activation_code}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of an activation code.  This representation is meant to be machine readable.
        :return: The activation code string.
        """
        return '<Code %r>' % self.activation_code

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this Code.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            self.activation_code == other.activation_code,
            self.deleted == other.deleted
        ])
