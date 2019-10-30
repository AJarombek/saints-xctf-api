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
        self.flair_id = flair.flair_id
        self.username = flair.username
        self.flair = flair.flair
