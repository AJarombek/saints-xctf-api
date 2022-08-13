"""
WeekStart ORM model for the 'metrics' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Metric import Metric


class MetricDemo(Metric):
    __bind_key__ = 'demo'
