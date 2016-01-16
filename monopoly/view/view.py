###############
# Monopoly/View
# view.py
# 2016-01-15
# Kelvin Wu
###############

import abc


class MonopolyView(abc.ABC):
    """Abstract view class. Defines interface methods for receiving communication
    from the controller."""
    def __init__(self):
        self._controller = None

    def registerController(self, controller):
        self._controller = controller

    @abc.abstractmethod
    def notifyOutOfMoves(self, data):
        pass

    @abc.abstractmethod
    def notifyDiceRoll(self, data):
        pass

    @abc.abstractmethod
    def notifyBuyOpp(self, data):
        pass

    @abc.abstractmethod
    def notifyPassGo(self, data):
        pass

    @abc.abstractmethod
    def notifyTilePurchase(self, data):
        pass

    @abc.abstractmethod
    def notifyInsufficientFunds(self, data):
        pass

    @abc.abstractmethod
    def notifyLiquidate(self, data):
        pass

    @abc.abstractmethod
    def notifyPlayerMove(self, data):
        pass

    @abc.abstractmethod
    def notifyRentPaid(self, data):
        pass

    @abc.abstractmethod
    def notifyMortgage(self, data):
        pass

    @abc.abstractmethod
    def notifyNotOwned(self, data):
        pass
