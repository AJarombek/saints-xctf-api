"""
WeekStart ORM model for the 'codes' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Code import Code


class CodeDemo(Code):
    __bind_key__ = 'demo'
