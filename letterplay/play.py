class Play(object):
    def __init__(self, player, places):
        self.player = player
        self.places = places

    def __iter__(self):
        return iter(self.places)
