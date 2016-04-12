#!/usr/bin/env python
# AMDG

import argparse
import logging
import locale
import os
import sys
from collections import OrderedDict
from subprocess import call
from analyzers import BasicAnalyzer
from balance_book import BalanceBook
from loaders import BasicLoader, RepayLoader
from repay_book import RepayBook

locale.setlocale(locale.LC_ALL, 'en_US')

DEFAULT_BOOK = './balance.book'
DEFAULT_EDITOR = 'vim'

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

def basic_analyzer(filename=None, content=None):
    loader = BasicLoader(filename=filename, content=content)
    bbook = BalanceBook(loader.load())
    return BasicAnalyzer(bbook)

def repay_analyzer(filename=None, content=None):
    loader = RepayLoader(filename=filename, content=content)
    rbook = RepayBook(loader.load())
    return BasicAnalyzer(rbook)

def get_piped():
    """
    Returns data if input piped through stdin, else None
    """
    with sys.stdin as stdin:
        if not stdin.isatty():
            return stdin.read()
        else:
            return None

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
                        default=None)
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
    parser.add_argument('--eq',
                        help="specify column equality filter, e.g. '--eq method credit' is equivalent to 'method == credit'",
                        action='store',
                        default=None,
                        nargs=2)
    parser.add_argument('--ne',
                        help="specify column not equality filter, e.g. '--ne method credit' is equivalent to 'method != credit'",
                        action='store',
                        default=None,
                        nargs=2)

    args = parser.parse_args()

    content = get_piped()
    book_path = None
    if args.book is None and content is None:
        book_path = DEFAULT_BOOK
    elif content is not None:
        book_path = None
    else:
        book_path = args.book
    
    loader = BasicLoader(filename=book_path, content=content)
    balance_book = BalanceBook(loader.load())

    if args.eq:
        kwargs = dict([set(args.eq)])
        balance_book = BalanceBook(balance_book.eq(**kwargs))
    if args.ne:
        kwargs = dict([set(args.ne)])
        balance_book = BalanceBook(balance_book.ne(**kwargs))

    if args.repay:
        analyzer = repay_analyzer(filename=book_path, content=content)
        metrics = OrderedDict([
            ('Repay', format_amount(analyzer.gained())),
            ('Repaid', format_amount(analyzer.spent()))
        ])
        output(format_table(align_dots(metrics)))
    elif args.spent:
        analyzer = BasicAnalyzer(balance_book)
        output(format_amount(analyzer.spent()))
    elif args.gained:
        analyzer = BasicAnalyzer(balance_book)
        output(format_amount(analyzer.gained()))
    elif args.list:
        for entry in balance_book.entries:
            output(entry)
    elif args.all:
        ba = BasicAnalyzer(balance_book)

        rloader = RepayLoader(filename=book_path, content=content)
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
        EDITOR = os.environ.get('EDITOR', DEFAULT_EDITOR)
        call([EDITOR, book_path])
        analyzer = basic_analyzer(filename=book_path, content=content)
        output(format_amount(analyzer.balance()))
    else:
        analyzer = BasicAnalyzer(balance_book)
        output(format_amount(analyzer.balance()))

if __name__ == '__main__':
    main()
