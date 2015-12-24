###############
# Monopoly/View
# textview.py
# 2015-12-23
# Kelvin Wu
###############

import cmd

class PlayerRep(object):
    def __init__(self, name, piece, pos):
        self.name = name
        self.piece = piece
        self.pos = pos

class InputHandler(cmd.Cmd):
    """Handles the game loop and user input."""
    def __init__(self, view):
        super().__init__()
        self.prompt = "> "
        self.view = view
        self.turn = 0

    def preloop(self):
        print("You are playing Monopoly!\n"
              "Style: {}\n"
              "Begin game?".format(self.view.style))

        if not self.confirmAction():
            raise SystemExit

        print("Enter the number of players (> 1).")
        while True:
            num = input(self.prompt)
            try:
                num = int(num)
                if num <= 1:
                    raise ValueError
                
                self.view.numPlayers = num
            except ValueError:
                print("Try again.")
                continue

            break

        for i in range(self.view.numPlayers):
            print("Player #{}".format(i + 1))
            print("What is your name?")
            name = input(self.prompt)
            print("What piece will you use?")
            piece = input(self.prompt)
            self.view.playerAdd(PlayerRep(name, piece, 0))

        print("It's {}'s turn.".format(self.view.players[self.turn].name))

    def postcmd(self, stop, line):
        if line == 'quit':
            print("Thanks for playing!")
            raise SystemExit

        print("It's {}'s turn.".format(self.view.players[self.turn].name))

    def confirmAction(self, prompt="> ", invalid="Try again."):
        """Returns a yes or no answer from the user using given prompt. User
        is prompted using the given invalid argument if answer is not yes/no."""
        action = input(prompt)
        while action.lower() not in ['y', 'yes', 'n', 'no']:
            print(invalid)
            action = input(prompt)

        return True if action in ['y', 'yes'] else False

    def do_roll(self, arg):
        """Roll the dice and move your player piece."""
        self.view.controller.playerMove(self.view.players[self.turn].name)

    def do_next(self, arg):
        """End your turn."""
        self.turn = (self.turn + 1) % self.view.numPlayers
        self.view._controller.resetCommandState()

    def do_quit(self, arg):
        """Quit the game."""
        return True

    def default(self, arg):
        print("Unknown or invalid command: {}.".format(arg))

class TextView(object):
    """Basic text view."""
    def __init__(self):
        self._style = ''
        self._players = []
        self._numPlayers = 0
        self._controller = None
        self._inputHandler = InputHandler(self)

    @property
    def style(self):
        return self._style
    
    @property
    def players(self):
        return self._players

    def playerAdd(self, player):
        self._players.append(player)
        self._controller.playerAdd(player.name, player.piece)
    
    @property
    def numPlayers(self):
        return self._numPlayers
    
    @numPlayers.setter
    def numPlayers(self, numPlayers):
        self._numPlayers = numPlayers

    @property
    def controller(self):
        return self._controller

    def register(self, controller):
        """Registers the controller with the view."""
        self._controller = controller

    def notifyOutOfMoves(self, player):
        print("{}, you cannot roll anymore.".format(player))

    def notifyBuyOpp(self, player, tile):
        print("This property is unowned! Purchase it?")
        if self._inputHandler.confirmAction():
            self._controller.playerPurchase(player)
        else:
            print("Auction (unimplemented).")

    def notifyPassGo(self, player):
        print("{} has passed GO! Collected $200.".format(player))

    def notifyTilePurchase(self, player, tile):
        print("{} has purchased {}. Congratulations!".format(player, tile))

    def notifyInsufficientFunds(self, player, deficit):
        print("{} has insufficient funds to do this. Short: {}.".format(player, deficit))

    def notifyLiquidate(self, player, required):
        print("{} must sell assets until they obtain {}.".format(player, required))

    def notifyAlreadyOwned(self, player, tile):
        print("{} has attempted to purchase {} again. Not possible!".format(player, tile))

    def notifyPlayerMove(self, player, tile):
        print("{} has moved to {}.".format(player, tile))

    def play(self):
        self._inputHandler.cmdloop()
