"""
Log ORM model for the 'logs' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Log(db.Model):

    def __init__(self, log: dict):
        """
        Initialize a Log by passing in a dictionary.
        :param log: A dictionary with fields matching the Log fields
        """
        self.log_id = log.get('log_id')
        self.username = log.get('username')
        self.first = log.get('first')
        self.last = log.get('last')
        self.name = log.get('name')
        self.location = log.get('location')
        self.date = log.get('date')
        self.type = log.get('type')
        self.distance = log.get('distance')
        self.metric = log.get('metric')
        self.miles = log.get('miles')
        self.time = log.get('time')
        self.pace = log.get('pace')
        self.feel = log.get('feel')
        self.description = log.get('description')
        self.time_created = log.get('time_created')
        self.deleted = log.get('deleted')
        self.created_date = log.get('created_date')
        self.created_user = log.get('created_user')
        self.created_app = log.get('created_app')
        self.modified_date = log.get('modified_date')
        self.modified_user = log.get('modified_user')
        self.modified_app = log.get('modified_app')
        self.deleted_date = log.get('deleted_date')
        self.deleted_user = log.get('deleted_user')
        self.deleted_app = log.get('deleted_app')

    __tablename__ = 'logs'

    # Data Columns
    log_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), db.ForeignKey('users.username'), nullable=False, index=True)
    first = Column(db.VARCHAR(30), nullable=False)
    last = Column(db.VARCHAR(30), nullable=False)
    name = Column(db.VARCHAR(40))
    location = Column(db.VARCHAR(50))
    date = Column(db.DATE, nullable=False, index=True)
    type = Column(db.VARCHAR(40), db.ForeignKey('types.type'), nullable=False, index=True)
    distance = Column(db.FLOAT)
    metric = Column(db.VARCHAR(15), db.ForeignKey('metrics.metric'))
    miles = Column(db.FLOAT, index=True)
    time = Column(db.TIME, index=True)
    pace = Column(db.TIME)
    feel = Column(db.INT, nullable=False, index=True)
    description = Column(db.VARCHAR(1000))
    time_created = Column(db.DATETIME, nullable=False)
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

    comment = db.relationship('Comment', backref='log_comment')

    def __str__(self):
        """
        String representation of an exercise log.  This representation is meant to be human readable.
        :return: The exercise log in string form.
        """
        return f'Log: [log_id: {self.log_id}, username: {self.username}, first: {self.first}, last: {self.last}, ' \
            f'name: {self.name}, location: {self.location}, date: {self.date}, type: {self.type} ' \
            f'distance: {self.distance}, metric: {self.metric}, miles: {self.miles}, time: {self.time}, ' \
            f'pace: {self.pace}, feel: {self.feel}, description: {self.description}, ' \
            f'time_created: {self.time_created}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of an exercise log.  This representation is meant to be machine readable.
        :return: The exercise log in string form.
        """
        return '<Log %r>' % self.log_id

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this exercise log.
        :return: True if the objects are equal, False otherwise.
        """
        return Log.compare(self, other)

    @classmethod
    def compare(cls, log_1, log_2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be exercise logs.
        :param log_1: The first log object.
        :param log_2: The second log object.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            log_1.log_id == log_2.log_id,
            log_1.username == log_2.username,
            log_1.first == log_2.first,
            log_1.last == log_2.last,
            log_1.name == log_2.name,
            log_1.location == log_2.location,
            str(log_1.date) == str(log_2.date),
            log_1.type == log_2.type,
            log_1.distance == log_2.distance,
            log_1.metric == log_2.metric,
            log_1.miles == log_2.miles,
            str(log_1.time) == str(log_2.time),
            str(log_1.pace) == str(log_2.pace),
            log_1.feel == log_2.feel,
            log_1.description == log_2.description,
            log_1.deleted == log_2.deleted
        ])
