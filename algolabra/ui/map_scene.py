from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsRectItem
from PyQt6.QtCore import Qt

from algolabra.scenarios.map_component import read_map
# from map_component import read_map

class MapViewTab:
    pass

class MapScene(QGraphicsScene):
    """
    whole map
    """
    # def __init__(self, search_service=None, tilesize=8):
    def __init__(self, citymap, tilesize=8):
        super().__init__()
        self.citymap = citymap
        # self.search_service = search_service
        self.tilesize = tilesize
        # self.rectangles = []
        self.rectangles = [[self.rectify(x, y, ground, self.tilesize) for x, ground in enumerate(line)] for y, line in
                           enumerate(citymap)]


    def read_map(self):
        pass
        # self.rectangles = self.search_service.get_citymap(self.tilesize)

    def rectify(self, x: int, y: int, ground: str, tilesize: int):
        if ground == '.':
            brush = QBrush(Qt.GlobalColor.green)
        else:
            brush = QBrush(Qt.GlobalColor.red)
        return self.addRect(x * tilesize, y * tilesize, tilesize, tilesize, brush=brush)

    # rectangles = [[self.rectify(x, y, ground, self.tilesize) for x, ground in enumerate(line)] for y, line in
    #                       enumerate(citymap)]


    def update_state(self, visited: list[tuple[int, int]], expanded: list[tuple[int, int]]):
        for x,y in visited:
            self.rectangles[y][x].setBrush(QBrush(QColor("yellow")))


if __name__=='__main__':
    from PyQt6.QtWidgets import QApplication, QGraphicsView
    import sys

    app = QApplication(sys.argv)

    # kartta = [['@', '@', '@', '@', '@'], ['@', '@', '.', '.', '.'], ['.', '.', '.', '.', '.']]

    scene = MapScene("Boston_0_512.map")
    # rects = scene.map_to_grid(kartta)

    # tilesize = 8

    view = QGraphicsView(scene)
    view.setWindowTitle("map_scene")
    view.resize(640, 480)
    view.show()

    sys.exit(app.exec())


