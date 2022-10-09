"""
Metric ORM model for the 'metrics' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Metric(db.Model):
    def __init__(self, metric: dict):
        """
        Initialize a Metric by passing in a dictionary.
        :param metric: A dictionary with fields matching the Metric fields
        """
        self.metric = metric.get("metric")

    __tablename__ = "metrics"
    __bind_key__ = "app"

    metric = Column(db.VARCHAR(15), primary_key=True)

    def __str__(self):
        """
        String representation of a distance metric.  This representation is meant to be human readable.
        :return: The metric in string form.
        """
        return f"Metric: [metric: {self.metric}]"

    def __repr__(self):
        """
        String representation of a distance metric.  This representation is meant to be machine readable.
        :return: The metric in string form.
        """
        return "<Metric %r>" % self.metric

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this metric.
        :return: True if the objects are equal, False otherwise.
        """
        return self.metric == other.metric
