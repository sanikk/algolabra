from decimal import Decimal
from multiprocessing.process import parent_process

from PyQt6.QtCore import pyqtSlot, Qt, QRectF
from PyQt6.QtGui import QColor, QImage, QPixmap, QBrush, QPen, QPainter
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem


class MapScene(QGraphicsScene):
    def __init__(self, scenario_service=None, search_service=None):
        super().__init__()
        self.scenario_service = scenario_service
        self.search_service = search_service
        self.pixmap = None
        self.paintable_layer = PaintableLayer()
        self.addItem(self.paintable_layer)
        scenario_service.map_changed.connect(self.map_changed)

    def get_image_from_map(self, map_data: list):
        image = QImage(len(map_data[0]), len(map_data), QImage.Format.Format_RGB32)
        image.fill(QColor(0, 0, 0))
        [[image.setPixelColor(x, y, QColor(255, 255, 255)) for x, cell in enumerate(row) if cell=="."] for y, row in enumerate(map_data)]
        return image

    @pyqtSlot()
    def map_changed(self):
        self.clear()
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
        # these are stylized so they can still be seen later
        x, y = start
        self.addRect(max(0, x - 1), y, 3, 1, pen=QPen(QColor(56, 194, 180)))
        self.addRect(x, max(0, y - 1), 1, 3, pen=QPen(QColor(56, 194, 180)))
        x, y = goal
        self.addRect(max(0, x - 1), y, 3, 1, pen=QPen(QColor(245, 34, 213)))
        self.addRect(x, max(0, y - 1), 1, 3, pen=QPen(QColor(245, 34, 213)))

    def paint_tile_color(self, x, y, red, blue, green):
        self.addRect(x, y, 1, 1, pen=QPen(Qt.PenStyle.NoPen), brush=QBrush(QColor(red, blue, green)))

    # @pyqtSlot(int, int)
    def node_visit(self, x, y):
        self.paint_tile_color(x, y,0, 255, 0)

    # @pyqtSlot(int, int)
    def node_expansion(self, x, y):
        self.paint_tile_color(x, y,0, 0, 255)

    @pyqtSlot(str)
    # TODO fill this in
    def flimit_change(self, new_flimit: str):
        visited, expanded, flimit = self.search_service.get_update()
        all(self.paint_tile_color(x, y, 0, 255, 0) for x, y in visited)
        all(self.paint_tile_color(x, y, 0, 0, 255) for x, y in expanded)

    @pyqtSlot(str, list, list)
    def handle_lists(self, new_flimit: str, visited: list, expanded: list):
        [self.paint_tile_color(x, y, 0, 255, 0) for x, y in visited]
        [self.paint_tile_color(x, y, 0, 0, 255) for x, y in expanded]

    def get_slots(self):
        return self.node_visit, self.node_expansion, self.flimit_change, self.handle_lists


class PaintableLayer(QGraphicsItem):
    def __init__(self, parent=None, size=0, visited=None, expanded=None):
        super().__init__(parent=parent)
        self.visited = visited or []
        self.expanded = expanded or []
        self.size = size

    def boundingRect(self):
        return QRectF(0,0,self.size, self.size)

    def paint(self, painter, option, widget = None):
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        [painter.drawPoint(x, y) for x,y in self.visited]
        painter.setBrush(QBrush(QColor(0, 0, 255)))
        [painter.drawPoint(x, y) for x, y in self.expanded]



if __name__=='__main__':
    pass
