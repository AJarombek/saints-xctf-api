"""
Flair data access from the SaintsXCTF MySQL database.  Contains flair displayed on users profiles.
Author: Andrew Jarombek
Date: 7/3/2019
"""

from database import db
from model.Flair import Flair


class FlairDao:

    @staticmethod
    def get_flair_by_username(username: str) -> list:
        """
        Get the all the flairs bound to a user
        :param username: Unique identifier for the user
        :return: A list of strings representing flairs.
        """
        return Flair.query.filter_by(username=username).with_entities(Flair.flair).all()
