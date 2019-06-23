"""
User data access from the SaintsXCTF MySQL database.  Contains SQL queries related to application users.
Author: Andrew Jarombek
Date: 6/16/2019
"""

from app import db, app
from dao.basicDao import BasicDao
from model.User import User
from model.Code import Code


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
        activation_code_count = Code.query.filter_by(activation_code=user.activation_code).count()
        if activation_code_count == 1:
            db.session.add(user)
            return BasicDao.safe_commit()
        else:
            app.logger.error('Failed to create new User: The Activation Code does not exist.')
            return False
