from PyQt6.QtWidgets import QTabWidget, QWidget

from algolabra.ui.intro_tab import IntroTab
from algolabra.ui.search_tabs import SearchTab


class TabWindow(QTabWidget):
    def __init__(self, parent: QWidget = None, map_path=None, search_service=None):
        super().__init__(parent=parent)

        intro_tab = IntroTab(search_service=search_service)
        self.addTab(intro_tab, 'intro tab')
        astar_tab = SearchTab(search_name='A*', search_func=search_service.playbyplay_astar, search_service=search_service)
        self.addTab(astar_tab, 'A* tab')
        fringe_tab = SearchTab(search_name='Fringe Search', search_func=search_service.playbyplay_fringe, search_service=search_service)
        self.addTab(fringe_tab, 'Fringe search tab')
