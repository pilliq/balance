# AMDG

class BaseTest(object):
    def check_entry(self, entry, amount, category,
                    description, vendor, method, date):
        self.assertEquals(amount, entry.amount)
        self.assertEquals(category, entry.category)
        self.assertEquals(description, entry.description)
        self.assertEquals(vendor, entry.vendor)
        self.assertEquals(method, entry.method)
        self.assertEquals(date, entry.date)
