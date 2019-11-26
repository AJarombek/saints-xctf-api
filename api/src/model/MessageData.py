"""
Message model that only includes data columns.
Author: Andrew Jarombek
Date: 11/24/2019
"""

from .Message import Message


class MessageData:
    def __init__(self, message: Message):
        """
        Create a message object without any auditing fields.
        :param message: The original Message object with auditing fields.
        """
        if message is not None:
            self.message_id = message.message_id
            self.username = message.username
            self.first = message.first
            self.last = message.last
            self.group_name = message.group_name
            self.time = message.time
            self.content = message.content
            self.deleted = message.deleted

    def __str__(self):
        """
        String representation of a group/team message.  This representation is meant to be human readable.
        :return: The message in string form.
        """
        return f'MessageData: [message_id: {self.message_id}, username: {self.username}, first: {self.first}, ' \
            f'last: {self.last}, group_name: {self.group_name}, time: {self.time}, content: {self.content}, ' \
            f'deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of a group/team message.  This representation is meant to be machine readable.
        :return: The message in string form.
        """
        return '<MessageData %r>' % self.message_id

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this group/team message.
        :return: True if the objects are equal, False otherwise.
        """
        return Message.compare(self, other)
