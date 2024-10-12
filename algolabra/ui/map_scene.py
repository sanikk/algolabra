from decimal import Decimal

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QColor, QImage, QPixmap, QBrush
from PyQt6.QtWidgets import QGraphicsScene


class MapScene(QGraphicsScene):
    def __init__(self, scenario_service=None, search_service=None, tile_size=10):
        super().__init__()
        self.tile_size = tile_size
        self.scenario_service = scenario_service
        self.search_service = search_service
        self.pixmap = None
        scenario_service.map_changed.connect(self.map_changed)

    def get_image_from_map(self, map_data: list):
        image = QImage(len(map_data[0]), len(map_data), QImage.Format.Format_RGB32)
        image.fill(QColor(0, 0, 0))

        [[image.setPixelColor(x, y, QColor(255, 255, 255)) for x, cell in enumerate(row) if cell=="."] for y, row in enumerate(map_data)]

        return image.scaled(len(map_data) * self.tile_size, len(map_data[0]) * self.tile_size)

    @pyqtSlot()
    def map_changed(self):
        map_data = self.scenario_service.get_map_data()
        if not map_data:
            return
        self.pixmap = QPixmap.fromImage(self.get_image_from_map(map_data))
        self.addPixmap(self.pixmap)

    @pyqtSlot(int, int)
    def scenario_changed(self, bucket, index):
        self.clear()
        if self.pixmap:
            self.addPixmap(self.pixmap)
        if bucket is None or index is None or index == -1:
            return
        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, index)
        self.fill_start_goal(start, goal)

    def fill_start_goal(self, start, goal):
        x, y = start
        self.addRect(max(0, x - 1) * self.tile_size, y * self.tile_size, 3 * self.tile_size, self.tile_size, brush=QBrush(QColor(56, 194, 180)))
        self.addRect(x * self.tile_size, max(0, y - 1) * self.tile_size, self.tile_size, 3 * self.tile_size, brush=QBrush(QColor(56, 194, 180)))
        x, y = goal
        self.addRect(max(0, x - 1) * self.tile_size, y * self.tile_size, 3 * self.tile_size, self.tile_size,
                     brush=QBrush(QColor(245, 34, 213)))
        self.addRect(x * self.tile_size, max(0, y - 1) * self.tile_size, self.tile_size, 3 * self.tile_size,
                     brush=QBrush(QColor(245, 34, 213)))

    def paint_tile_color(self, x, y, red, blue, green):
        self.addRect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size, brush=QBrush(QColor(red, blue, green)))

    def paint_tile_brush(self, x, y, brush):
        self.addRect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size, brush=brush)

    @pyqtSlot(int, int)
    def node_visit(self, x, y):
        self.paint_tile_color(x, y,0, 255, 0)

    @pyqtSlot(int, int)
    def node_expansion(self, x, y):
        self.paint_tile_color(x, y,0, 0, 255)

    @pyqtSlot(Decimal)
    # TODO fill this in
    def flimit_change(self, new_flimit):
        pass

    def get_slots(self):
        return self.node_visit, self.node_expansion, self.flimit_change

if __name__=='__main__':
    pass
