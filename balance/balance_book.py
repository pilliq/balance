# AMDG

import logging
import operator

class BalanceBook(object):
    def __init__(self, entries):
        self.logger = logging.getLogger(type(self).__name__)
        self._entries = self._group_by_eid(entries)

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

    @property
    def entries(self):
        return self._entries.values()

    def print_out(self):
        for e in self.entries:
            print(e)

    def remove(self, **kwargs):
        entries = self.eq(**kwargs)
        for e in entries:
            self._remove(e.eid)

    def eq(self, **kwargs):
        return self._filter(operator.eq, **kwargs)

    def ne(self, **kwargs):
        return self._filter(operator.ne, **kwargs)

    def _filter(self, op, **kwargs):
        result = []
        for e in self.entries:
            passes = True
            for key, value in kwargs.iteritems():
                print(key, value)
                if e.has_field(key):
                    if not op(getattr(e, key), value):
                        passes = False
                else:
                    passes = False
            if passes:
                result.append(e)
        return result
