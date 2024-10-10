from PyQt6.QtGui import QBrush, QColor, QImage, QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsRectItem
from PyQt6.QtCore import Qt

class MapScene_old(QGraphicsScene):
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


def get_image_from_map(map_data: list, cell_size=10):
        image = QImage(len(map_data[0]), len(map_data), QImage.Format.Format_MonoLSB)
        image.fill(0)
        # 255, 0, 0 red
        # 34, 139, 34 green
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                if cell == '.':
                    image.setPixel(x, y, 1)
        return image.scaled(len(map_data) * cell_size, len(map_data[0]) * cell_size)

def paint_cell(x, y, cell_size, color, image):
    # käytän tätä ehkä myöhemmin
    # tarviiko tota cell sizea vai voinko vaan zoomata viewissä?
    for i in range(cell_size):
        for j in range(cell_size):
            image.setPixel(x * cell_size + i, y * cell_size + j, color.rgb())


if __name__=='__main__':
    from PyQt6.QtWidgets import QApplication, QGraphicsView
    import sys
    from read_files import read_map

    app = QApplication(sys.argv)

    # kartta = [['@', '@', '@', '@', '@'], ['@', '@', '.', '.', '.'], ['.', '.', '.', '.', '.']]


    scene = QGraphicsScene()
    pixmap = QPixmap.fromImage(get_image_from_map(read_map("Boston_0_512.map")))
    scene.addPixmap(pixmap)


    # tilesize = 8

    view = QGraphicsView(scene)
    view.setWindowTitle("map_scene")
    view.resize(640, 480)
    view.show()

    sys.exit(app.exec())
