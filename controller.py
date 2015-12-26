#################
# Monopoly/Engine
# controller.py
# 2015-12-23
# Kelvin Wu
#################

import notification

class Command(object):
    """Handles the execution of game commands. Performs basic verification of
    command prerequisites."""
    def __init__(self, controller):
        self.controller = controller

    def execute(self, player):
        """Execute the command."""
        pass

    def reset(self):
        """Clears the state of the command for a new turn."""
        pass


class Move(Command):
    """Handles a request to move a player piece."""
    def __init__(self, controller):
        super().__init__(controller)
        self.rollCount = 0
        self.rollAgain = True

    def execute(self, player):
        if not self.rollAgain:
            self.controller.relayOutOfMoves(player)
            return

        self.controller.board.diceRoll()
        delta = self.controller.board.diceSum()
        isDouble = self.controller.board.diceIsDouble()

        if isDouble:
            self.rollCount += 1
            if self.rollCount == 2:
                self.rollAgain = False
        else:
            self.rollAgain = False

        self.controller.relayDiceRoll(self.controller.board.diceA(), 
                                      self.controller.board.diceB(), 
                                      isDouble, self.rollAgain)
        self.controller.board.acceptNotification(notification.CNPlayerMove(player, delta))


    def reset(self):
        self.rollCount = 0
        self.rollAgain = True


class Purchase(Command):
    """Handles a request to purchase a property. Only applies to purchases made
    after landing on a property."""
    def __init__(self, controller):
        super().__init__(controller)

    def execute(self, player):
        self.controller.board.acceptNotification(notification.CNPlayerPurchase(player))

    def reset(self):
        pass


class Controller(object):
    def __init__(self, board, view):
        self._board = board
        self._view = view
        self._board.register(self)

        self._commands = {
            'roll': Move(self),
            'purchase': Purchase(self)
        }

    @property
    def board(self):
        return self._board

    @property
    def view(self):
        return self._view

    def acceptNotification(self, notification):
        """Accepts notification from the Board."""
        notification.visitCT(self)

    def relayDiceRoll(self, diceA, diceB, isDouble, rollAgain):
        """Notify view of the results of a dice roll."""
        data = {
            'diceA': diceA,
            'diceB': diceB,
            'isDouble': isDouble,
            'rollAgain': rollAgain
        }

        self._view.notifyDiceRoll(data)

    def relayOutOfMoves(self, player):
        """Notify view that a player cannot move again."""
        self._view.notifyOutOfMoves(player)

    def relayBuyOpp(self, data):
        """Notify view that player should be prompted for a purchase action
        on tile."""
        self._view.notifyBuyOpp(data)

    def relayPassGo(self, data):
        """Notify view that player has passed GO."""
        self._view.notifyPassGo(data)

    def relayTilePurchase(self, data):
        """Notify view that player has successfully purchased tile."""
        self._view.notifyTilePurchase(data)

    def relayInsufficientFunds(self, data):
        """Notify view that player has insufficient funds to complete an action."""
        self._view.notifyInsufficientFunds(data)

    def relayLiquidate(self, data):
        """Notify view that player must liquidate assets until required cash
        is obtained."""
        self._view.notifyLiquidate(data)

    def relayPlayerMove(self, data):
        """Notify view that a player has changed positions."""
        self._view.notifyPlayerMove(data)

    def playerAdd(self, name, piece):
        """Adds a player to the game."""
        self._board.playerAdd(name, piece)

    def playerMove(self, player):
        """Executes command: moves the player."""
        self._commands['roll'].execute(player)

    def playerPurchase(self, player):
        """Executes command: purchases tile that player is located at."""
        self._commands['purchase'].execute(player)

    def resetCommandState(self):
        """Resets state of all commands."""
        for cmd in self._commands:
            self._commands[cmd].reset()
