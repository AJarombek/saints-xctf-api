"""
WeekStart ORM model for the 'teammembers' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.TeamMember import TeamMember


class TeamMemberDemo(TeamMember):
    __bind_key__ = 'demo'
