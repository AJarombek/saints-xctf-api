"""
Common Flair data access functions.  Contains flair displayed on users profiles.
Author: Andrew Jarombek
Date: 11/5/2022
"""

from typing import List, Union

from model.Flair import Flair
from model.FlairDemo import FlairDemo


class FlairDemoDao:
    flair_model = Flair

    def get_flair_by_username(self, username: str) -> List[Union[Flair, FlairDemo]]:
        """
        Get the all the flairs bound to a user
        :param username: Unique identifier for the user
        :return: A list of strings representing flairs.
        """
        return (
            self.flair_model.query.filter_by(username=username)
            .filter(self.flair_model.deleted.is_(False))
            .all()
        )
