# Monopoly
A project based on a class assignment originally done in C++. The goal is to implement the logic of Monopoly using the MVC pattern.

## Quick Start
To start a game, navigate to the `monopoly` folder and run `main.py` through your command line, using one of the following commands:
* `$ ./main.py`
* `$ python main.py`

This project was implemented and tested using Python 3. Backwards compatibility with Python 2 is not guaranteed.

### Options
The following command-line options are supported:
* `--skin=SKIN` Specify the board's appearance. Given value must be the name of a JSON file located in `monopoly/skin`. Provide only the name of the file.

## Project Overview
### Implemented Features
This is a list of features that are currently available.
* Rolling dice
* Moving around the board
* Buying properties
* Paying rent

### Views
By decoupling the player interface from the model, it is possible to implement different views without modifying the engine. View implementations are stored in `monopoly/view`.
* Minimal Textview

### Skins
The look and feel of the game board can be modified through the use of different JSON files stored in `monopoly/skin`. This provides an additional degree of customization to the player.
* US Standard Edition (2008)

## Notification Model
The Monopoly engine implements its own `Notification` class to handle communications between each of the application components. In particular, each `Notification` object can store a package of data in one of its fields. Each package of data is constructed using methods attached to certain Model classes such as `Tile` and `Player`.

All `Notification` objects overwrite two base abstract methods to implement the Visitor Pattern: one to visit the `Board` and another to visit the `Controller`. The structure of the data passed by certain `Notification` objects is illustrated below.

### `TNBuyOpp`
````
data = {
    'player': player.pack(),
    'tile': tile.pack()
}
````

### `PNRentPaid`
````
data = {
    'playerA': playerA.pack(),
    'playerB': playerB.pack(),
    'rent': rent
}
````

In the above code segments, `player.pack()` and `tile.pack()` represent a dictionary returned by the `pack()` method of each respective object. For instance, the `Tile` class's `pack()` method returns a dictionary containing state data for a `Tile` object:

````
{
    'name': 'Water Works',
    'pos': 28,
    'isOwned': False,
    'value': 150,
    'owner': None,
    'mortgaged': False
}
````
