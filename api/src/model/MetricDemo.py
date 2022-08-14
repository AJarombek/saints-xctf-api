"""
WeekStart ORM model for the 'metrics' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from sqlalchemy import Column

from app import db
from model.Metric import Metric


class MetricDemo(Metric):
    __bind_key__ = 'demo'

    metric = Column(db.TEXT, primary_key=True)
