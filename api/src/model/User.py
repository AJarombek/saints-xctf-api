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

    # Data Columns
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
    subscribed = Column(db.CHAR(1))
    last_signin = Column(db.DATETIME, nullable=False)
    week_start = Column(db.VARCHAR(15))
    deleted = Column(db.CHAR(1))

    # Audit Columns
    created_date = Column(db.DATETIME)
    created_user = Column(db.VARCHAR(31))
    created_app = Column(db.VARCHAR(31))
    modified_date = Column(db.DATETIME)
    modified_user = Column(db.VARCHAR(31))
    modified_app = Column(db.VARCHAR(31))
    deleted_date = Column(db.DATETIME)
    deleted_user = Column(db.VARCHAR(31))
    deleted_app = Column(db.VARCHAR(31))

    flair = db.relationship('Flair', backref='user_flair')
    notification = db.relationship('Notification', backref='notification')
    log = db.relationship('Log', backref='log')
    forgot_password = db.relationship('ForgotPassword', backref='forgot_password')
    message = db.relationship('Message', backref='message')
    comment = db.relationship('Comment', backref='comment')

    def __str__(self):
        """
        String representation of a user.  This representation is meant to be human readable.
        :return: The user in string form.
        """
        return f'User: [username: {self.username}, first: {self.first}, last: {self.last}, salt: {self.salt}, ' \
            f'password: {self.password}, profilepic: {self.profilepic}, profilepic_name: {self.profilepic_name}, ' \
            f'description: {self.description}, member_since: {self.member_since}, class_year: {self.class_year}, ' \
            f'location: {self.location}, favorite_event: {self.favorite_event}, ' \
            f'activation_code: {self.activation_code}, email: {self.email}, subscribed: {self.subscribed}, ' \
            f'last_signin: {self.last_signin}, week_start: {self.week_start}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of a user.  This representation is meant to be machine readable.
        :return: The user in string form.
        """
        return '<User %r>' % self.username

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this user.
        :return: True if the objects are equal, False otherwise.
        """
        return User.compare(self, other)

    @classmethod
    def compare(cls, user_1, user_2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be users.
        :param user_1: The first user object.
        :param user_2: The second user object.
        :return: True if the objects are equal, False otherwise.
        """
        if user_1.profilepic is None:
            self_profilepic = bytes()
        else:
            self_profilepic = user_1.grouppic
            try:
                self_profilepic = self_profilepic.decode('utf-8')
            except AttributeError:
                pass

        if user_2.profilepic is None:
            other_profilepic = bytes()
        else:
            other_profilepic = user_2.grouppic
            try:
                other_profilepic = other_profilepic.decode('utf-8')
            except AttributeError:
                pass

        return all([
            user_1.username == user_2.username,
            user_1.first == user_2.first,
            user_1.last == user_2.last,
            user_1.salt == user_2.salt,
            user_1.password == user_2.password,
            self_profilepic == other_profilepic,
            user_1.profilepic_name == user_2.profilepic_name,
            user_1.description == user_2.description,
            str(user_1.member_since) == str(user_2.member_since),
            user_1.class_year == user_2.class_year,
            user_1.location == user_2.location,
            user_1.favorite_event == user_2.favorite_event,
            user_1.activation_code == user_2.activation_code,
            user_1.email == user_2.email,
            user_1.subscribed == user_2.subscribed,
            user_1.last_signin == user_2.last_signin,
            user_1.week_start == user_2.week_start,
            user_1.deleted == user_2.deleted
        ])
