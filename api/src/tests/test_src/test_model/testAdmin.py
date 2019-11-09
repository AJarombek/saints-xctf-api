"""
Test suite for the model representing the possible group member types (api/src/model/Admin.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from tests.TestSuite import TestSuite
from model.Admin import Admin


class TestAdmin(TestSuite):

    def test_admin_str(self) -> None:
        """
        Prove that the human readable string representation of an Admin object is as expected.
        """
        admin = Admin({'user': 'user'})
        self.assertEquals(str(admin), 'Admin: [user: user]')
        self.assertEquals(admin.__str__(), 'Admin: [user: user]')

    def test_admin_repr(self) -> None:
        """
        Prove that the machine readable string representation of an Admin object is as expected.
        """
        admin = Admin({'user': 'admin'})
        self.assertEquals(repr(admin), '<Admin user>')
        self.assertEquals(admin.__repr__(), '<Admin user>')

    def test_admin_eq(self) -> None:
        """
        Prove that two Admin objects with the same property values test positive for value equality.
        """
        admin1 = Admin({'user': 'admin'})
        admin2 = Admin({'user': 'admin'})
        self.assertTrue(admin1 == admin2)
        self.assertTrue(admin1.__eq__(admin2))

    def test_admin_ne(self) -> None:
        """
        Prove that two Admin objects with different property values test negative for value equality.
        """
        admin1 = Admin({'user': 'admin'})
        admin2 = Admin({'user': 'user'})
        self.assertTrue(admin1 != admin2)
        self.assertTrue(admin1.__ne__(admin2))
