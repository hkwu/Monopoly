#################
# Monopoly/Engine
# tile.py
# 2015-12-22
# Kelvin Wu
#################

import abc
import notification

class TileFactory(object):
    """Class that instantiates members of the Tile hierarchy."""
    @staticmethod
    def makeTile(board, name, tileType, data):
        if tileType == 'basic':
            return BasicTile(name, board)
        elif tileType == 'property':
            return Property(name, board, data['cost'], data['rent'])


class Tile(abc.ABC):
    """Abstract tile class at head of hierarchy."""
    def __init__(self, name, board):
        super().__init__()
        self._name = name
        self._board = board

    @property
    def name(self):
        return self._name

    def pack(self):
        """Returns a dictionary containing the state information of the tile."""
        return {'name': self._name}

    @abc.abstractmethod
    def action(self, player):
        """Called when the player lands on this tile."""
        pass

    def pushNotification(self, notification):
        """Pushes a notification to the board."""
        self._board.acceptNotification(notification)


class BasicTile(Tile):
    """A basic tile that does nothing when the player lands on it."""
    def __init__(self, name, board):
        super().__init__(name, board)

    def action(self, player):
        pass


class OwnableTile(Tile):
    """Represents a tile that can be owned by a player."""
    def __init__(self, name, board, value, owner=None, isOwned=False):
        super().__init__(name, board)
        self._isOwned = isOwned
        self._value = value
        self._owner = owner

    @property
    def isOwned(self):
        return self._isOwned

    @property
    def value(self):
        return self._value

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, owner):
        self._owner = owner

    def pack(self):
        data = super().pack()
        data['isOwned'] = self._isOwned
        data['value'] = self._value
        data['owned'] = self._owner.name if self._owner else 'unowned'
        return data
    
    def action(self, player):
        if self._owner:
            self.charge(player)
        else:
            self.pushNotification(notification.TNBuyOpp(player, self))

    @abc.abstractmethod
    def charge(self, player):
        """Charges the player that lands on this tile."""
        pass


class Property(OwnableTile):
    """A tile that represents a property that charges rent."""
    def __init__(self, name, board, value, rent, owner=None, isOwned=False, level=0):
        super().__init__(name, board, value, owner, isOwned)
        self._rent = rent
        self._improvementLevel = level

    @property
    def rent(self):
        return self._rent[self._improvementLevel]

    def pack(self):
        data = super().pack()
        data['rent'] = self.rent
        data['improvementLevel'] = self._improvementLevel
        return data

    def charge(self, player):
        player.payRent(self._owner, self._value)


# TODO
class Utility(OwnableTile):
    """A tile that charges players according to a random die roll."""
    def __init__(self, name, board, value, owner=None, isOwned=False):
        super().__init__(name, board, value, owner, isOwned)
    
    def charge(self, player):
        pass