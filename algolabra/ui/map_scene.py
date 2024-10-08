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
    def __init__(self, citymap, tilesize=8, scenario_service=None):
        super().__init__()
        self.citymap = citymap
        self.scenario_service = scenario_service
        self.tilesize = tilesize
        self.rectangles = []
        if citymap:
            self.rectangles = [[self.rectify(x, y, ground, self.tilesize) for x, ground in enumerate(line)] for y, line in
                           enumerate(citymap)]
        # self.mark_start_goal()

    def rectify(self, x: int, y: int, ground: str, tilesize: int):
        if ground == '.':
            brush = QBrush(Qt.GlobalColor.green)
        else:
            brush = QBrush(Qt.GlobalColor.red)
        return self.addRect(x * tilesize, y * tilesize, tilesize, tilesize, brush=brush)

    def update_state(self, visited: list[tuple[int, int]], expanded: list[tuple[int, int]]):
        for x,y in visited:
            self.rectangles[y][x].setBrush(QBrush(QColor("yellow")))
        for x,y in expanded:
            self.rectangles[y][x].setBrush(QBrush(QColor('green')))
        # for x, y in pruned:
        #     self.rectangles[y][x].setBrush(QBrush(QColor('red')))

    # def mark_start_goal(self):
    #     # [26,	(187, 480), (256, 404), 104.58073578]
    #     bucket, start, goal, ideal_solution = self.search_service.get_scenario()
    #     x, y = start
    #     for cords,color in zip([start,goal], ['cyan', 'purple']):
    #         x,y = cords
    #         self.rectangles[y][x].setBrush(QBrush(QColor(color)))

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
