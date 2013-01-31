from functools import partial

from letterplay.board import Board
from letterplay.play import Play
from letterplay.suggestors.interface import Suggestor as ISuggestor


class Suggestor(ISuggestor):
    """Suggestor which weights words by how many blocks they block off"""

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
                self._allowed_plays.extend(self._board.plays_for(word))

    def _score_play(self, reusable_board, player, play):
        return self._score_board(
            self._pretend_play(Play(player, play), reusable_board), player)

    def _pretend_play(self, play, reusable_board):
        for i, block in enumerate(self._board):
            reusable_board[i].owner = block.owner
            reusable_board[i].blocked = block.blocked
        reusable_board.apply_play(play)
        return reusable_board

    def suggestions_for(self, player):
        suggestions = self._allowed_plays
        reusable_board = Board()
        reusable_board.setup(''.join([b.letter for b in self._board]))
        suggestions.sort(key=partial(self._score_play, reusable_board, player),
                         reverse=True)
        return suggestions

    def _score_board(self, board, player):
        score = 0
        if all(l.owner for l in board):
            # If all squares are owned; ie, the board is complete
            player_score = sum(l.owner == player for l in board)
            opponent_score = sum(l.owner != player for l in board)
            if player_score > opponent_score:
                return 1000
            else:
                return -1000

        for block in board:
            if block.owner == player:
                score += 1
                if block.blocked:
                    score += 5
            elif block.owner:  # If it's not free
                score -= 1
                if block.blocked:
                    score -= 5
        return score
