# AMDG

import logging

class BalanceBook(object):
    def __init__(self, entries):
        self.logger = logging.getLogger(type(self).__name__)
        self._entries = self._group_by_eid(entries)

    def __iter__(self):
        for e in self._entries:
            yield e

    def _iter_days(self, start=None, stop=None, step=1):
        sorted_entries = sorted(self._entries, key=lambda entry: entry.date)
        start = sorted_entries[0].date if start is None else start
        stop = sorted_entries[-1].date if stop is None else stop
        # return some kind of generator
        pass

    def _group_by_eid(self, entries):
        eids = {}
        for e in entries:
            eids[e.eid] = e
        return eids

    def _remove(self, eid):
        del self._entries[eid]

    def add(self, entry):
        """
        Will return False if entry has same eid as another entry in the
        BalanceBook. Else, will add to book and return True.
        """
        if entry.eid in self._entries:
            return False
        self._entries[entry.eid] = entry
        return True

    def iter_day(self, start=None, stop=None):
        return self._iter_days(start=start, stop=stop, step=1)

    def iter_week(self, start=None, stop=None):
        return self._iter_days(start=start, stop=stop, step=7)

    def iter_month(self, start=None, stop=None):
        pass

    def iter_year(self, start=None, stop=None):
        pass

    @property
    def entries(self):
        return self._entries.values()

    def print_out(self):
        for e in self.entries:
            print(e)

    def remove(self, **kwargs):
        entries = self.filter(**kwargs)
        for e in entries:
            self._remove(e.eid)

    def filter(self, **kwargs):
        result = []
        for e in self.entries:
            passes = True
            for key, value in kwargs.iteritems():
                if e.has_field(key):
                    if not getattr(e, key) == value:
                        passes = False
                else:
                    passes = False
            if passes:
                result.append(e)
        return result
