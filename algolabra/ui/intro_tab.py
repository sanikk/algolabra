from tokenize import group

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QGroupBox, QHBoxLayout, QPushButton, QFrame, \
    QComboBox


class IntroTab(QWidget):
    def __init__(self, parent=None, search_service=None):
        super().__init__(parent=parent)
        self.search_service = search_service

        self.chosen_map_box = None
        self.scenario_file_box = None
        self.scenario_combobox = None

        layout = QVBoxLayout()

        layout.addWidget(self.get_map_box())
        layout.addWidget(self.get_scenario_box())

        layout.addWidget(self.get_groupbox("A*", self.search_service.get_astar_time, "Run A* fast"))
        layout.addWidget(self.get_groupbox("Fringe search", self.search_service.get_fringe_time, "Run Fringe search fast"))

        self.setLayout(layout)

    def set_map(self, map_dir=None):
        ret = QFileDialog.getOpenFileName(parent=self,
                                                   caption='Choose Map file',
                                                   directory=map_dir or '.')
        if ret:
            self.search_service.set_citymap(ret[0])
            self.chosen_map_box.setText(ret[0] or "None chosen yet")

    def set_scenario_file(self, map_dir=None):
        ret = QFileDialog.getOpenFileName(parent=self,
                                          caption='Choose Scenario file',
                                          directory=map_dir or '.')
        if ret:
            self.search_service.set_scenario_file_path(ret[0])
            self.scenario_file_box.setText(ret[0] or "None chosen yet")


    def get_groupbox(self, title, result_getter, button_text):
        groupbox = QGroupBox(title)
        layout = QVBoxLayout()

        result_label = QLabel(result_getter() or "No results yet")
        layout.addWidget(result_label)

        button = QPushButton(button_text)
        def updater():
            data = result_getter()
            result_label.setText(data)
        button.clicked.connect(updater)
        layout.addWidget(button)

        groupbox.setLayout(layout)
        return groupbox

    def get_map_box(self):
        groupbox = QGroupBox("Map")
        layout = QVBoxLayout()

        self.chosen_map_box = QLabel(self.search_service.get_map_title() or "None chosen yet")

        button = QPushButton("Change")
        button.clicked.connect(self.set_map)

        layout.addWidget(self.chosen_map_box)
        layout.addWidget(button)
        groupbox.setLayout(layout)

        return groupbox

    def get_scenario_box(self):
        groupbox = QGroupBox("Scenario")
        layout = QVBoxLayout()

        self.scenario_file_box = QLabel(self.search_service.get_scenario_file_path() or "None chosen yet")
        scenario_file_button = QPushButton("Change")
        scenario_file_button.clicked.connect(self.set_scenario_file)

        layout.addWidget(self.scenario_file_box)
        layout.addWidget(scenario_file_button)
        groupbox.setLayout(layout)
        return groupbox

    def populate_scenario_list(self):
        print("populate_scenario_list fired!")
        scenario_list = ['all scenarios'] + self.search_service.get_scenario_list()
        self.scenario_combobox.addItems(scenario_list)
