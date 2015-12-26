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
    def visitBD(self, other):
        """Visit method for board."""
        pass

    @abc.abstractmethod
    def visitCT(self, other):
        """Visit method for controller."""
        pass


class BoardRelayNotification(Notification):
    """A notification that is relayed to the controller through the Board."""
    def visitBD(self, other):
        other.relayNotification(self)


class ControllerBoardNotification(Notification):
    """A notification sent from the controller to the Board."""
    def visitCT(self, other):
        pass


class BoardControllerNotification(Notification):
    """A notification sent from the Board to the controller."""
    def visitBD(self, other):
        pass


class TNBuyOpp(BoardRelayNotification):
    """Notification that a player has landed on a purchasable tile."""
    def __init__(self, player, tile):
        self.data = {
            'player': player.pack(),
            'tile': tile.pack()
        }

    def visitCT(self, other):
        other.relayBuyOpp(self.data)


class PNPassGo(BoardRelayNotification):
    """Notification that a player has passed GO."""
    def __init__(self, player):
        self.data = {
            'player': player.pack()
        }

    def visitCT(self, other):
        other.relayPassGo(self.data)


class PNTilePurchase(BoardRelayNotification):
    """Notification that a player has purchased a tile."""
    def __init__(self, player, tile):
        self.data = {
            'player': player.pack(),
            'tile': tile.pack()
        }

    def visitCT(self, other):
        other.relayTilePurchase(self.data)


class PNInsufficientFunds(BoardRelayNotification):
    """Notification that a player has insufficient funds to complete the
    current action."""
    def __init__(self, player, deficit):
        self.data = {
            'player': player.pack(),
            'deficit': deficit
        }

    def visitCT(self, other):
        other.relayInsufficientFunds(self.data)


class PNLiquidate(BoardRelayNotification):
    """Notification that a player must begin liquidating their assets."""
    def __init__(self, player, required):
        self.data = {
            'player': player.pack(),
            'required': required
        }

    def visitCT(self, other):
        other.relayLiquidate(self.data)


class CNPlayerMove(ControllerBoardNotification):
    """Notification that a player is attempting a move."""
    def __init__(self, player, delta):
        self.player = player
        self.delta = delta

    def visitBD(self, other):
        other.playerMove(self.player, self.delta)


class CNPlayerPurchase(ControllerBoardNotification):
    """Notification that a player is attempting to purchase a property."""
    def __init__(self, player):
        self.player = player

    def visitBD(self, other):
        other.playerPurchase(self.player)


class BNPlayerMove(BoardControllerNotification):
    """Notification that player has made a move to a tile."""
    def __init__(self, player, tile):
        self.data = {
            'player': player.pack(),
            'tile': tile.pack()
        }

    def visitCT(self, other):
        other.relayPlayerMove(self.data)
