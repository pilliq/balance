# AMDG

import unittest
from datetime import datetime
from balance import BasicLoader, BalanceBook, Entry
from base_test import BaseTest

class BalanceBookTests(BaseTest, unittest.TestCase):
    def test_load(self):
        loader = BasicLoader('tests/data/balance_book')
        bbook = BalanceBook(loader.load())
        self.assertEquals(6, len(bbook.entries))

    def test_add(self):
        entry = '-32.00:transport:train ticket:CalTrain:cash:092814'
        loader = BasicLoader('tests/data/balance_book')
        bbook = BalanceBook(loader.load())
        self.assertFalse(bbook.add(Entry(1, entry)))
        self.assertEquals(6, len(bbook.entries))
        self.assertTrue(bbook.add(Entry(7, entry)))
        self.assertEquals(7, len(bbook.entries))
        self.assertEquals(1, len(bbook.eq(eid=7)))

    def test_filter(self):
        loader = BasicLoader('tests/data/balance_book')
        bbook = BalanceBook(loader.load())

        entries = bbook.eq(eid=1)
        self.assertEquals(1, len(entries))
        self.check_entry(entries[0],
                         -11.00,
                         'food',
                         'burrito for lunch',
                         'Chipotle',
                         'cash',
                         datetime(2014,10,1))

        entries = bbook.eq(amount=-11.00)
        self.assertEquals(2, len(entries))
        self.check_entry(entries[0],
                         -11.00,
                         'food',
                         'burrito for lunch',
                         'Chipotle',
                         'cash',
                         datetime(2014,10,1))
        self.check_entry(entries[1],
                         -11.00,
                         'food',
                         'burrito for dinner',
                         'Chipotle',
                         'cash',
                         datetime(2014,10,1))

        entries = bbook.eq(category='fuel')
        self.assertEquals(1, len(entries))
        self.check_entry(entries[0],
                         -40.00,
                         'fuel',
                         'fill up on gas',
                         'BP',
                         'credit',
                         datetime(2014,10,1))

        entries = bbook.eq(description='gym membership')
        self.assertEquals(1, len(entries))
        self.check_entry(entries[0],
                         -30.00,
                         'fitness',
                         'gym membership',
                         'LA Fitness',
                         'cash',
                         datetime(2014,10,23))

        entries = bbook.eq(vendor='Amazon')
        self.assertEquals(1, len(entries))
        self.check_entry(entries[0],
                         -50.00,
                         'books',
                         'a bunch of books',
                         'Amazon',
                         'mcredit',
                         datetime(2014,10,04))

        entries = bbook.eq(method='debit')
        self.assertEquals(1, len(entries))
        self.check_entry(entries[0],
                         -3.25,
                         'groceries',
                         'milk',
                         'Giant',
                         'debit',
                         datetime(2014,10,23))

        entries = bbook.eq(date=datetime(2014,10,04))
        self.assertEquals(1, len(entries))
        self.check_entry(entries[0],
                         -50.00,
                         'books',
                         'a bunch of books',
                         'Amazon',
                         'mcredit',
                         datetime(2014,10,04))

        entries = bbook.eq(amount=-11.00,
                               category='food',
                               description='burrito for lunch',
                               vendor='Chipotle',
                               method='cash',
                               date=datetime(2014,10,01))
        self.assertEquals(1, len(entries))
        self.check_entry(entries[0],
                         -11.00,
                         'food',
                         'burrito for lunch',
                         'Chipotle',
                         'cash',
                         datetime(2014,10,01))

        entries = bbook.eq(amount=-42.00)
        self.assertEquals(0, len(entries))

        entries = bbook.eq(amount=-42.00, method='cash')
        self.assertEquals(0, len(entries))

        entries = bbook.eq(bad=True)
        self.assertEquals(0, len(entries))

        entries = bbook.eq(bad=True, date=datetime(2014,10,04))
        self.assertEquals(0, len(entries))

    def test_remove(self):
        loader = BasicLoader('tests/data/balance_book')
        bbook = BalanceBook(loader.load())
        bbook.remove(amount=-11.00)
        self.assertEquals(4, len(bbook.entries))
        self.assertEquals(0, len(bbook.eq(amount=-11.00)))

if __name__ == '__main__':
    unittest.main()
