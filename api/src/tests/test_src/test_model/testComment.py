"""
Test suite for the model representing comments on exercise logs (api/src/model/Comment.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.Comment import Comment


class TestComment(TestSuite):
    comment1 = Comment(
        {
            "comment_id": 1,
            "username": "andy",
            "first": "Andy",
            "last": "Jarombek",
            "log_id": 1,
            "time": datetime.fromisoformat("2019-11-09"),
            "content": "Test Comment",
            "deleted": False,
        }
    )

    comment2 = Comment(
        {
            "comment_id": 2,
            "username": "andy",
            "first": "Andy",
            "last": "Jarombek",
            "log_id": 1,
            "time": datetime.now(),
            "content": "Another Test Comment",
            "deleted": False,
        }
    )

    def test_comment_str(self) -> None:
        """
        Prove that the human-readable string representation of an Comment object is as expected.
        """
        self.assertEqual(
            str(self.comment1),
            "Comment: [comment_id: 1, username: andy, first: Andy, last: Jarombek, log_id: 1, "
            "time: 2019-11-09 00:00:00, content: Test Comment, deleted: False]",
        )

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(
            self.comment1.__str__(),
            "Comment: [comment_id: 1, username: andy, first: Andy, last: Jarombek, log_id: 1, "
            "time: 2019-11-09 00:00:00, content: Test Comment, deleted: False]",
        )

    def test_comment_repr(self) -> None:
        """
        Prove that the machine-readable string representation of an Comment object is as expected.
        """
        self.assertEqual(repr(self.comment1), "<Comment 1>")

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.comment1.__repr__(), "<Comment 1>")

    def test_comment_eq(self) -> None:
        """
        Prove that two Comment objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.comment1 == self.comment1)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.comment1.__eq__(self.comment1))

    def test_comment_ne(self) -> None:
        """
        Prove that two Comment objects with different property values test negative for value equality.
        """
        self.assertTrue(self.comment1 != self.comment2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.comment1.__ne__(self.comment2))
