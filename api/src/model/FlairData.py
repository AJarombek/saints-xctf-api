"""
Flair model that only includes data columns.
Author: Andrew Jarombek
Date: 10/26/2019
"""

from .Flair import Flair


class FlairData:
    def __init__(self, flair: Flair):
        """
        Create a flair object without any auditing fields.
        :param flair: The original Flair object with auditing fields.
        """
        if flair is not None:
            self.flair_id = flair.flair_id
            self.username = flair.username
            self.flair = flair.flair
            self.deleted = flair.deleted

    def __str__(self):
        """
        String representation of the user's flair.  This representation is meant to be human readable.
        :return: The flair in string form.
        """
        return f'FlairData: [flair_id: {self.flair_id}, username: {self.username}, flair: {self.flair}, ' \
            f'deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of the user's flair.  This representation is meant to be machine readable.
        :return: The flair in string form.
        """
        return '<FlairData %r,%r>' % (self.flair_id, self.username)

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this Flair.
        :return: True if the objects are equal, False otherwise.
        """
        return Flair.compare(self, other)
