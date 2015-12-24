###############
# Monopoly/View
# textview.py
# 2015-12-23
# Kelvin Wu
###############

class PlayerRep(object):
    def __init__(self, name, piece, pos):
        self.name = name
        self.piece = piece
        self.pos = pos

class TextView(object):
    """Basic text view."""
    def __init__(self):
        self._style = ''
        self._players = []
        self._numPlayers = 0
        self._controller = None

    def register(self, controller):
        """Registers the controller with the view."""
        self._controller = controller

    def notifyOutOfMoves(self, player):
        print("{}, you cannot roll anymore.".format(player))

    def notifyBuyOpp(self, tile, player):
        print("{} has landed on {}. It is unowned. Purchase possible.".format(tile, player))

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
        print("{} has moved to {}!".format(player, tile))

    def initialize(self):
        print("You are playing Monopoly!\n"
              "Style: {}\n"
              "Begin game?".format(self._style))

        proceed = input("> ")
        while proceed not in ['y', 'yes', 'n', 'no']:
            print("Try again.")

        if proceed in ['n', 'no']:
            raise SystemExit

        print("Enter the number of players (> 1).")
        while True:
            num = input("> ")
            try:
                num = int(num)
                self._numPlayers = num
            except ValueError:
                print("Try again.")
                continue

            break

        for i in range(self._numPlayers):
            name = input("Name? ")
            piece = input("Piece? ")
            self._players.append(PlayerRep(name, piece, 0))
            self._controller.notifyAddPlayer(name, piece)

    def play(self):
        player = 0
        while self._numPlayers > 1:
            print("It's {}'s turn.".format(self._players[player].name))
            command = input("> ")
            if command == 'roll':
                self._controller.playerMove(self._players[player].name)
            elif command == 'purchase':
                self._controller.playerPurchase(self._players[player].name)
            elif command == 'next':
                player = (player + 1) % self._numPlayers
                self._controller.resetCommandState()
