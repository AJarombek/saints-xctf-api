"""
Exercise type data access from the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 12/8/2022
"""

from typing import List

from model.Type import Type


class TypeDao:
    @staticmethod
    def get_types() -> List[Type]:
        """
        Get a list of all the exercise types in the database.
        :return: A list containing Type model objects.
        """
        return Type.query.all()
