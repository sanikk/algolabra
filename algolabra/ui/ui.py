from PyQt6.QtWidgets import QApplication, QGraphicsView
from algolabra.ui.map_scene import MapScene


class UI(QGraphicsView):
    def __init__(self, map_path=None, *args):
        super().__init__(*args)

        self.setScene(MapScene(map_path))
        self.setWindowTitle("Mapview")
        self.resize(640, 480)
        self.show()
