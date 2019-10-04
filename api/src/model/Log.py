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

    __tablename__ = 'logs'

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

    comment = db.relationship('Comment', backref='comment')

    def __repr__(self):
        return '<Log %r>' % self.log_id
