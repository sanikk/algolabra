from collections import deque

from PyQt6.QtGui import QColor, QImage, QPixmap
from PyQt6.QtWidgets import QGraphicsScene


class MapScene(QGraphicsScene):
    def __init__(self, scenario_service=None, tile_size=10):
        super().__init__()
        self.tile_size = tile_size
        self.scenario_service = scenario_service

    def get_image_from_map(self, map_data: list):
            image = QImage(len(map_data[0]), len(map_data), QImage.Format.Format_RGB32)
            image.fill(QColor(0, 0, 0))
            [[image.setPixelColor(x, y, QColor(255, 255, 255)) for x, cell in enumerate(row) if cell=="."] for y, row in enumerate(map_data)]

            return image.scaled(len(map_data) * self.tile_size, len(map_data[0]) * self.tile_size)

    def set_bg_image(self):
        map_list = self.scenario_service.get_map_list()
        if not map_list:
            return
        self.clear()
        pixmap = QPixmap.fromImage(self.get_image_from_map(map_list))
        self.addPixmap(pixmap)

def paint_cell(x, y, tile_size, color, image):
    # käytän tätä ehkä myöhemmin
    for i in range(tile_size):
        for j in range(tile_size):
            image.setPixel(x * tile_size + i, y * tile_size + j, color.rgb())


if __name__=='__main__':
    pass
