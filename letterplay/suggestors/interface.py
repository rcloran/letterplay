from abc import ABCMeta, abstractmethod


class Suggestor(object):
    """A suggestor provides suggestions for a board

    This ABC defines the interface for suggestors
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, dictionary, board):
        pass

    @abstractmethod
    def suggestions_for(self, player):
        pass
