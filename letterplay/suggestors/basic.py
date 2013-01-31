from copy import copy

from letterplay.suggestors.interface import Suggestor as ISuggestor


def bitcount(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


class Suggestor(ISuggestor):
    """Suggestor which weights words by how many blocks they block off"""
    _bitcache = [bitcount(n) for n in range(256)]

    def __init__(self, dictionary, board):
        ISuggestor.__init__(self, dictionary, board)
        self._dict = dictionary
        self._board = board

        self._allowed_plays = []

    def prep(self):
        # We can cache this, since a board's letters (ie, the possible words)
        # don't change. But we need to re-sort it each time.
        self._allowed_plays = []
        for word in self._dict:
            if word in self._board:
                plays = self._board.plays_for(word)
                self._allowed_plays.extend((p, self._board.to_bits(p))
                                           for p in plays)

    def _score_play(self, reusable_board, player, play):
        return self._score_board(
            self._pretend_play(player, play, reusable_board), player)

    def _pretend_play(self, player, places, reusable_board):
        # TODO: How should board handle updates like this efficiently, without
        # breaking encapsulation?
        pos = self._board.positions
        reusable_board.positions = [
            [pos[0][0], pos[0][1]],
            [pos[1][0], pos[1][1]],
        ]
        reusable_board.apply_play(player, places)
        return reusable_board

    def suggestions_for(self, player):
        suggestions = self._allowed_plays
        reusable_board = copy(self._board)

        def score(play):
            return self._score_play(reusable_board, player, play[1])

        suggestions.sort(key=score, reverse=True)
        return suggestions

    def _bitcount(self, n):
        return self._bitcache[n & 255] + \
            self._bitcache[(n & 65280) >> 8] + \
            self._bitcache[(n & 16711680) >> 16] + \
            self._bitcache[(n & 4278190080) >> 24]

    def _score_board(self, board, player):
        score = 0
        pos = board.positions
        if pos[0][0] | pos[1][0] == 0x1ffffff:
            # If all squares are owned; ie, the board is complete
            player_score = self._bitcount(pos[player][0])
            opponent_score = self._bitcount(pos[1 - player][0])
            if player_score > opponent_score:
                return float("inf")
            else:
                return -float("inf")

        other = 1 - player
        score = self._bitcount(pos[player][0]) - self._bitcount(pos[other][0])
        score += 5 * (self._bitcount(pos[player][1]) -
                      self._bitcount(pos[other][1]))
        return score
