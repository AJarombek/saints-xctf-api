"""
WeekStart ORM model for the 'teammembers' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from sqlalchemy import Column

from app import db
from model.TeamMember import TeamMember


class TeamMemberDemo(TeamMember):
    __bind_key__ = "demo"

    # Data Columns
    id = Column(db.INTEGER, primary_key=True)
    team_name = Column(db.TEXT, db.ForeignKey("teams.name"))
    username = Column(db.TEXT, db.ForeignKey("users.username"))
    status = Column(db.TEXT)
    user = Column(db.TEXT)
    deleted = Column(db.INTEGER)

    # Audit Columns
    created_date = Column(db.NUMERIC)
    created_user = Column(db.TEXT)
    created_app = Column(db.TEXT)
    modified_date = Column(db.NUMERIC)
    modified_user = Column(db.TEXT)
    modified_app = Column(db.TEXT)
    deleted_date = Column(db.NUMERIC)
    deleted_user = Column(db.TEXT)
    deleted_app = Column(db.TEXT)
