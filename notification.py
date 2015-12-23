#################
# Monopoly/Engine
# notification.py
# 2015-12-22
# Kelvin Wu
#################

import abc

class Notification(abc.ABC):
    """Abstract notification class."""
    @abc.abstractmethod
    def visit(self, board):
        pass


class TNBuyOpp(Notification):
    """Notification that a player has landed on a purchasable tile."""
    def __init__(self, tile, player):
        self.tile = tile
        self.player = player

    def visit(self, board):
        board.
