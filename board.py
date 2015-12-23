#################
# Monopoly/Engine
# board.py
# 2015-12-10
# Kelvin Wu
#################

import dice
import parser
import player
import tile

class Board(object):
    """Handles state information for the board."""
    def __init__(self):
        dataObject = parser.MonopolyInitParser(self, 'standard.json')
        self.gameStyle = dataObject.gameStyle
        self._boardSize = dataObject.boardSize
        self._tiles = dataObject.tiles
        self._dice = dice.Dice()

    def acceptNotification(notification):
        """Handles a notification object pushed by tiles or the controller."""
        notification.visit(self)
