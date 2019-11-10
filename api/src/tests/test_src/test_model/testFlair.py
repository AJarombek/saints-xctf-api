"""
Test suite for the model representing a user's flair (api/src/model/Flair.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from tests.TestSuite import TestSuite
from model.Flair import Flair


class TestFlair(TestSuite):
    flair1 = Flair({
        'flair_id': 1,
        'username': 'andy',
        'flair': 'Website Creator',
        'deleted': False
    })

    flair2 = Flair({
        'flair_id': 2,
        'username': 'andy',
        'flair': 'Software Engineer',
        'deleted': True
    })

    def test_flair_str(self) -> None:
        """
        Prove that the human readable string representation of a Flair object is as expected.
        """
        self.assertEquals(
            str(self.flair1),
            'Flair: [flair_id: 1, username: andy, flair: Website Creator, deleted: False]'
        )
        self.assertEquals(
            self.flair1.__str__(),
            'Flair: [flair_id: 1, username: andy, flair: Website Creator, deleted: False]'
        )

    def test_flair_repr(self) -> None:
        """
        Prove that the machine readable string representation of a Flair object is as expected.
        """
        self.assertEquals(repr(self.flair1), "<Flair 1,'andy'>")
        self.assertEquals(self.flair1.__repr__(), "<Flair 1,'andy'>")

    def test_flair_eq(self) -> None:
        """
        Prove that two Flair objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.flair1 == self.flair1)
        self.assertTrue(self.flair1.__eq__(self.flair1))

    def test_flair_ne(self) -> None:
        """
        Prove that two Flair objects with different property values test negative for value equality.
        """
        self.assertTrue(self.flair1 != self.flair2)
        self.assertTrue(self.flair1.__ne__(self.flair2))
