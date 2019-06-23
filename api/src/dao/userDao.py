"""
User data access from the SaintsXCTF MySQL database.  Contains SQL queries related to application users.
Author: Andrew Jarombek
Date: 6/16/2019
"""

from app import db, app
from dao.basicDao import BasicDao
from dao.codeDao import CodeDao
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
        """
        Add a user if it has a valid activation code.
        :param user: Object representing a user for the application.
        :return: True if the user is inserted into the database, False otherwise.
        """
        activation_code_count = CodeDao.get_code_count(activation_code=user.activation_code)
        if activation_code_count == 1:
            # First add the user since its activation code is valid
            db.session.add(user)
            result = BasicDao.safe_commit()

            if not result:
                return False

            # Second remove the activation code so it cant be used again
            code = Code(activation_code=user.activation_code)
            return CodeDao.remove_code(code)
        else:
            app.logger.error('Failed to create new User: The Activation Code does not exist.')
            return False

    @staticmethod
    def update_user(user: User) -> bool:
        pass
