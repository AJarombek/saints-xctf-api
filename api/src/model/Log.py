"""
Log ORM model for the 'logs' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Log(db.Model):

    def __init__(self, user: dict):
        """
        Initialize a Log by passing in a dictionary.
        :param user: A dictionary with fields matching the Log fields
        """
        self.username = user.get('username')
        self.first = user.get('first')
        self.last = user.get('last')
        self.name = user.get('name')
        self.location = user.get('location')
        self.date = user.get('date')
        self.type = user.get('type')
        self.distance = user.get('distance')
        self.metric = user.get('metric')
        self.miles = user.get('miles')
        self.time = user.get('time')
        self.pace = user.get('pace')
        self.feel = user.get('feel')
        self.description = user.get('description')
        self.time_created = user.get('time_created')

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
    feel = Column(db.INT(2), nullable=False, index=True)
    description = Column(db.VARCHAR(1000))
    time_created = Column(db.DATETIME, nullable=False)

    comment = db.relationship('Comment', backref='comment')

    def __repr__(self):
        return '<Log %r>' % self.log_id
