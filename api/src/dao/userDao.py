"""
User data access from the SaintsXCTF MySQL database.  Contains SQL queries related to application users.
Author: Andrew Jarombek
Date: 6/16/2019
"""

from database import db
from dao.basicDao import BasicDao
from model.User import User


class UserDao:

    @staticmethod
    def get_users() -> list:
        """
        Get a list of all the users in the database.
        :return: A list containing User model objects.
        """
        return User.query.all()

    @staticmethod
    def get_user_by_username(username: str) -> User:
        """
        Get a single user from the database based on their username.
        :param username: Username which uniquely identifies the user.
        :return: The result of the database query.
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email: str) -> User:
        """
        Get a single user from the database based on their email.
        :param email: Email which uniquely identifies the user.
        :return: The result of the database query.
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def add_user(user: User) -> bool:
        """
        Add a user if it has a valid activation code.
        :param user: Object representing a user for the application.
        :return: True if the user is inserted into the database, False otherwise.
        """
        db.session.add(user)
        return BasicDao.safe_commit()


    @staticmethod
    def update_user(user: User) -> bool:
        pass
