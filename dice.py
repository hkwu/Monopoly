#################
# Monopoly/Engine
# dice.py
# 12-22-2015
# Kelvin Wu
#################

import random

class Dice(object):
    """An object representing two fair dice."""
    def __init__(self):
        self.a = 6
        self.b = 6

    def roll(self):
        """Re-rolls the dice."""
        self.a = random.randrange(6) + 1
        self.b = random.randrange(6) + 1

    def sum(self):
        """Returns sum of the two dice."""
        return self.a + self.b

    def isDouble(self):
        """Returns true if both dice show the face."""
        return self.a == self.b
