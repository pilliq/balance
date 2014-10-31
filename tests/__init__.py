# AMDG

import unittest

from tests.test_entries import EntryTests
from tests.test_loaders import LoaderTests
from tests.test_balance_book import BalanceBookTests
from tests.test_repay_book import RepayBookTests
from tests.test_analyzers import BasicAnalyzerTests

def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EntryTests))
    suite.addTest(unittest.makeSuite(LoaderTests))
    suite.addTest(unittest.makeSuite(BalanceBookTests))
    suite.addTest(unittest.makeSuite(RepayBookTests))
    suite.addTest(unittest.makeSuite(BasicAnalyzerTests))
    return suite
