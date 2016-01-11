# Monopoly
A project based on a class assignment. The goal is to implement the logic of Monopoly using the MVC pattern.

## Quick Start
To start a game, navigate to the `monopoly` folder and run `main.py` through your command line, using one of the following commands:
* `$ ./main.py`
* `$ python main.py`

This project was implemented and tested using Python 3. Backwards compatibility with Python 2 is not guaranteed.

### Options
The following command-line options are supported:
* `[--skin SKIN]` Specify the board's appearance. Given value must be the name of a JSON file located in `monopoly/skin`. Provide only the name of the file.

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
