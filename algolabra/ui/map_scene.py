from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QColor, QImage, QPixmap, QBrush
from PyQt6.QtWidgets import QGraphicsScene


class MapScene(QGraphicsScene):
    def __init__(self, scenario_service=None, tile_size=10):
        super().__init__()
        self.tile_size = tile_size
        self.scenario_service = scenario_service
        scenario_service.map_changed.connect(self.set_bg_image)
        self.connect_fringe()

    def get_image_from_map(self, map_data: list):
        image = QImage(len(map_data[0]), len(map_data), QImage.Format.Format_RGB32)
        image.fill(QColor(0, 0, 0))

        [[image.setPixelColor(x, y, QColor(255, 255, 255)) for x, cell in enumerate(row) if cell=="."] for y, row in enumerate(map_data)]

        return image.scaled(len(map_data) * self.tile_size, len(map_data[0]) * self.tile_size)

    @pyqtSlot()
    def set_bg_image(self):
        map_list = self.scenario_service.get_map_list()
        if not map_list:
            return
        self.clear()
        pixmap = QPixmap.fromImage(self.get_image_from_map(map_list))
        self.addPixmap(pixmap)

    @pyqtSlot(int, int)
    def node_visit(self, x, y):
        self.addRect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size, brush= QBrush(QColor(0,255,0)))

    @pyqtSlot(int, int)
    def node_expansion(self, x, y):
        self.addRect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size, brush= QBrush(QColor(0, 0, 255)))

    @pyqtSlot(float)
    # TODO fill this in
    def flimit_change(self, new_flimit):
        pass

    def connect_fringe(self):
        # flimit_connection, node_visited_connection, node_expanded_connection
        self.scenario_service.connect_fringe(self.flimit_change, self.node_visit, self.node_expansion)

if __name__=='__main__':
    pass
