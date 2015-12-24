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

        self.controller.board.dice.roll()

        # if self._controller.board.dice.isDouble() and self._rollCount == 2:
        #     self._controller.board.acceptNotification(CNJailPlayer(player))
        #     self._controller.view.notifyPlayerJailed(player)

        delta = self.controller.board.dice.sum()
        self.controller.board.acceptNotification(notification.CNPlayerMove(player, delta))
        print("sum is {}, doubles is {}".format(delta, self.controller.board.dice.isDouble()))

        if self.controller.board.dice.isDouble():
            self.rollCount += 1
            if self.rollCount == 2:
                self.rollAgain = False
        else:
            self.rollAgain = False


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

    def relayOutOfMoves(self, player):
        """Notify view that a player cannot move again."""
        self._view.notifyOutOfMoves(player)

    def relayBuyOpp(self, tile, player):
        """Notify view that player should be prompted for a purchase action
        on tile."""
        self._view.notifyBuyOpp(tile, player)

    def relayPassGo(self, player):
        """Notify view that player has passed GO."""
        self._view.notifyPassGo(player)

    def relayTilePurchase(self, player, tile):
        """Notify view that player has successfully purchased tile."""
        self._view.notifyTilePurchase(player, tile)

    def relayInsufficientFunds(self, player, deficit):
        """Notify view that player has insufficient funds to complete an action."""
        self._view.notifyInsufficientFunds(player, deficit)

    def relayLiquidate(self, player, required):
        """Notify view that player must liquidate assets until required cash
        is obtained."""
        self._view.notifyLiquidate(player, required)

    def relayAlreadyOwned(self, player, tile):
        """Notify view that a player is attempting to purchase an owned property."""
        self._view.notifyAlreadyOwned(player, tile)

    def relayPlayerMove(self, player, tile):
        """Notify view that a player has changed positions."""
        self._view.notifyPlayerMove(player, tile)

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
