"""
WeekStart ORM model for the 'logs' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from sqlalchemy import Column

from app import db
from model.Log import Log


class LogDemo(Log):
    __bind_key__ = "demo"

    # Data Columns
    log_id = Column(db.INTEGER, autoincrement=True, primary_key=True)
    username = Column(db.TEXT, db.ForeignKey("users.username"), nullable=False)
    first = Column(db.TEXT, nullable=False)
    last = Column(db.TEXT, nullable=False)
    name = Column(db.TEXT)
    location = Column(db.TEXT)
    date = Column(db.NUMERIC, nullable=False)
    type = Column(db.TEXT, db.ForeignKey("types.type"), nullable=False)
    distance = Column(db.NUMERIC)
    metric = Column(db.TEXT, db.ForeignKey("metrics.metric"))
    miles = Column(db.NUMERIC)
    time = Column(db.NUMERIC)
    pace = Column(db.NUMERIC)
    feel = Column(db.INTEGER, nullable=False)
    description = Column(db.TEXT)
    time_created = Column(db.NUMERIC, nullable=False)
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
