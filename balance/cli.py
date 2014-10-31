#!/usr/bin/env python
# AMDG

import argparse
import logging
import locale
import sys
from collections import OrderedDict
from analyzers import BasicAnalyzer
from balance_book import BalanceBook
from loaders import BasicLoader, RepayLoader
from repay_book import RepayBook

locale.setlocale(locale.LC_ALL, 'en_US')

DEFAULT_BOOK = './balance.book'

def init_logging():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def format_amount(amt):
    return locale.currency(amt, symbol=True, grouping=True)

def format_table(table, key_space=5):
    """
    Accepts a dict of {string: string} and returns a string of the dict
    formatted into a table
    """
    longest = 0
    for k in table:
        if len(k) > longest:
            longest = len(k)
    result = '' 
    for k, v in table.iteritems():
        k += (longest - len(k)) * ' '
        result += k + (' '*key_space) + v + '\n'
    return result[:-1] # remove final \n

def align_dots(table):
    """
    Expects values to be money amount strings. Will the modified table with
    decimals aligned
    """
    longest = 0
    for v in table.values():
        if len(v) > longest:
            longest = len(v)
    for k, v in table.iteritems():
        v = ((longest - len(v)) * ' ') + v
        table[k] = v
    return table

def output(s):
    print(s)

def basic_analyzer(book_path):
    loader = BasicLoader(book_path) 
    bbook = BalanceBook(loader.load())
    return BasicAnalyzer(bbook)

def repay_analyzer(book_path):
    loader = RepayLoader(book_path)
    rbook = RepayBook(loader.load())
    return BasicAnalyzer(rbook)

def main():
    init_logging()
    parser = argparse.ArgumentParser()

    parser.add_argument('-a',
                        '--all',
                        help='calculate all metrics',
                        action='store_true')
    parser.add_argument('-b',
                        '--book',
                        help='path to balance.book',
                        action='store',
                        default=DEFAULT_BOOK)
    parser.add_argument('-e',
                        '--edit',
                        help='edit balance.book file with $EDITOR',
                        action='store_true')
    parser.add_argument('-r',
                        '--repay',
                        help='calculate amount needed to be repaid',
                        action='store_true')
    parser.add_argument('-s',
                        '--spent',
                        help='calculate total money spent',
                        action='store_true')
    parser.add_argument('-g',
                        '--gained',
                        help='calculate total money gained',
                        action='store_true')
    parser.add_argument('-l',
                        '--list',
                        help='list all entries',
                        action='store_true')

    args = parser.parse_args()
    
    if args.repay:
        analyzer = repay_analyzer(args.book)
        metrics = OrderedDict([
            ('Repay', format_amount(analyzer.gained())),
            ('Repaid', format_amount(analyzer.spent()))
        ])
        output(format_table(align_dots(metrics)))
    elif args.spent:
        analyzer = basic_analyzer(args.book)
        output(format_amount(analyzer.spent()))
    elif args.gained:
        analyzer = basic_analyzer(args.book)
        output(format_amount(analyzer.gained()))
    elif args.list:
        loader = BasicLoader(args.book) 
        bbook = BalanceBook(loader.load())
        for entry in bbook.entries:
            output(entry)
    elif args.all:
        bloader = BasicLoader(args.book) 
        bbook = BalanceBook(bloader.load())
        ba = BasicAnalyzer(bbook)

        rloader = RepayLoader(args.book)
        rbook = RepayBook(rloader.load())
        ra = BasicAnalyzer(rbook)

        metrics = OrderedDict([
            ('Balance', format_amount(ba.balance())),
            ('Spent', format_amount(ba.spent())),
            ('Gained', format_amount(ba.gained())),
            ('Repay', format_amount(ra.gained())),
            ('Repaid', format_amount(ra.spent())),
        ])
        output(format_table(align_dots(metrics)))
    elif args.edit:
        pass
    else:
        analyzer = basic_analyzer(args.book)
        output(format_amount(analyzer.balance()))

if __name__ == '__main__':
    main()
