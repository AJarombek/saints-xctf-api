"""
Group data access from the SaintsXCTF MySQL database.  Contains SQL queries related to group information.
Most membership data is accessed from a separate GroupMemberDao.
Author: Andrew Jarombek
Date: 7/2/2019
"""

from database import db
from dao.basicDao import BasicDao
from model.Group import Group


class GroupDao:

    @staticmethod
    def get_user_groups():
        pass
