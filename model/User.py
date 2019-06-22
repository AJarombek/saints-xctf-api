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
    first = Column(db.VARCHAR(30), nullable=False, index=True)
    last = Column(db.VARCHAR(30), nullable=False, index=True)
    salt = Column(db.VARCHAR(255))
    password = Column(db.VARCHAR(255), nullable=False)
    profilepic = Column(LONGBLOB)
    profilepic_name = Column(db.VARCHAR(50))
    description = Column(db.VARCHAR(255))
    member_since = Column(db.DATE, nullable=False)
    class_year = Column(db.INT(4), index=True)
    location = Column(db.VARCHAR(50))
    favorite_event = Column(db.VARCHAR(20))
    activation_code = Column(db.VARCHAR(8), nullable=False)
    email = Column(db.VARCHAR(50), index=True)
    subscribed = Column(TINYINT(1))
    last_signin = Column(db.DATETIME, nullable=False)
    week_start = Column(db.VARCHAR(15), db.ForeignKey('weekstart.week_start'))

    flair = db.relationship('Flair', backref='flair')
    notification = db.relationship('Notification', backref='notification')
    log = db.relationship('Log', backref='log')
    forgot_password = db.relationship('ForgotPassword', backref='forgot_password')
    message = db.relationship('Message', backref='message')
    comment = db.relationship('Comment', backref='comment')

    def __repr__(self):
        return '<User %r>' % self.username
