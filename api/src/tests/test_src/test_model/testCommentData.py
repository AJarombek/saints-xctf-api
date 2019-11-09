"""
Test suite for the model representing comments on exercise logs [without the auditing columns]
(api/src/model/CommentData.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.Comment import Comment
from model.CommentData import CommentData


class TestComment(TestSuite):
    comment1 = CommentData(Comment({
        'comment_id': 1,
        'username': 'andy',
        'first': 'Andy',
        'last': 'Jarombek',
        'log_id': 1,
        'time': datetime.fromisoformat('2019-11-09'),
        'content': 'Test Comment',
        'deleted': False
    }))

    comment2 = CommentData(Comment({
        'comment_id': 2,
        'username': 'andy',
        'first': 'Andy',
        'last': 'Jarombek',
        'log_id': 1,
        'time': datetime.now(),
        'content': 'Another Test Comment',
        'deleted': False
    }))

    def test_comment_data_str(self) -> None:
        """
        Prove that the human readable string representation of an CommentData object is as expected.
        """
        self.assertEquals(
            str(self.comment1),
            'CommentData: [comment_id: 1, username: andy, first: Andy, last: Jarombek, log_id: 1, '
            'time: 2019-11-09 00:00:00, content: Test Comment, deleted: False]'
        )
        self.assertEquals(
            self.comment1.__str__(),
            'CommentData: [comment_id: 1, username: andy, first: Andy, last: Jarombek, log_id: 1, '
            'time: 2019-11-09 00:00:00, content: Test Comment, deleted: False]'
        )

    def test_comment_data_repr(self) -> None:
        """
        Prove that the machine readable string representation of an CommentData object is as expected.
        """
        self.assertEquals(repr(self.comment1), "<CommentData 1>")
        self.assertEquals(self.comment1.__repr__(), "<CommentData 1>")

    def test_comment_data_eq(self) -> None:
        """
        Prove that two CommentData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.comment1 == self.comment1)
        self.assertTrue(self.comment1.__eq__(self.comment1))

    def test_comment_data_ne(self) -> None:
        """
        Prove that two CommentData objects with different property values test negative for value equality.
        """
        self.assertTrue(self.comment1 != self.comment2)
        self.assertTrue(self.comment1.__ne__(self.comment2))
