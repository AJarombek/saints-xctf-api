"""
User data access from the SaintsXCTF MySQL database.  Contains SQL queries related to application users.
Author: Andrew Jarombek
Date: 6/16/2019
"""

from typing import List

from sqlalchemy.orm import defer

from app import app
from database import db
from dao.basicDao import BasicDao
from model.User import User


class UserDao:
    engine = db.get_engine(app=app, bind="app")

    @staticmethod
    def get_users() -> List[User]:
        """
        Get a list of all the users in the database.
        :return: A list containing User model objects.
        """
        return User.query.filter(User.deleted.is_(False)).all()

    @staticmethod
    def get_user_by_username(username: str) -> User:
        """
        Get a single user from the database based on their username.
        :param username: Username which uniquely identifies the user.
        :return: The result of the database query.
        """
        return (
            User.query.filter_by(username=username)
            .filter(User.deleted.is_(False))
            .options(defer("profilepic"), defer("profilepic_name"))
            .first()
        )

    @staticmethod
    def get_user_by_email(email: str) -> User:
        """
        Get a single user from the database based on their email.
        :param email: Email which uniquely identifies the user.
        :return: The result of the database query.
        """
        return (
            User.query.filter_by(email=email)
            .filter(User.deleted.is_(False))
            .options(defer("profilepic"), defer("profilepic_name"))
            .first()
        )

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
    def update_user(username: str, user: User) -> bool:
        """
        Update a user in the database.  This function does NOT update passwords.
        :param username: Username which uniquely identifies the user.
        :param user: Object representing an updated user for the application.
        :return: True if the user is updated in the database, False otherwise.
        """
        db.session.execute(
            """
            UPDATE users SET 
                first=:first, 
                last=:last, 
                email=:email,
                profilepic_name=:profilepic_name, 
                description=:description,
                class_year=:class_year, 
                location=:location, 
                favorite_event=:favorite_event, 
                week_start=:week_start 
            WHERE username=:username
            AND deleted IS FALSE
            """,
            {
                "first": user.first,
                "last": user.last,
                "email": user.email,
                "profilepic_name": user.profilepic_name,
                "description": user.description,
                "class_year": user.class_year,
                "location": user.location,
                "favorite_event": user.favorite_event,
                "week_start": user.week_start,
                "username": username,
            },
            bind=UserDao.engine,
        )
        return BasicDao.safe_commit()

    @staticmethod
    def update_user_password(username: str, password: str) -> bool:
        """
        Update the password of a user.  This operation can't be done using the update_user() function.
        :param username: Username which uniquely identifies the user.
        :param password: New password for a user.
        :return: True if the update was successful, False otherwise
        """
        db.session.execute(
            """
            UPDATE users 
            SET password=:password 
            WHERE username=:username 
            AND deleted IS FALSE
            """,
            {"username": username, "password": password},
            bind=UserDao.engine,
        )
        return BasicDao.safe_commit()

    @staticmethod
    def update_user_last_login(username: str) -> bool:
        """
        Update the date of the previous login for a user.
        :param username: Username which uniquely identifies the user.
        :return: True if the update was successful, False otherwise
        """
        db.session.execute(
            """
            UPDATE users 
            SET last_signin=SYSDATE() 
            WHERE username=:username
            AND deleted IS FALSE
            """,
            {"username": username},
            bind=UserDao.engine,
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_user(username: str) -> bool:
        """
        Delete a user from the database based on its username.
        :param username: Username which uniquely identifies the user.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            "DELETE FROM teammembers WHERE username=:username",
            {"username": username},
            bind=UserDao.engine,
        )
        db.session.execute(
            "DELETE FROM users WHERE username=:username",
            {"username": username},
            bind=UserDao.engine,
        )
        return BasicDao.safe_commit()

    @staticmethod
    def soft_delete_user(user: User) -> bool:
        """
        Soft Delete a user from the database.
        :param user: Object representing a user to soft delete.
        :return: True if the soft deletion was successful without error, False otherwise.
        """
        db.session.execute(
            """
            UPDATE users SET 
                deleted=:deleted,
                modified_date=:modified_date,
                modified_app=:modified_app,
                deleted_date=:deleted_date,
                deleted_app=:deleted_app
            WHERE username=:username
            AND deleted IS FALSE
            """,
            {
                "username": user.username,
                "deleted": user.deleted,
                "modified_date": user.modified_date,
                "modified_app": user.modified_app,
                "deleted_date": user.deleted_date,
                "deleted_app": user.deleted_app,
            },
            bind=UserDao.engine,
        )
        return BasicDao.safe_commit()
