class LetterBag(object):
    """A minimal bag/multiset/Counter tweaked for checking alphabetical letters

    This performs slightly better than collections.Counter for checking if
    a word is "in" a set of letters, by taking advantage of the fact that
    the letters are sortable.
    """
    def __init__(self, word=''):
        self._letters = sorted(word)

    def add(self, word):
        self._letters.extend(word)
        self._letters.sort()

    def __contains__(self, word):
        letters = sorted(word)
        mynext = 0  # Which letter in the bag will I look at next?
        mylen = len(self._letters)
        for letter in letters:
            while mynext < mylen and letter > self._letters[mynext]:
                mynext += 1
            if mynext >= mylen or letter < self._letters[mynext]:
                return False
            mynext += 1
        return True


class Board(object):
    """Represent a board state

    Does not (currently?) apply any game logic; any word will do.
    """

    _neighbours = [
        0x23,  0x47,  0x8e,  0x11c,  0x218,
        0x461,  0x8e2,  0x11c4,  0x2388,  0x4310,
        0x8c20,  0x11c40,  0x23880,  0x47100,  0x86200,
        0x118400,  0x238800,  0x471000,  0x8e2000,  0x10c4000,
        0x308000,  0x710000,  0xe20000,  0x1c40000,  0x1880000,
    ]

    def __init__(self):
        # For each player, the blocks they hold, and the positions they can
        # play (ie, the blocks the other player doesn't have blocked)
        self.positions = [
            [0, 0x1ffffff],
            [0, 0x1ffffff],
        ]
        self._letters = ''
        self._counts = LetterBag()

    def setup(self, letters):
        """Ready the board for play with @letters"""
        # This should probably be refactored to go in __init__
        if isinstance(letters, basestring):
            letters = letters.replace(' ', '').replace("\n", '').lower()

        if len(letters) != 25:
            raise ValueError("A board must consist of 25 letters")

        self._letters = letters
        self._counts.add(letters)

    def apply_play(self, player, places):
        changed = places & self.positions[player][1]
        self.positions[player][0] |= changed
        self.positions[1 - player][0] &= ~changed
        self._recalculate_blocked()

    def plays_for(self, word):
        """Find the list of plays which we can use to make @word

        Equivalent plays are not included
        """
        # TODO: Optimisation target #1
        # First find all the possible places for playing each letter of the
        # word
        possible_places = []
        for letter in word:
            places = [i for i, l in enumerate(self) if l == letter]
            possible_places.append(places)

        # Then turn that into a list of ways to play that word
        plays = [[x] for x in possible_places[0]]
        for places in possible_places[1:]:
            newplays = []
            for place in places:
                for partial_play in plays:
                    if place in partial_play:
                        # We can't add to this partial play with this place
                        continue
                    newplays.append(partial_play + [place])
            plays = newplays

        # Now we remove equivalent plays
        play_check = {}
        for play in plays:
            playbits = self.to_bits(play)
            if playbits in play_check:
                continue

            play_check[playbits] = play

        return play_check

    def _recalculate_blocked(self):
        for player in (0, 1):
            other = self.positions[1 - player][0]
            playable = 0x1ffffff
            for i, neigh in enumerate(self._neighbours):
                playable &= ~((other & neigh == neigh) << i)

            self.positions[player][1] = playable

    def to_word(self, play):
        return ''.join(self._letters[i] for i in play)

    def owner(self, block):
        for player in (0, 1):
            if self.positions[player][0] & (1 << block):
                return player
        return None

    def blocked(self, block):
        mask = 1 << block
        return bool((~self.positions[0][1] & mask) or
                    (~self.positions[1][1] & mask))

    def to_bits(self, positions):
        return sum(1 << x for x in positions)

    def to_positions(self, bits):
        set_bits = []
        pos = 0
        while bits:
            if bits % 2:
                set_bits.append(pos)
            pos += 1
            bits /= 2
        return set_bits

    def __iter__(self):
        return iter(self._letters)

    def __len__(self):
        return 25

    def __contains__(self, word):
        return word in self._counts

    def __getitem__(self, index):
        return self._letters[index]

    def __copy__(self):
        ret = self.__class__()
        ret.setup(self._letters)
        ret.positions = [
            [self.positions[0][0], self.positions[0][1]],
            [self.positions[1][0], self.positions[1][1]],
        ]
        return ret
