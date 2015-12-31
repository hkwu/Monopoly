#################
# Monopoly/Engine
# notification.py
# 2015-12-22
# Kelvin Wu
#################

import abc

# notification codes
OUT_OF_MOVES = 'OUT_OF_MOVES'
DICE_ROLL = 'DICE_ROLL'
BUY_OPP = 'BUY_OPP'
PASS_GO = 'PASS_GO'
TILE_PURCHASE = 'TILE_PURCHASE'
INSUFFICIENT_FUNDS = 'INSUFFICIENT_FUNDS'
LIQUIDATE = 'LIQUIDATE'
PLAYER_MOVE = 'PLAYER_MOVE'
RENT_PAID = 'RENT_PAID'

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

    def visitCT(self, other):
        other.notifyView(self.id, self.data)


class ControllerBoardNotification(Notification):
    """A notification sent from the controller to the Board."""
    def visitCT(self, other):
        pass


class BoardControllerNotification(Notification):
    """A notification sent from the Board to the controller."""
    def visitBD(self, other):
        pass

    def visitCT(self, other):
        other.notifyView(self.id, self.data)


class TNBuyOpp(BoardRelayNotification):
    """Notification that a player has landed on a purchasable tile."""
    def __init__(self, player, tile):
        self.id = BUY_OPP
        self.data = {
            'player': player.pack(),
            'tile': tile.pack()
        }


class PNPassGo(BoardRelayNotification):
    """Notification that a player has passed GO."""
    def __init__(self, player):
        self.id = PASS_GO
        self.data = {
            'player': player.pack()
        }


class PNTilePurchase(BoardRelayNotification):
    """Notification that a player has purchased a tile."""
    def __init__(self, player, tile):
        self.id = TILE_PURCHASE
        self.data = {
            'player': player.pack(),
            'tile': tile.pack()
        }


class PNInsufficientFunds(BoardRelayNotification):
    """Notification that a player has insufficient funds to complete the
    current action."""
    def __init__(self, player, deficit):
        self.id = INSUFFICIENT_FUNDS
        self.data = {
            'player': player.pack(),
            'deficit': deficit
        }


class PNLiquidate(BoardRelayNotification):
    """Notification that a player must begin liquidating their assets."""
    def __init__(self, player, required):
        self.id = LIQUIDATE
        self.data = {
            'player': player.pack(),
            'required': required
        }


class PNRentPaid(BoardRelayNotification):
    """Notification that a player has paid rent."""
    def __init__(self, playerRenter, playerLandlord, rent):
        self.id = RENT_PAID
        self.data = {
            'playerRenter': playerRenter.pack(),
            'playerLandlord': playerLandlord.pack(),
            'rent': rent
        }


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
        self.id = PLAYER_MOVE
        self.data = {
            'player': player.pack(),
            'tile': tile.pack()
        }
