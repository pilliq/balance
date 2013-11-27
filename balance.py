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
supported_date_formats = ('%m%d%y',)

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

def _is_valid_date(date):
    for date_format in supported_date_formats:
        try:
            datetime.strptime(date, date_format)
        except ValueError:
            continue
        else: # date conforms to one of the supported formats
            return True
        return False # should only get here if all supported formats fail

def valid(line, strict=False):
    """
    Return True if line is valid. If strict is True, checks if line has no more
    columns than the number of supported columns.
    """
    parts = line.split(':')

    # if strict, make sure there are no extra columns
    if strict:
        if len(parts) != len(columns):
            return False
    # else, check if line has at least as many columns as is supported
    else:
        if len(parts) < len(columns):
            return False

    # check that operator is supported
    if line[0] not in operators:
        return False

    # check that amount is a number
    try:
        float(parts[column_positions['amount']][1:])
    except ValueError:
        return False
    
    # check if date format is valid
    if not _is_valid_date(parts[column_positions['date']]):
        return False

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
