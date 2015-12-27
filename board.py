#################
# Monopoly/Engine
# board.py
# 2015-12-10
# Kelvin Wu
#################

import dice
import notification
import data_parser
import player
import tile

class Board(object):
    """Handles state information for the board."""
    def __init__(self, dataFile):
        dataObject = data_parser.MonopolyInitParser(self, dataFile)
        dataObject.parse()
        self._subscriber = None
        self._size = 40
        self._style = dataObject.style
        self._currency = dataObject.currency
        self._tiles = dataObject.tiles
        self._dice = dice.Dice()
        self._players = []

    @property
    def size(self):
        return self._size

    @property
    def style(self):
        return self._style

    @property
    def currency(self):
        # return a copy so Board's data isn't tampered with
        return self._currency.copy()

    def diceA(self):
        """Gets the value of the first die."""
        return self._dice.a

    def diceB(self):
        """Gets the value of the second die."""
        return self._dice.b

    def diceRoll(self):
        self._dice.roll()

    def diceSum(self):
        return self._dice.sum()

    def diceIsDouble(self):
        return self._dice.isDouble()

    def register(self, observer):
        """Registers a subscriber with the board. Replaces existing subscriber."""
        self._subscriber = observer

    def acceptNotification(self, notification):
        """Handles a notification object pushed by model components or the 
        controller."""
        notification.visitBD(self)

    def relayNotification(self, notification):
        """Passes the given notification on to the subscriber."""
        self._subscriber.acceptNotification(notification)

    def playerAdd(self, name, piece, pos=0, cash=None):
        """Adds a player to the game."""
        if cash == None:
            self._players.append(player.Player(name, piece, pos, self, self._currency['defaultAmount']))
        else:
            self._players.append(player.Player(name, piece, pos, self, cash))

    def playerMove(self, player, delta):
        """Moves a player delta spaces."""
        for i in self._players:
            if i.name == player:
                i.move(delta)
                tile = self._tiles[i.pos]
                self._subscriber.acceptNotification(notification.BNPlayerMove(i, tile))
                tile.action(i)
                break

    def playerPurchase(self, player):
        """Purchases the tile that player is standing on."""
        for i in self._players:
            if i.name == player:
                i.purchase(self._tiles[i.pos])
                break
