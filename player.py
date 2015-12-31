#################
# Monopoly/Engine
# player.py
# 2015-12-22
# Kelvin Wu
#################

import notification


class Player(object):
    """Class to store player state data."""
    def __init__(self, name, piece, pos, board, cash):
        self._name = name
        self._piece = piece
        self._pos = pos
        self._board = board
        self._cash = cash
        self._properties = []

    @property
    def name(self):
        return self._name

    @property
    def piece(self):
        return self._piece

    @property
    def pos(self):
        return self._pos

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, val):
        self._cash = val

    @property
    def properties(self):
        return self._properties

    def pack(self):
        """Returns a dictionary containing the state information of the player."""
        data = {
            'name': self._name,
            'piece': self._piece,
            'pos': self._pos,
            'cash': self._cash,
            'properties': []
        }

        for i in self._properties:
            data['properties'].append({'name': i.name, 'value': i.value})

        return data

    def move(self, delta):
        """Moves player delta tiles from current position."""
        newPos = (self._pos + delta) % self._board.size
        # check for Pass GO condition
        if delta > 0 and newPos < self._pos:
            self._board.acceptNotification(notification.PNPassGo(self))

        self._pos = newPos
        self._board.acceptNotification(notification.PNPlayerMove(self))

    def payRent(self, player, amount):
        """Pays the required rent to the other player. Sends a notification
        when the debt is too high."""
        if player.name == self._name:
            return
        elif self._cash - amount < 0:
            self._board.acceptNotification(notification.PNLiquidate(self, player, 
                                                                    self.cash + amount))
        else:
            self._cash -= amount
            player.cash += amount
            self._board.acceptNotification(notification.PNRentPaid(self, player, amount))

    def purchase(self, tile):
        """Purchases the tile given."""
        if tile.value <= self._cash:
            self._cash -= tile.value
            tile.owner = self
            self._board.acceptNotification(notification.PNTilePurchase(self, tile))
        else:
            self._board.acceptNotification(notification.PNInsufficientFunds(self, tile.value - self._cash))
