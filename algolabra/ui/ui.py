from PyQt6.QtWidgets import QTabWidget, QWidget

from algolabra.ui.intro_tab import IntroTab
from algolabra.ui.search_tabs import AstarTab, FringeTab


class TabWindow(QTabWidget):

    # TODO make resizable like this
    # https://doc.qt.io/qt-6/qsizegrip.html
    def __init__(self, parent: QWidget = None, scenario_service=None):
        super().__init__(parent=parent)

        intro_tab = IntroTab(scenario_service=scenario_service)
        self.addTab(intro_tab, 'intro tab')
        astar_tab = AstarTab(scenario_service=scenario_service)
        self.addTab(astar_tab, 'A* tab')
        fringe_tab = FringeTab(scenario_service=scenario_service)
        self.addTab(fringe_tab, 'Fringe search tab')
