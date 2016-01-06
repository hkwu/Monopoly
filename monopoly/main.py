#!/usr/bin/env python3

############
# Monopoly
# 2015-12-22
# Kelvin Wu
############

import argparse

from engine import board
from engine import controller
from view import textview

if __name__ == '__main__':
    mparser = argparse.ArgumentParser()
    mparser.add_argument("--skin", help=("provide the name of a JSON file to "
                                         "customize the board's theme"),
                         default='standard')
    args = mparser.parse_args()

    # exception is thrown if file doesn't exist
    gameBoard = board.Board('skin/' + args.skin + '.json')
    gameView = textview.TextView()
    gameController = controller.Controller(gameBoard, gameView)
    gameView.register(gameController)
    gameView.play()
