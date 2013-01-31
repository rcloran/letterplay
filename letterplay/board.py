from collections import Counter


class Block(object):
    def __init__(self, letter, owner=0, blocked=False):
        self.letter = letter
        self.owner = owner
        self.blocked = blocked


class Board(object):
    """Represent a board state

    Does not (currently?) apply any game logic; any word will do.
    """

    _neighbours = [
        [1, 5], [0, 2, 6], [1, 3, 7], [2, 4, 8], [3, 9],
        [0, 6, 10], [1, 5, 7, 11], [2, 6, 8, 12], [3, 7, 9, 13], [4, 8, 14],
        [5, 11, 15], [6, 10, 12, 16], [7, 11, 13, 17], [8, 12, 14, 18],
        [9, 13, 19],
        [10, 16, 20], [11, 15, 17, 21], [12, 16, 18, 22], [13, 17, 19, 23],
        [14, 18, 24],
        [15, 21], [16, 20, 22], [17, 21, 23], [18, 22, 24], [19, 23]
    ]

    def __init__(self):
        self._positions = []
        self._counts = Counter()

    def setup(self, letters):
        """Ready the board for play with @letters"""
        # This should probably be refactored to go in __init__
        letters = letters.replace(' ', '').replace("\n", '').lower()

        if len(letters) != 25:
            raise ValueError("A board must consist of 25 letters")

        self._positions = [Block(letter) for letter in letters]
        self._counts = Counter(letters)

    def apply_play(self, play):
        for position in play:
            if not self._positions[position].blocked:
                self._positions[position].owner = play.player
        self._recalculate_blocked()

    def plays_for(self, word):
        """Find the list of plays which we can use to make @word

        Equivalent plays are not included
        """
        # First find all the possible places for playing each letter of the
        # word
        possible_places = []
        for letter in word:
            places = [i for i, l in enumerate(self) if l.letter == letter]
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
        filteredplays = []
        play_check = set()
        for play in plays:
            play_s = '-'.join(str(b) for b in sorted(play))
            if play_s in play_check:
                continue

            filteredplays.append(play)
            play_check.add(play_s)

        return filteredplays

    def _recalculate_blocked(self):
        for i, block in enumerate(self._positions):
            if not block.owner:
                continue
            if all(self._positions[n].owner == block.owner
                   for n in self._neighbours[i]):
                block.blocked = True
            else:
                block.blocked = False

    def to_word(self, play):
        return ''.join(self._positions[i].letter for i in play)

    def __iter__(self):
        return iter(self._positions)

    def __len__(self):
        return 25

    def __contains__(self, word):
        cword = Counter(word)
        return self._counts & cword == cword

    def __getitem__(self, index):
        return self._positions[index]
