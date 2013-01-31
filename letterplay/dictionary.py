class Dictionary(object):
    def __init__(self, wordfile):
        self._wordfile = wordfile
        self._words = set()

        self._read()

    def _read(self):
        with open(self._wordfile) as words:
            for word in words:
                self._words.add(word.strip().lower())

    def __len__(self):
        raise len(self._words)

    def __iter__(self):
        return iter(self._words)

    def __contains__(self, word):
        return word in self._words
