"""
User ORM model for the 'users' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/21/2019
"""

from database import db
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, LONGBLOB


class User(db.Model):

    def __init__(self, user: dict):
        """
        Initialize a User by passing in a dictionary.
        :param user: A dictionary with fields matching the User fields
        """
        # get() returns None by default
        self.username = user.get('username')
        self.first = user.get('first')
        self.last = user.get('last')
        self.salt = user.get('salt')
        self.password = user.get('password')
        self.profilepic = user.get('profilepic')
        self.profilepic_name = user.get('profilepic_name')
        self.description = user.get('description')
        self.member_since = user.get('member_since')
        self.class_year = user.get('class_year')
        self.location = user.get('location')
        self.favorite_event = user.get('favorite_event')
        self.activation_code = user.get('activation_code')
        self.email = user.get('email')
        self.subscribed = user.get('subscribed')
        self.last_signin = user.get('last_signin')
        self.week_start = user.get('week_start', 'monday')

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
    class_year = Column(db.INTEGER, index=True)
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
