# AMDG

from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, '')

class Operators(object):
    operators = ('+', '-')

    @staticmethod
    def valid(op):
        return op in Operators.operators

class ColumnPositions(object):
    AMOUNT = 0
    CATEGORY = 1
    DESCRIPTION = 2
    VENDOR = 3
    METHOD = 4
    DATE = 5

class Columns(object):
    EID = 'eid'
    AMOUNT = 'amount'
    CATEGORY = 'category'
    DESCRIPTION = 'description'
    VENDOR = 'vendor'
    METHOD = 'method'
    DATE = 'date'

    @staticmethod
    def exists(category):
        if category in (Columns.EID,
                        Columns.AMOUNT,
                        Columns.CATEGORY,
                        Columns.DESCRIPTION,
                        Columns.VENDOR,
                        Columns.METHOD,
                        Columns.DATE):
            return True
        return False
    
class Dates(object):
    default_format = '%m%d%y'
    supported_formats = (default_format,)

    @staticmethod
    def get_date(date_str):
        for fmt in Dates.supported_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
            except ValueError:
                continue
            else: # date conforms to one of the supported formats
                return parsed_date
            return None # should only get here if all supported formats fail

NUM_COLUMNS = 6

class Entry(object):
    def __init__(self, eid, raw_entry):
        ok, msg = self._parse(raw_entry)
        if not ok:
            raise ValueError("Not a valid entry. Error: %s" % msg)
        self._eid = eid

    def __str__(self):
        symbol = '+' if self.amount >= 0 else ''
        amount = locale.currency(self.amount, symbol=False)
        amount = symbol + amount
        return ':'.join([amount,
                self.category,
                self.description,
                self.vendor,
                self.method,
                self.date.strftime(Dates.default_format)])

    def __repr__(self):
        return "Entry(" + str(self.eid) + "," + str(self).__str__() + ")"

    def _parse(self, raw_entry):
        parts = raw_entry.split(':')

        # ensure correct number of columns
        length = len(parts)
        if length != NUM_COLUMNS:
            return (False,
                "Expected %s columns, found %s" % (NUM_COLUMNS, length,))

        # check that operator is supported
        if not Operators.valid(raw_entry[0]):
            return (False, "Invalid operator: '%s'" % raw_entry[0])

        # check that amount is a number
        try:
            self._amount = float(parts[ColumnPositions.AMOUNT])
        except ValueError:
            return (False,
                "Amount is not a number: %s" % parts[ColumnPositions.AMOUNT])
        
        # check if date format is valid
        self._date = Dates.get_date(parts[ColumnPositions.DATE])
        if self._date is None:
            return (False,
                "Invalid date format: %s" % parts[ColumnPositions.DATE])

        self._category = parts[ColumnPositions.CATEGORY]
        self._description = parts[ColumnPositions.DESCRIPTION]
        self._vendor = parts[ColumnPositions.VENDOR]
        self._method = parts[ColumnPositions.METHOD]

        return (True, '')

    def has_field(self, column):
        if column == 'eid':
            return True
        return Columns.exists(column) 

    @property
    def eid(self):
        return self._eid

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def category(self):
        return self._category

    @property
    def description(self):
        return self._description

    @property
    def vendor(self):
        return self._vendor

    @property
    def method(self):
        return self._method

    @property
    def date(self):
        return self._date
