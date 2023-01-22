"""
User model that only includes data columns.
Author: Andrew Jarombek
Date: 12/9/2019
"""

from .User import User


class UserData:
    def __init__(self, user: User, defer_profile_picture: bool = True):
        """
        Create a user object without any auditing fields.
        :param user: The original User object with auditing fields.
        """
        if user is not None:
            self.username = user.username
            self.first = user.first
            self.last = user.last
            self.salt = user.salt
            self.password = user.password
            self.profilepic_name = user.profilepic_name
            self.description = user.description
            self.member_since = user.member_since
            self.class_year = user.class_year
            self.location = user.location
            self.favorite_event = user.favorite_event
            self.activation_code = user.activation_code
            self.email = user.email
            self.subscribed = user.subscribed
            self.last_signin = user.last_signin
            self.week_start = user.week_start
            self.deleted = user.deleted

        if not defer_profile_picture:
            self.profilepic = user.profilepic
            self.profilepic_name = user.profilepic_name

    def __str__(self):
        """
        String representation of a user.  This representation is meant to be human-readable.
        :return: The user in string form.
        """
        return (
            f"UserData: [username: {self.username}, first: {self.first}, last: {self.last}, salt: {self.salt}, "
            f"password: {self.password}, profilepic_name: {self.profilepic_name}, description: {self.description}, "
            f"member_since: {self.member_since}, class_year: {self.class_year}, location: {self.location}, "
            f"favorite_event: {self.favorite_event}, activation_code: {self.activation_code}, email: {self.email}, "
            f"subscribed: {self.subscribed}, last_signin: {self.last_signin}, week_start: {self.week_start}, "
            f"deleted: {self.deleted}]"
        )

    def __repr__(self):
        """
        String representation of a user.  This representation is meant to be machine-readable.
        :return: The user in string form.
        """
        return f"<UserData {self.username}>"

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this user.
        :return: True if the objects are equal, False otherwise.
        """
        return User.compare(self, other)
