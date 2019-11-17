"""
Log model that only includes data columns.
Author: Andrew Jarombek
Date: 11/17/2019
"""

from .Log import Log


class LogData:
    def __init__(self, log: Log):
        """
        Create an exercise log object without any auditing fields.
        :param log: The original Log object with auditing fields.
        """
        if log is not None:
            self.log_id = log.log_id
            self.username = log.username
            self.first = log.first
            self.last = log.last
            self.name = log.name
            self.location = log.location
            self.date = log.date
            self.type = log.type
            self.distance = log.distance
            self.metric = log.metric
            self.miles = log.miles
            self.time = log.time
            self.pace = log.pace
            self.feel = log.feel
            self.description = log.description
            self.time_created = log.time_created
            self.deleted = log.deleted

    def __str__(self):
        """
        String representation of an exercise log.  This representation is meant to be human readable.
        :return: The exercise log in string form.
        """
        return f'LogData: [log_id: {self.log_id}, username: {self.username}, first: {self.first}, last: {self.last}, ' \
            f'name: {self.name}, location: {self.location}, date: {self.date}, type: {self.type} ' \
            f'distance: {self.distance}, metric: {self.metric}, miles: {self.miles}, time: {self.time}, ' \
            f'pace: {self.pace}, feel: {self.feel}, description: {self.description}, ' \
            f'time_created: {self.time_created}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of an exercise log.  This representation is meant to be machine readable.
        :return: The exercise log in string form.
        """
        return '<LogData %r>' % self.log_id

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this exercise log.
        :return: True if the objects are equal, False otherwise.
        """
        return Log.compare(self, other)
