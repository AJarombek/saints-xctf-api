"""
WeekStart ORM model for the 'groups' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from sqlalchemy import Column

from app import db
from model.Group import Group


class GroupDemo(Group):
    __bind_key__ = 'demo'

    # Data Columns
    id = Column(db.INTEGER, autoincrement=True, primary_key=True)
    group_name = Column(db.TEXT)
    group_title = Column(db.TEXT)
    grouppic = Column(db.BLOB)
    grouppic_name = Column(db.TEXT)
    week_start = Column(db.TEXT, db.ForeignKey('weekstart.week_start'))
    description = Column(db.TEXT)
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
