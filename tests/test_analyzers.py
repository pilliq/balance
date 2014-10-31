# AMDG

import unittest
from balance import (
    BasicAnalyzer,
    BasicLoader,
    BalanceBook,
    RepayLoader,
    RepayBook
)
from base_test import BaseTest

class BasicAnalyzerTests(BaseTest, unittest.TestCase):
    def setUp(self):
        self.loader = BasicLoader('tests/data/basic_analyzer')
        self.bbook = BalanceBook(self.loader.load())
        self.analyzer = BasicAnalyzer(self.bbook)
        self.rloader = RepayLoader('tests/data/basic_analyzer')
        self.rbook = RepayBook(self.rloader.load())
        self.ranalyzer = BasicAnalyzer(self.rbook)

    def test_balance(self):
        self.assertEquals(786.10, self.analyzer.balance())
        # one +13, and one -13 entry
        self.assertEquals(0, self.ranalyzer.balance()) 

    def test_spend(self):
        self.assertEquals(213.90, self.analyzer.spent())
        self.assertEquals(13.00, self.ranalyzer.spent())

    def test_gained(self):
        self.assertEquals(1000.00, self.analyzer.gained())
        self.assertEquals(13.00, self.ranalyzer.gained())

if __name__ == '__main__':
    unittest.main()
