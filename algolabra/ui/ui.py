from PyQt6.QtWidgets import QTabWidget, QWidget
import sys

from algolabra.ui.intro_tab import IntroTab
from algolabra.ui.search_tabs import AstarTab, FringeTab, SearchTab
from algolabra.ui.map_scene import MapScene


class TabWindow(QTabWidget):
    def __init__(self, parent: QWidget = None, map_path=None, search_service=None):
        super().__init__(parent=parent)

        intro_tab = IntroTab(search_service=search_service)
        self.addTab(intro_tab, 'intro tab')
        astar_tab = SearchTab('A*', search_service.playbyplay_astar)
        self.addTab(astar_tab, 'A* tab')
        fringe_tab = SearchTab('Fringe Search', search_service.playbyplay_fringe)
        self.addTab(fringe_tab, 'Fringe search tab')
