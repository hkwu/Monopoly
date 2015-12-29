###############
# Monopoly/View
# textview.py
# 2015-12-23
# Kelvin Wu
###############

import cmd

class PlayerRep(object):
    def __init__(self, name, piece, pos, cash=1500, properties=None):
        self.name = name
        self.piece = piece
        self.pos = pos
        self.cash = cash
        self.properties = properties if properties else []


class TileRep(object):
    def __init__(self, name, pos):
        self.name = name
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

        print("\nIt's {}'s turn.".format(self.view.players[self.turn].name))

    def postcmd(self, stop, line):
        if line == 'quit':
            print("Thanks for playing!")
            raise SystemExit

        print("\nIt's {}'s turn.".format(self.view.players[self.turn].name))

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
        self.view.controller.resetCommandState()

    def do_players(self, arg):
        """Prints the player data for each player in the game."""
        for player in self.view.players:
            print("{} [{}]: located at {}. Money: {}{}.".format(player.name, player.pos,
                                                                self.view.tiles[player.pos].name,
                                                                self.view.currency['symbol'],
                                                                player.cash))
            if player.properties:
                print("Properties owned:")
                for prop in player.properties:
                    print(prop)
            else:
                print("No owned properties.")

    def _playerOnTile(self, tiles):
        """Takes a list of tiles. Goes through the list and prints the tile names 
        in a column along with any players that are on those tiles."""
        width = 0
        for tile in tiles:
            displayWidth = len(tile.name)
            if displayWidth > width:
                width = displayWidth

        print("{:2} {:{}} Players\n"
              "== {:{}} {}".format("ID", "Location", width + 1, '=' * len("Location"), 
                                   width + 1, '=' * len("Players")))
        for tile in tiles:
            present = []
            for player in self.view.players:
                if player.pos == tile.pos:
                    present.append(player.name)

            msg = "{:02} {:{}}".format(tile.pos, tile.name, width + 1)
            if present:
                print(msg, "{}".format(", ".join(present)), sep=" ")
            else:
                print(msg)

    def do_look(self, arg):
        """Prints tile information for <n> tiles around your player, up to a 
        maximum of 5 tiles on each side. Defaults to 1 if no argument is provided."""
        if not arg:
            arg = 1

        try:
            if not 0 <= int(arg) <= 5:
                print("Usage: look <n>, 0 <= n <= 5")
            else:
                ppos = self.view.players[self.turn].pos
                if ppos - int(arg) < 0:
                    listTail = self.view.tiles[0:ppos + int(arg) + 1]
                    count = int(arg) - ppos
                    listHead = self.view.tiles[self.view.size - count + 1:self.view.size + 1]
                    self._playerOnTile(listHead + listTail)
                elif ppos + int(arg) + 1 > self.view.size:
                    listHead = self.view.tiles[ppos - int(arg):self.view.size + 1]
                    count = self.view.size - ppos
                    listTail = self.view.tiles[0:int(arg) - count + 1]
                    self._playerOnTile(listHead + listTail)
                else:
                    self._playerOnTile(self.view.tiles[ppos - int(arg):ppos + int(arg) + 1])
        except ValueError:
            print("Usage: look <n>, 0 <= n <= 5")

    def do_quit(self, arg):
        """Quit the game."""
        return True

    def default(self, arg):
        print("Unknown or invalid command: {}.".format(arg))

class TextView(object):
    """Basic text view."""
    def __init__(self):
        self._controller = None
        self._inputHandler = InputHandler(self)
        self._players = []
        self._numPlayers = 0
        
    @property
    def size(self):
        return self._size

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

    @property
    def currency(self):
        return self._currency

    @property
    def tiles(self):
        return self._tiles

    def register(self, controller):
        """Registers the controller with the view."""
        self._controller = controller
        self._size = self._controller.querySize()
        self._style = self._controller.queryStyle()
        self._currency = self._controller.queryCurrency()
        self._tiles = [TileRep(tile['name'], tile['pos']) for tile in self._controller.queryTiles()]

    def notifyDiceRoll(self, data):
        print("Rolled: ({}, {})".format(data['diceA'], data['diceB']))
        if data['isDouble']:
            msg = "Doubles rolled! "
            if data['rollAgain']:
                msg += "You can roll again."
            else:
                msg += "Careful! If you roll doubles again, you'll go to jail!"

            print(msg)

    def notifyOutOfMoves(self, data):
        print("{}, you cannot roll anymore.".format(data['player']['name']))

    def notifyBuyOpp(self, data):
        print("This property is unowned! Purchase it for {}{}?".format(self._currency['symbol'],
                                                                       data['tile']['value']))
        if self._inputHandler.confirmAction():
            self._controller.playerPurchase(data['player']['name'])
        else:
            print("Auction (unimplemented).")

    def notifyPassGo(self, data):
        print("{} has passed GO! Collected {}200.".format(data['player']['name'],
                                                          self._currency['symbol']))
        for player in self._players:
            if player.name == data['player']['name']:
                player.cash += 200
                break

    def notifyTilePurchase(self, data):
        print("{} has purchased {}. Congratulations!".format(data['player']['name'], 
                                                             data['tile']['name']))
        for player in self._players:
            if player.name == data['player']['name']:
                player.cash -= data['tile']['value']
                player.properties.append(data['tile']['name'])
                break

    def notifyInsufficientFunds(self, data):
        print("{} has insufficient funds to do this. Short: {}{}.".format(self._currency['symbol'],
                                                                          data['player']['name'], 
                                                                          data['deficit']))

    def notifyLiquidate(self, data):
        print("{} must sell assets until they obtain {}{}.".format(self._currency['symbol'],
                                                                   data['player']['name'], 
                                                                   data['required']))

    def notifyPlayerMove(self, data):
        print("{} has moved to {}.".format(data['player']['name'], data['tile']['name']))
        for player in self._players:
            if player.name == data['player']['name']:
                player.pos = data['player']['pos']
                break

    def notifyRentPaid(self, data):
        print("{} has paid {}{} to {}.".format(data['playerRenter']['name'],
                                               self._currency['symbol'], data['rent'],
                                               data['playerLandlord']['name']))
        for player in self._players:
            if player.name == data['player']['name']:
                player.cash -= data['rent']
                break

    def play(self):
        self._inputHandler.cmdloop()
