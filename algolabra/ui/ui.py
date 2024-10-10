from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QPushButton, QFileDialog, \
    QGridLayout, QComboBox
from PyQt6.QtCore import pyqtSlot, pyqtSignal

from algolabra.ui.intro_tab import IntroTab
from algolabra.ui.search_tabs import AstarTab, FringeTab
from algolabra.ui.map_scene import MapScene

class UI(QWidget):
    def __init__(self, scenario_service=None):
        super().__init__()
        layout = QVBoxLayout()
        self.scenario_controls = ScenarioControls(scenario_service=scenario_service)
        layout.addWidget(self.scenario_controls)
        self.tab_window = TabWindow(scenario_service=scenario_service)
        layout.addWidget(self.tab_window)
        self.setLayout(layout)

        # self.scenario_controls.bucketbox.currentIndexChanged.connect(self.tab_window.intro_tab.update_table)
        # intro_tab.update_table()

        # update_table

class ScenarioControls(QGroupBox):
    # TODO NEXT !!
    # signal slot: change scenario file => change bucket list
    def __init__(self, scenario_service=None):
        super().__init__("Scenario")
        self.scenario_service = scenario_service
        self.default_button_text = "Choose a Scenario file"
        self.default_label_text = "Pick a Scenario file first"
        layout = QGridLayout()

        self.scenario_file_button = QPushButton(scenario_service.get_scenario_file() or self.default_button_text)
        self.scenario_file_button.clicked.connect(self.set_scenario_file)
        layout.addWidget(self.scenario_file_button, 0,0)

        self.chosen_map_label = QLabel(scenario_service.get_map_name() or self.default_label_text)
        layout.addWidget(self.chosen_map_label, 0, 1)

        self.bucketbox = QComboBox()
        layout.addWidget(self.bucketbox, 1, 0, 1, 2)
        self.scenario_service.map_changed.connect(self.update_bucketbox)

        self.setLayout(layout)

    def set_scenario_file(self):
        ret = QFileDialog.getOpenFileName(parent=self,
                                          caption='Choose Scenario file',
                                          directory='.')
        if ret:
            self.scenario_service.set_scenario_file(ret[0])
            self.scenario_file_button.setText(ret[0] or "Change file")
            self.chosen_map_label.setText(self.scenario_service.get_map_name() or self.default_label_text)

    @pyqtSlot(str)
    def update_bucketbox(self, trash):
        self.bucketbox.clear()
        self.bucketbox.addItems(self.scenario_service.get_bucket_list())

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
