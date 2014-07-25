#!/usr/bin/env python

import argparse
import sys
import select
import time
from datetime import datetime

try:
    import simplejson as Json
except ImportError:
    import json as Json

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

class BalanceError(Exception): pass
class BalanceQueryError(BalanceError): pass
class BalanceCommandError(BalanceError): pass

def json(fp):
    result = []
    for line in fp:
        parts = line.strip().split(':')
        result.append(dict(zip(columns, parts)))
    return Json.dumps(result)

def _get_default(l, pos, default=None):
    """
    Given and list and position, returns the element of the list at that
    position, else returns the the default value on error.
    """
    try:
        return l[pos]
    except IndexError:
        return default

def list_entries(fp, args):
    entries = []
    if len(args) == 0: # list all entries
        for entry in clean(fp):
            entries.append(entry)
    elif args[0] not in columns:
        raise BalanceCommandError('Column "%s" does not exist' % args[0])
    elif args[0] == 'date':
        entries = list_date(fp, *args)
    else: # default is to list all entries whose column matches a value
        #entries = list_by_column(fp
        pass
    return entries

def list_by_column(fp, column, value):
    if column not in columns:
        raise BalanceQueryError('Column does not exist')
    entries = []
    for line in clean(fp):
        parts = line.strip().split(':')
        if parts[column_positions[column]] == value:
            entries.append(line)
    return entries

def list_date(fp, *args):
    """
    Expects `start` and optionally `end` in args
    """
    if len(args) == 0:
        raise BalanceCommandError('Need at least one date for listing dates')
    entries = []
    print("ARGS")
    print(args)
    start_date = _parse_date(_get_default(args, 0, ''))
    end_date = _parse_date(_get_default(args, 1, ''))
    if start_date is None:
        raise BalanceCommandError('Invalid start date')
    if end_date is None:
        raise BalanceCommandError('Invalid end date')
    for line in clean(fp):
        parts = line.split(':')
        date = _parse_date(parts[column_positions['date']])
        if date >= start_date and date <= end_date:
            entries.append(line) 
    return entries

def _parse_date(date):
    for date_format in supported_date_formats:
        try:
            parsed_date = datetime.strptime(date, date_format)
        except ValueError:
            continue
        else: # date conforms to one of the supported formats 
            return parsed_date
        return None # should only get here if all supported formats fail

def _is_valid_date(date):
    if _parse_date(date) is None:
        return False
    return True

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

def log(data):
    sys.stderr.write(str(data)+'\n')

def main(entries, args):
    if args.list is not None:
        if args.list[0] not in columns:
            raise BalanceCommandError('Column "%s" does not exist' % args.list[0])
        print('\n'.join(list_by_column(entries, args.list[0], args.list[1])))

    elif args.output == 'json':
        print(json(entries))
    elif args.spent:
        print(total(entries, '-'))
    elif args.gained:
        print(total(entries, '+'))
    else:
        print(total(entries))

    exit(0)

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
    parser.add_argument('-l',
                        '--list',
                        nargs='+',
                        help='list all entries in [column] that match [value]')

    args = parser.parse_args()

    try:
        time.sleep(1)
        if select.select([sys.stdin,],[],[],0.0)[0]:
            log('stdin')
            main(sys.stdin, args)
        else:
            log('file')
            with open('./balance', 'r') as fp:
                main(fp, args)
            log('done')
    except BalanceError as e:
        print(e)
        exit(1)
