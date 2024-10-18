from PyQt6.QtCore import pyqtSlot, Qt, QRectF, QEvent
from PyQt6.QtGui import QColor, QImage, QPixmap, QBrush, QPen, QHelpEvent
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem, QToolTip, QWidget


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
        self.paintable_layer = PaintableLayer(size=self.pixmap.width(), start=start, goal=goal)
        self.addItem(self.paintable_layer)

    def paint_tile_color(self, x, y, red, blue, green):
        self.addRect(x, y, 1, 1, pen=QPen(Qt.PenStyle.NoPen), brush=QBrush(QColor(red, blue, green)))

    @pyqtSlot(int, int)
    def node_visit(self, x, y):
        self.paintable_layer.node_visit(x, y)

    @pyqtSlot(int, int)
    def node_expansion(self, x, y):
        self.paintable_layer.node_expand(x, y)

    @pyqtSlot(str)
    def flimit_change(self, new_flimit: str):
        # not used right now
        pass

    def get_slots(self):
        return self.node_visit, self.node_expansion, self.flimit_change

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
        self.setAcceptHoverEvents(True)
        # self.setToolTip(f"({event.pos()},{})")

    def boundingRect(self):
        return QRectF(0,0,self.size, self.size)

    def paint(self, painter, option, widget = None):
        """
        When update() is called this method handles the actual painting.
        I try to paint visited first and expanded on top of that.
        We shall see.
        """
        self.paint_start_goal(painter)

        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(QBrush(QColor(0, 255, 0)))
        [painter.drawRect(x, y, 1, 1) for x, y in self.visited]

        painter.setBrush(QBrush(QColor(0, 0, 255)))
        [painter.drawRect(x, y, 1, 1) for x, y in self.expanded]

    def paint_start_goal(self, painter):
        if not self.start and self.goal:
            return
        painter.setPen(QPen(QColor(56, 194, 180)))
        painter.drawRect(max(0, self.start[0] - 1), self.start[1], 3, 1)
        painter.drawRect(self.start[0], max(0, self.start[1] - 1), 1, 3)
        painter.setPen(QPen(QColor(245, 34, 213)))
        painter.drawRect(max(0, self.goal[0] - 1), self.goal[1], 3, 1)
        painter.drawRect(self.goal[0], max(0, self.goal[1] - 1), 1, 3)

    def node_visit(self, x, y):
        self.visited.append((x, y))
        self.update(x, y, 1, 1)

    def node_expand(self, x, y):
        self.expanded.append((x, y))
        self.update(x,y,1,1)

    def fill_start_goal(self, start, goal):
        # these are stylized so they can still be seen later
        self.start = start
        self.goal = goal
        self.update()

    def clear(self):
        self.visited = []
        self.expanded = []
        self.update()

    def hoverMoveEvent(self, event):
        QToolTip.showText(event.screenPos(), f"({int(event.pos().x())}, {int(event.pos().y())})", None)
        super().hoverMoveEvent(event)


if __name__=='__main__':
    pass
