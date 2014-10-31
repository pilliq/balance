# AMDG

import unittest
from datetime import datetime
from balance import Entry
from base_test import BaseTest

class EntryTests(BaseTest, unittest.TestCase):
    def setUp(self):
        pass

    def test_parsing(self):
        # num columns
        self.assertRaises(ValueError, Entry, 0, 'this is not an entry')
        self.assertRaises(ValueError, Entry, 0, 'one:two:three:')
        self.assertRaises(ValueError, Entry, 0, 'one:two:three:four:five:six:seven:eight:nine')
        
        # operator
        self.assertRaises(ValueError, Entry, 0, '~53.80:gifts:card and $50 amazon gift card for Paul Shi for his birthday:Walgreens:mcredit:060714')

        # amount
        self.assertRaises(ValueError, Entry, 0, '-5.3.80:gifts:card and $50 amazon gift card for Paul Shi for his birthday:Walgreens:mcredit:060714')
        self.assertRaises(ValueError, Entry, 0, '-5k:gifts:card and $50 amazon gift card for Paul Shi for his birthday:Walgreens:mcredit:060714')

        # date format
        self.assertRaises(ValueError, Entry, 0, '-53.80:gifts:card and $50 amazon gift card for Paul Shi for his birthday:Walgreens:mcredit:260714')
        self.assertRaises(ValueError, Entry, 0, '-53.80:gifts:card and $50 amazon gift card for Paul Shi for his birthday:Walgreens:mcredit:0610714')

        # correctness
        entry = Entry(0, '-29.37:sports_equipment:volleyball and frisbee:Paragon Sports:mcredit:060714')
        self.assertEquals(entry.amount, -29.37)
        self.assertEquals(entry.category, 'sports_equipment')
        self.assertEquals(entry.description, 'volleyball and frisbee')
        self.assertEquals(entry.vendor, 'Paragon Sports')
        self.assertEquals(entry.method, 'mcredit')
        self.assertEquals(entry.date, datetime(2014, 06, 07))

        entry = Entry(0, '+400.09:paycheck:a good paycheck:MongoDB, Inc.:deposit:053014')
        self.assertEquals(entry.amount, 400.09)
        self.assertEquals(entry.category, 'paycheck')
        self.assertEquals(entry.description, 'a good paycheck')
        self.assertEquals(entry.vendor, 'MongoDB, Inc.')
        self.assertEquals(entry.method, 'deposit')
        self.assertEquals(entry.date, datetime(2014, 05, 30))

    def test_dates(self):
        pass

if __name__ == '__main__':
    unittest.main()
