from PyQt6.QtWidgets import QTabWidget, QWidget
import sys

from algolabra.ui.intro_tab import IntroTab
from algolabra.ui.map_scene import MapScene


class TabWindow(QTabWidget):
    def __init__(self, parent: QWidget = None, map_path=None, search_service=None):
        super().__init__(parent=parent)
        # need this to exit cleanly?
        self._search_service = search_service

        intro_tab = IntroTab(search_service=search_service)
        self.addTab(intro_tab, 'intro tab')
        # map_view_tab = MapScene(map_path, search_service)
        # self.addTab(map_view_tab, 'map view')

