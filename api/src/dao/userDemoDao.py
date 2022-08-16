"""
User data access from the SaintsXCTF demo SQLite database.  Contains SQL queries related to application users.
Author: Andrew Jarombek
Date: 8/15/2022
"""

from typing import List

from model.UserDemo import UserDemo


class UserDemoDao:

    @staticmethod
    def get_users() -> List[UserDemo]:
        """
        Get a list of all the users in the database.
        :return: A list containing User model objects.
        """
        return UserDemo.query.filter(UserDemo.deleted.is_(False)).all()
