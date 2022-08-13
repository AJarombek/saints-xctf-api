"""
WeekStart ORM model for the 'teamgroups' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.TeamGroup import TeamGroup


class TeamGroupDemo(TeamGroup):
    __bind_key__ = 'demo'
