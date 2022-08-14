"""
WeekStart ORM model for the 'codes' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from app import db
from model.Code import Code
from sqlalchemy import Column


class CodeDemo(Code):
    __bind_key__ = 'demo'

    # Data Columns
    activation_code = Column(db.TEXT, primary_key=True, nullable=False)
    email = Column(db.TEXT)
    group_id = Column(db.INTEGER, db.ForeignKey('groups.id'))
    expiration_date = Column(db.NUMERIC)
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
