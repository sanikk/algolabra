from PyQt6.QtGui import QBrush
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtCore import Qt

from algolabra.scenarios.map_component import read_map


class MapScene(QGraphicsScene):
    """
    whole map
    """
    def __init__(self, map_path, tilesize=8):
        super().__init__()
        # nämä on varmasti muutenkin scenessä tallessa, katon kohta
        self.rectangles = self.map_to_grid(read_map(map_path), tilesize)

    def rectify(self, x: int, y: int, ground: str, tilesize: int):
        if ground == '.':
            brush = QBrush(Qt.GlobalColor.green)
        else:
            brush = QBrush(Qt.GlobalColor.red)
        return self.addRect(x * tilesize, y * tilesize, tilesize, tilesize, brush=brush)

    def map_to_grid(self, citymap, tilesize):
        self.rectangles = [[self.rectify(x,y,ground,tilesize) for x, ground in enumerate(line)] for y, line in enumerate(citymap)]
        return self.rectangles
