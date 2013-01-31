from sys import stdin


class Console(object):
    _players = ['blue', 'red']

    reset = white = ['\033[0m', '\033[0m']
    _colours = {
        None: ['\033[0m', '\033[0m'],
        0: ['\033[0;34m', '\033[1;34m'],
        1: ['\033[0;31m', '\033[1;31m'],
    }

    def __init__(self, board, suggestor):
        self._board = board
        self._suggestor = suggestor

    def loop(self):
        try:
            self._loop()
        except KeyboardInterrupt:
            return

    def _loop(self):
        self._board.setup(self.get_board())
        self.display(self._board)
        print 'Finding all possible words for this board...'
        self._suggestor.prep()  # Setup for this board
        while True:
            print 'Getting some suggestions for this board...'
            self.show_suggestions(self._suggestor.suggestions_for(0))
            play = self.get_play()
            if not play:
                break
            self._board.apply_play(play[0], play[1])
            self.display(self._board)

    def display(self, board):
        for i, letter in enumerate(board):
            self._display_block(letter, board.owner(i), board.blocked(i))
            if (i + 1) % 5 == 0:
                print self.reset[0]

    def get_board(self):
        print "Enter board in one line: ",
        l = stdin.readline()
        print
        return l

    def show_suggestions(self, suggestions):
        if not suggestions:
            return

        print "I have some suggestions for the blue player:"

        # The suggestor returns a number of options for how each word can be
        # played. Let's give the user a few more options by presenting only one
        # way of playing each one.
        seen_words = set()
        for positions, _ in suggestions:
            word = self._board.to_word(positions)
            if word in seen_words:
                continue
            numbers = ' '.join(str(i) for i in positions)
            print "%s (%s)" % (word, numbers)
            seen_words.add(word)
            if len(seen_words) >= 5:
                break

    def get_play(self):
        play = None
        while not play:
            print 'Enter a play (eg "red foo"): ',
            line = stdin.readline().strip()
            print

            if not line:
                return

            parts = line.split()

            if parts[0] not in self._players:
                print 'Bad player. Try again.'
                continue

            player = self._players.index(parts[0])

            possible_plays = self._board.plays_for(parts[1])
            if not possible_plays:
                print "That word cannot be played on the board"
                continue

            play = 0
            if len(possible_plays) > 1:
                possible_plays.sort()
                print "There are a few ways of playing that word"
                for i, possible_play in enumerate(possible_plays):
                    print "%s) %s" % (i + 1,
                                      ' '.join(str(x) for x in possible_play))
                print "Which one? ",
                line = stdin.readline()
                play = int(line.strip()) - 1
            positions = possible_plays[play]
            play = (player, self._board.to_bits(positions))
        return play

    def _display_block(self, letter, owner, blocked):
        c = self._colours[owner][blocked]
        print '%s%s' % (c, letter, ),
