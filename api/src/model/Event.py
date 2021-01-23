"""
Event ORM model for the 'events' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Event(db.Model):

    def __init__(self, event: dict):
        """
        Initialize an Event by passing in a dictionary.
        :param comment: A dictionary with fields matching the Event fields
        """
        self.event_id = event.get('event_id')
        self.name = event.get('name')
        self.group_name = event.get('group_name')
        self.start_date = event.get('start_date')
        self.end_date = event.get('end_date')
        self.start_time = event.get('start_time')
        self.end_time = event.get('end_time')
        self.description = event.get('description')
        self.deleted = event.get('deleted')
        self.created_date = event.get('created_date')
        self.created_user = event.get('created_user')
        self.created_app = event.get('created_app')
        self.modified_date = event.get('modified_date')
        self.modified_user = event.get('modified_user')
        self.modified_app = event.get('modified_app')
        self.deleted_date = event.get('deleted_date')
        self.deleted_user = event.get('deleted_user')
        self.deleted_app = event.get('deleted_app')

    __tablename__ = 'events'

    # Data Columns
    event_id = Column(db.INT, autoincrement=True, primary_key=True)
    name = Column(db.VARCHAR(40), nullable=False)
    group_name = Column(db.VARCHAR(20), db.ForeignKey('groups.group_name'), nullable=False)
    start_date = Column(db.DATE, nullable=False)
    end_date = Column(db.DATE)
    start_time = Column(db.TIME)
    end_time = Column(db.TIME)
    description = Column(db.VARCHAR(1000))
    deleted = Column(db.BOOLEAN)

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

    def __str__(self):
        """
        String representation of an event.  This representation is meant to be human readable.
        :return: The event/meeting.
        """
        return f"Event: [event_id: {self.event_id}, name: {self.name}, group_name: {self.group_name}, " \
            f"start_date: {self.start_date}, end_date: {self.end_date}, start_time: {self.start_time}, " \
            f"end_time: {self.end_time}, description: {self.description}, deleted: {self.deleted}]"

    def __repr__(self):
        """
        String representation of an event.  This representation is meant to be machine readable.
        :return: The event/meeting.
        """
        return '<Event %r>' % self.name

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this Event.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            self.event_id == other.event_id,
            self.name == other.name,
            self.group_name == other.group_name,
            self.start_date == other.start_date,
            self.end_date == other.end_date,
            self.start_time == other.start_time,
            self.description == other.description,
            self.deleted == other.deleted
        ])
