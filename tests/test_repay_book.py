# AMDG

import unittest
import logging
import sys
import balance
from datetime import datetime
from balance import BalanceBook, RepayBook, RepayLoader, Entry
from base_test import BaseTest
from utils import MockLoggingHandler

class RepayBookTests(BaseTest, unittest.TestCase):
    def test_load(self):
        loader = RepayLoader('tests/data/balance_book')
        bbook = BalanceBook(loader.load())
        self.assertEquals(1, len(bbook.entries))
        self.check_entry(bbook.entries[0],
                         -40.00,
                         'fuel',
                         'fill up on gas',
                         'BP',
                         'credit',
                         datetime(2014,10,01))

        loader = RepayLoader('tests/data/repay_book')
        rbook = RepayBook(loader.load())
        self.assertEquals(5, len(rbook.entries))
        self.assertEquals(1, len(rbook.repay.entries))
        self.check_entry(rbook.repay.entries[0],
                         +7.00,
                         'groceries',
                         'misc groceries',
                         'Pathmark',
                         'mcheck',
                         datetime(2014,9,29))
        self.assertEquals(4, len(rbook.repaid.entries))
        repaid_total = 0
        for e in rbook.repaid.entries:
            self.assertNotEqual('repay', e.category)
            repaid_total += e.amount
        self.assertEquals(-42.00, repaid_total)

    def test_load_errors(self):
        mlh = MockLoggingHandler()
        repay_logger = logging.getLogger(RepayBook.__name__)
        repay_logger.addHandler(mlh)
        loader = RepayLoader('tests/data/repay_book1')
        rbook = RepayBook(loader.load())
        self.assertEquals(1, len(mlh.warning))
        msg = mlh.warning[0]
        self.assertTrue('eid=3 expected_repay_amount=21.00 actual_repay_amount=15.00' in msg)
        mlh.reset()
        loader = RepayLoader('tests/data/repay_book2')
        rbook = RepayBook(loader.load())
        self.assertEquals(1, len(mlh.warning))
        msg = mlh.warning[0]
        self.assertTrue('Could not find repay entry for eid=3' in msg)

if __name__ == '__main__':
    unittest.main()
