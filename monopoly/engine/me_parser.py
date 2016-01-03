#################
# Monopoly/Engine
# me_parser.py
# 2015-12-22
# Kelvin Wu
#################

import abc
import json

from . import tile


class MonopolyDataParser(abc.ABC):
    """Abstract class for JSON data parsers."""
    def __init__(self, board, dataFile):
        self._board = board
        with open(dataFile) as data:
            self._file = json.load(data)

    @abc.abstractmethod
    def parse(self):
        """Parses the file given to this object and stores the data
        obtained as the object's fields."""
        pass


class MonopolyInitParser(MonopolyDataParser):
    """Parses JSON file that contains tile initialization data."""
    def __init__(self, board, dataFile):
        super().__init__(board, dataFile)
        self.tiles = []

    def parse(self):
        self.style = self._file['style']
        self.currency = self._file['currency']

        for i in self._file['tiles']:
            self.tiles.append(tile.TileFactory.makeTile(self._board, i['name'],
                                                        i['index'], i['type'], 
                                                        i['data']))
