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
MORTGAGE = 'MORTGAGE'
NOT_OWNED = 'NOT_OWNED'


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


class ModelViewNotification(Notification):
    """A notification that is relayed from the model to the view."""
    def visitBD(self, other):
        other.relayNotification(self)

    def visitCT(self, other):
        other.notifyView(self.id, self.data)


class ControllerModelNotification(Notification):
    """A notification sent from the controller to the model."""
    def visitCT(self, other):
        pass


class TNBuyOpp(ModelViewNotification):
    """Notification that a player has landed on a purchasable tile."""
    def __init__(self, player, tile):
        self.id = BUY_OPP
        self.data = {
            'player': player.pack(),
            'tile': tile.pack()
        }


class PNPlayerMove(ModelViewNotification):
    """Notification that a player has moved to a new location."""
    def __init__(self, player):
        self._player = player
        self.id = PLAYER_MOVE
        self.data = {
            'player': player.pack()
        }

    def visitBD(self, other):
        tile = other.getTile(self.data['player']['pos'])
        self.data['tile'] = tile.pack()
        other.relayNotification(self)
        tile.action(self._player)


class PNPassGo(ModelViewNotification):
    """Notification that a player has passed GO."""
    def __init__(self, player):
        self.id = PASS_GO
        self.data = {
            'player': player.pack()
        }


class PNTilePurchase(ModelViewNotification):
    """Notification that a player has purchased a tile."""
    def __init__(self, player, tile):
        self.id = TILE_PURCHASE
        self.data = {
            'player': player.pack(),
            'tile': tile.pack()
        }


class PNInsufficientFunds(ModelViewNotification):
    """Notification that a player has insufficient funds to complete the
    current action."""
    def __init__(self, player, deficit):
        self.id = INSUFFICIENT_FUNDS
        self.data = {
            'player': player.pack(),
            'deficit': deficit
        }


class PNLiquidate(ModelViewNotification):
    """Notification that a player must begin liquidating their assets."""
    def __init__(self, player, other, required):
        self.id = LIQUIDATE
        self.data = {
            'player': player.pack(),
            'other': other.pack() if other else {'name': None},
            'required': required
        }


class PNRentPaid(ModelViewNotification):
    """Notification that a player has paid rent."""
    def __init__(self, playerRenter, playerLandlord, rent):
        self.id = RENT_PAID
        self.data = {
            'playerRenter': playerRenter.pack(),
            'playerLandlord': playerLandlord.pack(),
            'rent': rent
        }


class PNMortgage(ModelViewNotification):
    """Notification that a player has mortgaged a property."""
    def __init__(self, player, tile):
        self.id = MORTGAGE
        self.data = {
            'player': player.pack(),
            'tile': tile.pack()
        }


class PNNotOwned(ModelViewNotification):
    """Notification that a player is attempting to perform an action on a tile
    they do not own."""
    def __init__(self, player, tile):
        self.id = NOT_OWNED
        self.data = {
            'player': player.pack(),
            'tile': tile.pack()
        }


class CNPlayerMove(ControllerModelNotification):
    """Notification that a player is attempting a move."""
    def __init__(self, player, delta):
        self.player = player
        self.delta = delta

    def visitBD(self, other):
        other.playerMove(self.player, self.delta)


class CNPlayerPurchase(ControllerModelNotification):
    """Notification that a player is attempting to purchase a property."""
    def __init__(self, player):
        self.player = player

    def visitBD(self, other):
        other.playerPurchase(self.player)


class CNPlayerMortgage(ControllerModelNotification):
    """Notification that a player is attempting to mortgage a property."""
    def __init__(self, player, tile):
        self.player = player
        self.tile = tile

    def visitBD(self, other):
        other.playerMortgage(self.player, self.tile)
