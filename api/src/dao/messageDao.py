"""
Message data access from the SaintsXCTF MySQL database.  Contains messages which are private to group members.
Author: Andrew Jarombek
Date: 7/18/2019
"""

from dao.basicDao import BasicDao
from database import db
from model.Message import Message


class MessageDao:

    @staticmethod
    def get_messages() -> list:
        pass
