"""
WeekStart ORM model for the 'groupmembers' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.GroupMember import GroupMember


class GroupMemberDemo(GroupMember):
    __bind_key__ = 'demo'
