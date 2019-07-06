"""
Flair data access from the SaintsXCTF MySQL database.  Contains flair displayed on users profiles.
Author: Andrew Jarombek
Date: 7/3/2019
"""

from database import db
from model.Flair import Flair
from dao.basicDao import BasicDao


class FlairDao:

    @staticmethod
    def get_flair_by_username(username: str) -> list:
        """
        Get the all the flairs bound to a user
        :param username: Unique identifier for the user
        :return: A list of strings representing flairs.
        """
        return Flair.query.filter_by(username=username).with_entities(Flair.flair).all()

    @staticmethod
    def get_flair_by_content(username: str, flair: str) -> dict:
        """
        Retrieve a Flair object based on its username and flair contents.
        :param username: Unique identifier for the user.
        :param flair: Content of the flair which is displayed on the users profile.
        :return: The result of the database query
        """
        return Flair.query.filter_by(username=username, flair=flair).first()

    @staticmethod
    def add_flair(flair: Flair) -> bool:
        """
        Add a flair item to the database.
        :param flair: Object representing a flair for a user in the application.
        :return: True if the flair is inserted into the database, False otherwise.
        """
        db.session.add(flair)
        return BasicDao.safe_commit()
