import unittest

from letterplay.board import Board


class TestBoard(unittest.TestCase):
    """Test letterplay.board.Board"""
    def setUp(self):
        self._board = Board()
        self._board.setup('abcdefghijklmnopqrstuvwxy')

    def test_apply_play_simple(self):
        """Test simple plays"""
        self._board.apply_play(0, 0b001000001000001)
        self.assertEqual(self._board.positions[0][0], 0b001000001000001)
        self.assertEqual(self._board.positions[1][0], 0)
        self.assertEqual(self._board.positions[0][1], 0x1ffffff)
        self.assertEqual(self._board.positions[1][1], 0x1ffffff)

        self._board.apply_play(1, 0b001000001000001)
        self.assertEqual(self._board.positions[0][0], 0)
        self.assertEqual(self._board.positions[1][0], 0b001000001000001)
        self.assertEqual(self._board.positions[0][1], 0x1ffffff)
        self.assertEqual(self._board.positions[1][1], 0x1ffffff)

    def test_apply_play_block(self):
        """Test simple plays which cause blocks to be blocked"""
        # pylint: disable-msg=W0212
        self._board.apply_play(0, 0b0000100011)
        self.assertEqual(self._board.positions[0][0], 0b0000100011)
        self.assertEqual(self._board.positions[1][0], 0)
        self.assertEqual(self._board.positions[0][1], 0x1ffffff)
        self.assertEqual(self._board.positions[1][1], 0x1fffffe)

        self._board.apply_play(1, 0b0000100011)
        self.assertEqual(self._board.positions[0][0], 1)
        self.assertEqual(self._board.positions[1][0], 0b0000100010)
        self.assertEqual(self._board.positions[0][1], 0x1ffffff)
        self.assertEqual(self._board.positions[1][1], 0x1ffffff)
