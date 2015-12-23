#################
# Monopoly/Engine
# player.py
# 2015-12-22
# Kelvin Wu
#################

class Player(object):
    """Class to store player state data."""
    def __init__(self, name, piece, pos, board, piece, cash=1500):
        self.name = name
        self.piece = piece
        self._pos = pos
        self._board = board
        self._cash = cash

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, val):
        # TODO implement check for bankruptcy
        self._cash = val
