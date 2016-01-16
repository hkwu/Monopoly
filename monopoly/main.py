#!/usr/bin/env python3

############
# Monopoly
# 2015-12-22
# Kelvin Wu
############

import argparse
import importlib

from engine import board
from engine import controller

VIEWS = {'textview_min'}

if __name__ == '__main__':
    mparser = argparse.ArgumentParser()
    mparser.add_argument('--skin', help=("provide the name of a JSON file to "
                                         "customize the board's theme"),
                         default='standard')
    mparser.add_argument('--view', help="enter the name of a view module to use",
                         default='textview_min')
    mparser.add_argument('-d', '--debug', help="enter debug mode", action='store_true')
    args = mparser.parse_args()

    # initialize gameBoard
    gameBoard = None
    try:
        gameBoard = board.Board('skin/' + args.skin + '.json')
    except:
        print("Invalid JSON file: " + args.skin)
        raise SystemExit

    # import appropriate view
    if args.view in VIEWS:
        view = importlib.import_module('view.' + args.view)
        gameView = view.View()
        gameController = controller.Controller(gameBoard, gameView, args.debug)
        gameView.registerController(gameController)
        gameView.play()
    else:
        print("Unable to locate view: " + args.view)
