# Monopoly
A project based on a class assignment. The goal is to implement the logic of Monopoly using the MVC pattern.

## Implemented Features
This is a list of features that are currently available.
* Rolling dice
* Moving around the board
* Buying properties
* Paying rent

## Views
By decoupling the player interface from the model, it is possible to implement different views without modifying the engine. View implementations are stored in `monopoly/view`.
* Minimal Textview

## Skins
The look and feel of the game board can be modified through the use of different JSON files stored in `monopoly/skin`. This provides an additional degree of customization to the player.
* US Standard Edition (2008)
