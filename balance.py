#!/usr/bin/env python

import argparse
from datetime import datetime

try:
    import simplejson as Json
except ImportError:
    import Json

file_name = './balance'
columns = ('amount', 'category', 'description', 'vendor', 'method', 'date')
column_positions = {
        'amount': 0,
        'category': 1,
        'description': 2,
        'vendor': 3,
        'method': 4,
        'date': 5
}
operators = ('-', '+')
date_formats = ('%m%d%y')

def json(fp):
    result = []
    for line in fp:
        parts = line.strip().split(':')
        result.append(dict(zip(columns, parts)))
    return Json.dumps(result)

def select():
    pass

def list(fp):
    pass

def valid(line, strict=False):
    """
    Return True if line is valid. If strict is True, if line has the correct
    number of supported columns.
    """
    parts = line.split(':')

    if strict:
        if len(parts) != len(columns): # correct number of columns
            return False

    if line[0] not in operators: # supported operator
        return False

    try: # amount is a number
        float(parts[column_positions['amount']][1:])
    except ValueError:
        return False
    
    if not len(parts[column_positions['date']].strip()) == 6:
        return False

    for date_format in date_formats:
        try:
            datetime.strptime(parts[column_positions['date']], date_format)
        except ValueError:
            continue
        else: # date conforms to one of the supported formats
            break
        return False # should only get here if all supported formats fail

    return True

# TODO: ability to yield a set of invalid lines
def clean(fp, yield_invalid_count=False):
    """
    Generator to ignore empty, commented out, and invalid lines. If 
    yield_invalid_count is True, the last yield will be the number of lines that
    are invalid in the balance document.
    """
    count = 0
    for line in fp:
        line = line.strip()
        if line == '':
            continue
        if line[0] == '#':
            continue
        if not valid(line):
            count += 1
            continue
        yield line
    if yield_invalid_count:
        yield count


def total(fp, sym=None):
    """
    Sums up entries in the balance file. fp is the file pointer to the balance
    file. sym is a character used to select which entries to sum. sym can be
    '+', '-', or None. If sym is None, both '+' and '-' are interpretted and
    summed. This is equivalent to the total balance. Returns a float of the sum
    """
    total = 0
    for line in clean(fp):
        if sym is None:
            total += float(line.strip().split(':')[0])
        if line[0] == sym:
            total += float(line.strip().split(':')[0][1:])
    return total

def average(fp, period):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', 
                        '--output', 
                        help='ouput in different formats like json', 
                        action='store')
    parser.add_argument('-s', 
                        '--spent', 
                        help='calculate total money spent', 
                        action='store_true')
    parser.add_argument('-g', 
                        '--gained', 
                        help='calculate total money gained', 
                        action='store_true')

    args = parser.parse_args()

    with open('./balance', 'r') as fp:
        if args.output == 'json':
            print(json(fp))
        elif args.spent:
            print(total(fp, '-'))
        elif args.gained:
            print(total(fp, '+'))
        else:
            print(total(fp))
