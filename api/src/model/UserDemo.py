"""
WeekStart ORM model for the 'users' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from sqlalchemy import Column

from app import db
from model.User import User


class UserDemo(User):
    __bind_key__ = "demo"

    # Data Columns
    username = Column(db.TEXT, primary_key=True)
    first = Column(db.TEXT, nullable=False)
    last = Column(db.TEXT, nullable=False)
    salt = Column(db.TEXT)
    password = Column(db.TEXT, nullable=False)
    profilepic = Column(db.BLOB)
    profilepic_name = Column(db.TEXT)
    description = Column(db.TEXT)
    member_since = Column(db.NUMERIC, nullable=False)
    class_year = Column(db.INTEGER)
    location = Column(db.TEXT)
    favorite_event = Column(db.TEXT)
    activation_code = Column(db.TEXT, nullable=False)
    email = Column(db.TEXT)
    subscribed = Column(db.TEXT)
    last_signin = Column(db.NUMERIC, nullable=False)
    week_start = Column(db.TEXT)
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
