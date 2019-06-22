"""
Metric ORM model for the 'metrics' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Metric(db.Model):
    __tablename__ = 'metrics'

    metric = Column(db.VARCHAR(15), primary_key=True)

    def __repr__(self):
        return '<Metric %r>' % self.metric
