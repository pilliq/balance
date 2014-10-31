# AMDG

import logging
from balance_book import BalanceBook
from itertools import islice

class RepayBook(object):
    """
    RepayBook keeps track of entries that have been and need to be repaid to 
    other people. It keeps these two types of entries in separate BalanceBooks.
    When both types of entries are combined into one BalanceBook or list,
    entries that have been repaid are negative, while entries that need to be
    repaid are positive.
    """
    epsilon = 0.00000001

    def __init__(self, entries):
        self.logger = logging.getLogger(type(self).__name__)
        self._raw_entries = entries
        self._repay, self._repaid = self._split_entries()
        self._expand_repaid()
        self._positize_repay()

    def _float_equals(self, a, b):
        return abs(a - b) < self.epsilon

    def _split_entries(self):
        repay = [] 
        repaid = [] 
        for e in self._raw_entries:
            if e.category == 'repay':
                repaid.append(e)
            else:
                repay.append(e)
        return BalanceBook(repay), BalanceBook(repaid)

    def _parse_eid(self, raw):
        if raw[0] == '#':
            try:
                return int(raw[1:])
            except ValueError:
                return None
        return None

    def _expand_repaid(self):
        for e in islice(self._repaid.entries, 0, len(self._repaid.entries)):
            repaid_total = 0
            for eid_str in e.description.split(' '):
                eid = self._parse_eid(eid_str)
                if eid is not None:
                    results = self._repay.filter(eid=eid)
                    if len(results) == 0:
                        self.logger.warning(
                            "Could not find repay entry for eid=%d", eid
                        )
                        continue
                    repay_entry = results[0]
                    repaid_total += abs(repay_entry.amount)
                    self._repay.remove(eid=repay_entry.eid)
                    ok = self._repaid.add(repay_entry)
                    if not ok:
                        self.logger.warning(
                            "Duplicate entry. eid=%d", repay_entry.eid
                        )
            if not self._float_equals(repaid_total,  abs(e.amount)):
                self.logger.warning(
                    "Total repay amount does not match total amount of items in repay description. eid=%d expected_repay_amount=%.2f actual_repay_amount=%.2f",
                    e.eid,
                    abs(e.amount),
                    repaid_total
                )
            self._repaid.remove(eid=e.eid)

    def _positize_repay(self):
        """
        Make amounts in self.repay positive
        """
        for e in self._repay.entries:
            e.amount = abs(e.amount)

    @property
    def entries(self):
        return self._repay.entries + self._repaid.entries

    @property
    def repay(self):
        """
        BalanceBook  of entries that need to be repaid. Amounts are positive.
        """
        return self._repay

    @property
    def repaid(self):
        """
        BalanceBook  of entries that have been repaid. Amounts are negative.
        """
        return self._repaid
