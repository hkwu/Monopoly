#!/usr/bin/env python3

############
# Monopoly
# 2015-12-22
# Kelvin Wu
############

from engine import board
from engine import controller
from view import textview

if __name__ == '__main__':
    gameBoard = board.Board('skin/standard.json')
    gameView = textview.TextView()
    gameController = controller.Controller(gameBoard, gameView)
    gameView.register(gameController)
    gameView.play()
