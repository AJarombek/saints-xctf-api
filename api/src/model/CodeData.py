"""
Comment model that only includes data columns.
Author: Andrew Jarombek
Date: 10/8/2019
"""

from . import Code


class CodeData:
    def __init__(self, code: Code):
        """
        Create an activation code object without any auditing fields.
        :param code: A dictionary with fields matching the Code fields
        """
        self.activation_code = code.activation_code
        self.deleted = code.deleted
