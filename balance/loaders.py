# AMDG

from entry import Entry

COMMENT_STR='#'

def _iter_lines(filename, content):
    if content is not None:
        for line in content.split('\n'):
            yield line
    if filename is not None:
        with open(filename, 'r') as f:
            for line in f:
                yield line

class BasicLoader(object):
    def __init__(self, filename=None, content=None):
        self.filename = filename
        self.content = content

    def load(self, return_errors=False):
        entries = []
        errors = []
        for i, line in enumerate(_iter_lines(self.filename, self.content)):
            if len(line) > 0:
                if line[0] == COMMENT_STR:
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

    def __init__(self, filename=None, content=None):
        self.filename = filename
        self.content = content

    def load(self, return_errors=False):
        entries = []
        errors = []
        for i, line in enumerate(_iter_lines(self.filename, self.content)):
            if len(line) > 0:
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
