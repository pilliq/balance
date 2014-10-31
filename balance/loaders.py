# AMDG

from entry import Entry

COMMENT_STR='#'

class BasicLoader(object):
    def __init__(self, filename):
        self.filename = filename
        pass

    def load(self, return_errors=False):
        entries = []
        errors = []
        with open(self.filename, 'r') as f:
            for i, line in enumerate(f):
                if line[0] == COMMENT_STR or line == '':
                    continue
                try:
                    entries.append(Entry(i+1, line.strip()))
                except ValueError as e:
                    errors.append({'error': e, 'entry': line})
                    continue
        if return_errors:
            return entries, errors
        return entries

class RepayLoader(object):

    methods = ('credit', 'mcash', 'mcheck')

    def __init__(self, filename):
        self.filename = filename

    def load(self, return_errors=False):
        entries = []
        errors = []
        with open(self.filename, 'r') as fp:
            for i, line in enumerate(fp):
                if line[0] == COMMENT_STR:
                    try:
                        entry = Entry(i+1, line[1:].strip())
                    except ValueError as e:
                        errors.append({'error': e, 'entry': line})
                        continue
                    if entry.category == 'repay':
                        entries.append(entry)
                else:
                    try:
                        entry = Entry(i+1, line.strip())
                    except ValueError as e:
                        errors.append({'error': e, 'entry': line})
                        continue
                    if entry.method in RepayLoader.methods:
                        entries.append(entry)
        if return_errors:
            return entries, errors
        return entries
