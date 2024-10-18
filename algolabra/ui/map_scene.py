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
        # TODO make this clear paintable layer right.
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

        self.paintable_layer = PaintableLayer(size=self.scenario_service.get_map_size())
        self.addItem(self.paintable_layer)
        if bucket is None or index is None or index == -1:
            return
        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, index)
        self.fill_start_goal(start, goal)

    def paint_tile_color(self, x, y, red, blue, green):
        self.addRect(x, y, 1, 1, pen=QPen(Qt.PenStyle.NoPen), brush=QBrush(QColor(red, blue, green)))

    @pyqtSlot(int, int)
    def node_visit(self, x, y):
        # self.paint_tile_color(x, y,0, 255, 0)
        self.paintable_layer.node_visit(x, y)

    @pyqtSlot(int, int)
    def node_expansion(self, x, y):
        # self.paint_tile_color(x, y,0, 0, 255)
        self.paintable_layer.node_expand(x, y)

    @pyqtSlot(str)
    # TODO fill this in
    def flimit_change(self, new_flimit: str):
        visited, expanded, flimit = self.search_service.get_update()

        all(self.paint_tile_color(x, y, 0, 255, 0) for x, y in visited)
        all(self.paint_tile_color(x, y, 0, 0, 255) for x, y in expanded)

    @pyqtSlot(str, list, list)
    def handle_lists(self, new_flimit: str, visited: list, expanded: list):
        # TODO aw heck no. this does not work at all. send 3 numbers: visited, expanded, flimit. join thread at end.
        # [self.paint_tile_color(x, y, 0, 255, 0) for x, y in visited]
        # [self.paint_tile_color(x, y, 0, 0, 255) for x, y in expanded]
        self.paintable_layer.list_visit(visited)
        self.paintable_layer.list_expand(expanded)

    def get_slots(self):
        return self.node_visit, self.node_expansion, self.flimit_change, self.handle_lists

    def fill_start_goal(self, start, goal):
        if self.paintable_layer:
            self.paintable_layer.fill_start_goal(start, goal)


class PaintableLayer(QGraphicsItem):
    def __init__(self, parent=None, size=0, visited=None, expanded=None, start=None, goal=None):
        super().__init__(parent=parent)
        self.visited = visited or []
        self.expanded = expanded or []
        self.start = start
        self.goal = goal
        self.size = size

    def boundingRect(self):
        return QRectF(0,0,self.size, self.size)

    def paint(self, painter, option, widget = None):
        # print("paint called")
        if self.start and self.goal:
            painter.setBrush(QBrush(QColor(56, 194, 180)))
            painter.drawRect(max(0, self.start[0] - 1), self.start[1], 3, 1)
            painter.drawRect(self.start[0], max(0, self.start[1] - 1), 1, 3)
            painter.setBrush(QBrush(QColor(245, 34, 213)))
            painter.drawRect(max(0, self.goal[0] - 1), self.goal[1], 3, 1)
            painter.drawRect(self.goal[0], max(0, self.goal[1] - 1), 1, 3)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        # painter.drawRects([(*coords, 1, 1) for coords in self.visited])
        # [painter.drawPoint(x, y) for x,y in self.visited]
        [painter.drawRect(x, y, 1, 1) for x, y in self.expanded]
        painter.setBrush(QBrush(QColor(0, 0, 255)))
        # [painter.drawPoint(x, y) for x, y in self.expanded]
        [painter.drawRect(x, y, 1, 1) for x, y in self.expanded]

    def node_visit(self, x, y):
        self.visited.append((x, y))
        self.update()

    def node_expand(self, x, y):
        self.expanded.append((x, y))
        self.update()

    def fill_start_goal(self, start, goal):
        # these are stylized so they can still be seen later
        self.start = start
        self.goal = goal
        # x, y = start
        # s1 = self.addRect(max(0, x - 1), y, 3, 1, pen=QPen(QColor(56, 194, 180)))
        # s2 = self.addRect(x, max(0, y - 1), 1, 3, pen=QPen(QColor(56, 194, 180)))
        # x, y = goal
        # g1 = self.addRect(max(0, x - 1), y, 3, 1, pen=QPen(QColor(245, 34, 213)))
        # g2 = self.addRect(x, max(0, y - 1), 1, 3, pen=QPen(QColor(245, 34, 213)))

    def list_visit(self, node_list):
        self.visited.extend(node_list)

    def list_expand(self, node_list):
        self.expanded.extend(node_list)

    def clear(self):
        self.visited = []
        self.expanded = []

if __name__=='__main__':
    pass
