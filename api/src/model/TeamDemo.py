"""
WeekStart ORM model for the 'teams' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Team import Team


class TeamDemo(Team):
    __bind_key__ = 'demo'
