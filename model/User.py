"""
User ORM model for the 'users' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/21/2019
"""

from app import db
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, LONGBLOB


class User(db.Model):
    __tablename__ = 'users'

    username = Column(db.VARCHAR(20), primary_key=True)
    first = Column(db.VARCHAR(30), nullable=False)
    last = Column(db.VARCHAR(30), nullable=False)
    salt = Column(db.VARCHAR(255))
    password = Column(db.VARCHAR(255), nullable=False)
    profilepic = Column(LONGBLOB)
    profilepic_name = Column(db.VARCHAR(50))
    description = Column(db.VARCHAR(255))
    member_since = Column(db.DATE, nullable=False)
    class_year = Column(db.INT(4))
    location = Column(db.VARCHAR(50))
    favorite_event = Column(db.VARCHAR(20))
    activation_code = Column(db.VARCHAR(8), nullable=False)
    email = Column(db.VARCHAR(50))
    subscribed = Column(TINYINT(1))
    last_signin = Column(db.DATETIME, nullable=False)
    week_start = Column(db.VARCHAR(15))

    def __repr__(self):
        return '<User %r>' % self.username
