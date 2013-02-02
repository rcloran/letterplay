import unittest

from letterplay.board import LetterBag


class TestLetterCounter(unittest.TestCase):
    def setUp(self):
        self._lc = LetterBag()

    def test_basic(self):
        self._lc.add('abcdefghijklmnopqrstuvwxyz')
        self.assertTrue('a' in self._lc)
        self.assertTrue('aeiou' in self._lc)
        self.assertTrue('uaeo' in self._lc)

    def test_board_repeats(self):
        self._lc.add('aabbccdefghi')
        self.assertTrue('bab' in self._lc)
        self.assertTrue('aab' in self._lc)
        self.assertTrue('ac' in self._lc)
        self.assertTrue('i' in self._lc)

    def test_completely_missing(self):
        self._lc.add('abc')
        self.assertFalse('xyz' in self._lc)

    def test_dup_not_in(self):
        self._lc.add('aeiou')
        self.assertFalse('aaeiou' in self._lc)
        self.assertFalse('aeeiou' in self._lc)

    def test_empty_board(self):
        self.assertFalse('a' in self._lc)
        self.assertFalse('abc' in self._lc)

    def test_empty_word(self):
        # Not really sure what the semantic here should be. Just test things
        # don't blow up.
        self.assertTrue('' in self._lc)
        self._lc.add('bob')
        self.assertTrue('' in self._lc)
