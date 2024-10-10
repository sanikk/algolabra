from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QPushButton, QFileDialog

from algolabra.ui.intro_tab import IntroTab
from algolabra.ui.search_tabs import AstarTab, FringeTab

class UI(QWidget):
    def __init__(self, scenario_service=None):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(ScenarioControls(scenario_service=scenario_service))
        layout.addWidget(TabWindow(scenario_service=scenario_service))
        self.setLayout(layout)

class ScenarioControls(QGroupBox):
    # TODO NEXT !!
    # signal slot: change scenario file => change bucket list
    def __init__(self, scenario_service=None):
        super().__init__("Scenario")
        self.scenario_service = scenario_service
        self.default_button_text = "Choose a Scenario file"
        self.default_label_text = "Pick a Scenario file first"

        layout = QHBoxLayout()

        self.scenario_file_button = QPushButton(scenario_service.get_scenario_file() or self.default_button_text)
        self.scenario_file_button.clicked.connect(self.set_scenario_file)
        layout.addWidget(self.scenario_file_button)

        self.chosen_map_label = QLabel(scenario_service.get_map_name() or self.default_label_text)
        layout.addWidget(self.chosen_map_label)

        self.setLayout(layout)

    def set_scenario_file(self):
        ret = QFileDialog.getOpenFileName(parent=self,
                                          caption='Choose Scenario file',
                                          directory='.')
        if ret:
            self.scenario_service.set_scenario_file(ret[0])
            self.scenario_file_button.setText(ret[0] or "Change file")
            self.chosen_map_label.setText(self.scenario_service.get_map_name() or self.default_label_text)
            # update_bucketbox()

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
