#################
# Monopoly/Engine
# controller.py
# 2015-12-23
# Kelvin Wu
#################

from . import notification


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
            self.controller.notifyView(notification.OUT_OF_MOVES, {'player': {'name': player}})
            return

        self.controller.board.diceRoll()
        delta = self.controller.board.diceSum()
        isDouble = self.controller.board.diceIsDouble()

        if isDouble:
            if self.rollCount == 2:
                self.rollAgain = False

            self.rollCount += 1
        else:
            self.rollAgain = False

        data = {
            'diceA': self.controller.board.diceA(),
            'diceB': self.controller.board.diceB(),
            'isDouble': isDouble,
            'rollAgain': self.rollAgain
        }

        self.controller.notifyView(notification.DICE_ROLL, data)
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


class Mortgage(Command):
    """Handles a request to mortgage a property."""
    def __init__(self, controller):
        super().__init__(controller)

    def execute(self, player, tile):
        self.controller.board.acceptNotification(notification.CNPlayerMortgage(player, tile))

    def reset(self):
        pass


class Controller(object):
    def __init__(self, board, view):
        self._board = board
        self._view = view
        self._viewNotifications = {
            notification.OUT_OF_MOVES: self._view.notifyOutOfMoves,
            notification.DICE_ROLL: self._view.notifyDiceRoll,
            notification.BUY_OPP: self._view.notifyBuyOpp,
            notification.PASS_GO: self._view.notifyPassGo,
            notification.TILE_PURCHASE: self._view.notifyTilePurchase,
            notification.INSUFFICIENT_FUNDS: self._view.notifyInsufficientFunds,
            notification.LIQUIDATE: self._view.notifyLiquidate,
            notification.PLAYER_MOVE: self._view.notifyPlayerMove,
            notification.RENT_PAID: self._view.notifyRentPaid,
            notification.MORTGAGE: self._view.notifyMortgage,
            notification.NOT_OWNED: self._view.notifyNotOwned
        }
        self._commands = {
            'roll': Move(self),
            'purchase': Purchase(self)
        }

        self._board.register(self)

    @property
    def board(self):
        return self._board

    @property
    def view(self):
        return self._view

    def acceptNotification(self, notification):
        """Accepts notification from the Board."""
        notification.visitCT(self)

    def notifyView(self, code, data):
        """Sends a notification package to the view. Takes in code that identifies
        what kind of notification is being sent."""
        self._viewNotifications[code](data)

    def querySize(self):
        """Returns the size of the game board."""
        return self._board.size

    def queryStyle(self):
        """Returns the style of the game board."""
        return self._board.style

    def queryCurrency(self):
        """Returns currency data for the current game."""
        return self._board.currency

    def queryTiles(self):
        """Returns a list of tile data for each tile in the board, structured
        according to the pack() method of each tile. The tiles are ordered from
        least to greatest index."""
        return self._board.tiles

    def playerAdd(self, name, piece):
        """Adds a player to the game."""
        self._board.playerAdd(name, piece)

    def playerMove(self, player):
        """Executes command: moves the player."""
        self._commands['roll'].execute(player)

    def playerPurchase(self, player):
        """Executes command: purchases tile that player is located at."""
        self._commands['purchase'].execute(player)

    def playerMortgage(self, player, tile):
        """Executes command: mortgages tile given."""
        self._commands['mortgage'].execute(player, tile)

    def playerBankrupt(self, player, other):
        """Removes a player from the game."""
        self._board.playerBankrupt(player, other)

    def resetCommandState(self):
        """Resets state of all commands."""
        for cmd in self._commands:
            self._commands[cmd].reset()

    # DEBUG
    def playerMoveP(self, player, num):
        data = {
            'diceA': num / 2,
            'diceB': num / 2,
            'isDouble': False,
            'rollAgain': False
        }

        self.notifyView(notification.DICE_ROLL, data)
        self._board.acceptNotification(notification.CNPlayerMove(player, num))
