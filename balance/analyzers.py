# AMDG

class BasicAnalyzer(object):
    def __init__(self, balance_book):
        self.book = balance_book

    def balance(self):
        balance = 0
        for entry in self.book.entries:
            balance += entry.amount
        return balance

    def spent(self):
        spent = 0
        for entry in self.book.entries:
            if entry.amount < 0:
                spent += abs(entry.amount)
        return spent

    def gained(self):
        gained = 0
        for entry in self.book.entries:
            if entry.amount > 0:
                gained += entry.amount
        return gained
