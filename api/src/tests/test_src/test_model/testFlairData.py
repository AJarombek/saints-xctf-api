"""
Test suite for the model representing a user's flair [without the auditing columns] (api/src/model/Flair.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from tests.TestSuite import TestSuite
from model.Flair import Flair
from model.FlairData import FlairData


class TestFlairData(TestSuite):
    flair1 = FlairData(Flair({
        'flair_id': 1,
        'username': 'andy',
        'flair': 'Website Creator',
        'deleted': False
    }))

    flair2 = FlairData(Flair({
        'flair_id': 2,
        'username': 'andy',
        'flair': 'Software Engineer',
        'deleted': True
    }))

    def test_flair_data_str(self) -> None:
        """
        Prove that the human readable string representation of a FlairData object is as expected.
        """
        self.assertEquals(
            str(self.flair1),
            'FlairData: [flair_id: 1, username: andy, flair: Website Creator, deleted: False]'
        )
        self.assertEquals(
            self.flair1.__str__(),
            'FlairData: [flair_id: 1, username: andy, flair: Website Creator, deleted: False]'
        )

    def test_flair_data_repr(self) -> None:
        """
        Prove that the machine readable string representation of a FlairData object is as expected.
        """
        self.assertEquals(repr(self.flair1), "<FlairData 1,'andy'>")
        self.assertEquals(self.flair1.__repr__(), "<FlairData 1,'andy'>")

    def test_flair_data_eq(self) -> None:
        """
        Prove that two FlairData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.flair1 == self.flair1)
        self.assertTrue(self.flair1.__eq__(self.flair1))

    def test_flair_data_ne(self) -> None:
        """
        Prove that two FlairData objects with different property values test negative for value equality.
        """
        self.assertTrue(self.flair1 != self.flair2)
        self.assertTrue(self.flair1.__ne__(self.flair2))
