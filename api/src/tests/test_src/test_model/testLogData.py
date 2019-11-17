"""
Test suite for the model representing exercise logs [without the auditing columns] (api/src/model/LogData.py)
Author: Andrew Jarombek
Date: 11/17/2019
"""

from tests.TestSuite import TestSuite
from tests.test_src.test_model.testLog import TestLog
from model.Log import Log
from model.LogData import LogData


class TestLogData(TestSuite):
    log1_dict = TestLog.log1_dict
    log2_dict = TestLog.log2_dict

    log1 = LogData(Log(log1_dict))
    log1copy = LogData(Log(log1_dict))

    log2 = LogData(Log(log2_dict))

    def test_log_data_str(self) -> None:
        """
        Prove that the human readable string representation of a Log object is as expected.
        """
        log_str = 'LogData: [log_id: 1, username: andy, first: Andrew, last: Jarombek, ' \
            'name: Van Cortlandt NYRR XC 5K, location: Bronx, NY, date: 2019-11-17 00:00:00, type: run ' \
            'distance: 5, metric: kilometers, miles: 3.11, time: 17:35, ' \
            "pace: 5:40, feel: 5, " \
            "description: Didn't run very fast and felt tired, but it was nice to run a cross country race again., " \
            "time_created: 2019-11-17 00:00:00, deleted: None]"

        self.maxDiff = None
        self.assertEquals(str(self.log1), log_str)
        self.assertEquals(self.log1.__str__(), log_str)

    def test_log_data_repr(self) -> None:
        """
        Prove that the machine readable string representation of a LogData object is as expected.
        """
        self.assertEquals(repr(self.log1), "<LogData 1>")
        self.assertEquals(self.log1.__repr__(), "<LogData 1>")

    def test_log_data_eq(self) -> None:
        """
        Prove that two LogData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.log1 == self.log1copy)
        self.assertTrue(self.log1.__eq__(self.log1copy))

    def test_log_data_ne(self) -> None:
        """
        Prove that two LogData objects with different property values test negative for value equality.
        """
        self.assertTrue(self.log1 != self.log2)
        self.assertTrue(self.log1.__ne__(self.log2))
