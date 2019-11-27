"""
Message data access from the SaintsXCTF MySQL database.  Contains messages which are private to group members.
Author: Andrew Jarombek
Date: 7/18/2019
"""

from dao.basicDao import BasicDao
from sqlalchemy.engine import ResultProxy
from database import db
from model.Message import Message


class MessageDao:

    @staticmethod
    def get_messages() -> list:
        """
        Retrieve all the group messages in the database
        :return: The result of the query.
        """
        return Message.query.order_by(Message.time).all()

    @staticmethod
    def get_message_by_id(message_id: int) -> Message:
        """
        Retrieve a single message by its unique id
        :param message_id: The unique identifier for a message.
        :return: The result of the query.
        """
        return Message.query.filter_by(message_id=message_id).first()

    @staticmethod
    def get_message_feed(group_name: str, limit: int, offset: int) -> ResultProxy:
        """
        Retrieve a collection of messages in a group
        :param group_name: The unique name of a group
        :param limit: The maximum number of messages to return
        :param offset: The number of messages to skip before returning
        :return: A list of messages
        """
        return db.session.execute(
            '''
            SELECT * FROM messages 
            WHERE group_name=:group_name 
            ORDER BY time DESC 
            LIMIT :limit OFFSET :offset
            ''',
            {'group_name': group_name, 'limit': limit, 'offset': offset}
        )

    @staticmethod
    def add_message(new_message: Message) -> bool:
        """
        Add a group message to the database.
        :param new_message: Object representing a message posted to a group.
        :return: True if the message is inserted into the database, False otherwise.
        """
        db.session.add(new_message)
        return BasicDao.safe_commit()

    @staticmethod
    def update_message(message: Message) -> bool:
        """
        Update a message in the database. Certain fields (message_id, username, first, last, group_name, time)
        can't be modified.
        :param message: Object representing an updated message.
        :return: True if the message is updated in the database, False otherwise.
        """
        db.session.execute(
            '''
            UPDATE messages SET 
                content=:content,
                modified_date=:modified_date,
                modified_app=:modified_app
            WHERE message_id=:message_id
            ''',
            {
                'message_id': message.message_id,
                'content': message.content,
                'modified_date': message.modified_date,
                'modified_app': message.modified_app
            }
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_message_by_id(message_id: int) -> bool:
        """
        Delete a message from the database based on its id.
        :param message_id: ID which uniquely identifies the message.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            'DELETE FROM messages WHERE message_id=:message_id',
            {'message_id': message_id}
        )
        return BasicDao.safe_commit()

    @staticmethod
    def soft_delete_message(message: Message) -> bool:
        """
        Soft Delete a group/team message from the database.
        :param message: Object representing a message to soft delete.
        :return: True if the soft deletion was successful without error, False otherwise.
        """
        db.session.execute(
            '''
            UPDATE messages SET 
                deleted=:deleted,
                modified_date=:modified_date,
                modified_app=:modified_app,
                deleted_date=:deleted_date,
                deleted_app=:deleted_app
            WHERE message_id=:message_id
            ''',
            {
                'message_id': message.message_id,
                'deleted': message.deleted,
                'modified_date': message.modified_date,
                'modified_app': message.modified_app,
                'deleted_date': message.deleted_date,
                'deleted_app': message.deleted_app
            }
        )
        return BasicDao.safe_commit()
