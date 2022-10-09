"""
Flair data access from the SaintsXCTF demo database.  Contains flair displayed on users profiles.
Author: Andrew Jarombek
Date: 9/13/2022
"""

from typing import List

from model.FlairDemo import FlairDemo


class FlairDemoDao:
    @staticmethod
    def get_flair_by_username(username: str) -> List[FlairDemo]:
        """
        Get the all the flairs bound to a user
        :param username: Unique identifier for the user
        :return: A list of strings representing flairs.
        """
        return (
            FlairDemo.query.filter_by(username=username)
            .filter(FlairDemo.deleted.is_(False))
            .all()
        )
