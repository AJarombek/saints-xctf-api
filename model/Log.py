"""
Log ORM model for the 'logs' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Log(db.Model):
    __tablename__ = 'logs'

    log_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), nullable=False)
    first = Column(db.VARCHAR(30), nullable=False)
    last = Column(db.VARCHAR(30), nullable=False)
    name = Column(db.VARCHAR(40))
    location = Column(db.VARCHAR(50))
    date = Column(db.DATE, nullable=False)
    type = Column(db.VARCHAR(40), nullable=False)
    distance = Column(db.FLOAT)
    metric = Column(db.VARCHAR(15))
    miles = Column(db.FLOAT)
    time = Column(db.TIME)
    pace = Column(db.TIME)
    feel = Column(db.INT(2), nullable=False)
    description = Column(db.VARCHAR(1000))
    time_created = Column(db.DATETIME, nullable=False)

    def __repr__(self):
        return '<Log %r>' % self.log_id
