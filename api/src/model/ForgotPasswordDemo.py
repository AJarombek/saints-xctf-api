"""
WeekStart ORM model for the 'forgotpassword' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from sqlalchemy import Column

from app import db
from model.ForgotPassword import ForgotPassword


class ForgotPasswordDemo(ForgotPassword):
    __bind_key__ = 'demo'

    # Data Columns
    forgot_code = Column(db.TEXT, primary_key=True)
    username = Column(db.TEXT, db.ForeignKey('users.username'), nullable=False)
    expires = Column(db.NUMERIC, nullable=False)
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
