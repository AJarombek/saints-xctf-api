"""
User data access from the SaintsXCTF MySQL database.  Contains SQL queries related to application users.
Author: Andrew Jarombek
Date: 6/16/2019
"""

from app import get_db
from pymysql import Error


class UserDao:

    def __init__(self):
        """
        Initialize the UserDao object by defining a MySQL database connection object
        """
        self.connection = get_db()

    def get_user_by_username(self, username: str):
        """
        Get a single user from the database based on their username.
        :param username: Username which uniquely identifies the user.
        :return: The result of the database query.
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username=%s"
                cursor.execute(sql, args=[username])
                result = cursor.fetchone()
                print(result)
                return result
        except Error as e:
            print(e)

    def get_user_by_email(self, email: str):
        """
        Get a single user from the database based on their email.
        :param email: Email which uniquely identifies the user.
        :return: The result of the database query.
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE email=%s"
                cursor.execute(sql, args=[email])
                result = cursor.fetchone()
                print(result)
                return result
        except Error as e:
            print(e)