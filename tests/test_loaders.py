# AMDG

import unittest
from datetime import datetime
from balance import BasicLoader, RepayLoader
from base_test import BaseTest

class LoaderTests(BaseTest, unittest.TestCase):
    def test_basic_loader(self):
        loader = BasicLoader('tests/data/basic_loader')
        entries, errors = loader.load(return_errors=True)
        self.assertEquals(1, len(entries))
        entry = entries[0]
        self.assertEquals(-5.00, entry.amount)
        self.assertEquals(2, len(errors))
        self.assertEquals(errors[0]['entry'], '\n')
        self.assertTrue(errors[0]['error'].message.startswith('Not a valid entry'))
        self.assertEquals(errors[1]['entry'], 'this is a bad line:\n')
        self.assertTrue(errors[1]['error'].message.startswith('Not a valid entry'))

    def test_repay_loader(self):
        loader = RepayLoader('tests/data/repay_loader')
        entries, errors = loader.load(return_errors=True)
        self.assertEquals(4, len(entries))
        entry = entries.pop()
        self.assertEquals(-11.00, entry.amount)
        self.assertEquals('repay', entry.category)
        self.assertEquals('#2', entry.description)
        self.assertEquals('Joe', entry.vendor)
        self.assertEquals('cash', entry.method)
        self.assertEquals(datetime(2014,10,3), entry.date)
        for e in entries:
            self.assertTrue(e.method in RepayLoader.methods)
        self.assertEquals(2, len(errors))
        self.assertEquals(errors[0]['entry'], '#hello\n')
        self.assertTrue(errors[0]['error'].message.startswith('Not a valid entry'))
        self.assertEquals(errors[1]['entry'], 'bad line\n')
        self.assertTrue(errors[1]['error'].message.startswith('Not a valid entry'))

if __name__ == '__main__':
    unittest.main()
