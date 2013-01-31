from letterplay.suggestors.interface import Suggestor as ISuggestor


class NullSuggestor(ISuggestor):
    """The null suggestor never suggests anything."""
    def __init__(self, dictionary, board):
        ISuggestor.__init__(self, dictionary, board)

    def suggestions_for(self, player):
        return []
