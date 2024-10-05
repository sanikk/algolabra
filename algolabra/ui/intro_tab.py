from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QGroupBox, QHBoxLayout, QPushButton


class IntroTab(QWidget):
    def __init__(self, parent=None, search_service=None):
        super().__init__(parent=parent)
        self.search_service = search_service

        layout = QVBoxLayout()

        chosen_map_label = QLabel('Chosen map')
        layout.addWidget(chosen_map_label)
        self.chosen_map_value_label = QLabel(self.search_service.get_map_path() or "No map chosen yet")
        layout.addWidget(self.chosen_map_value_label)

        chosen_scenario_label = QLabel('Chosen scenario')
        layout.addWidget(chosen_scenario_label)
        self.chosen_scenario_value_label = QLabel(str(self.search_service.get_scenario() or "No scenario chosen yet"))
        layout.addWidget(self.chosen_scenario_value_label)

        astar_time_title_label = QLabel('A* time')
        layout.addWidget(astar_time_title_label)
        self.astar_time_result_label = QLabel(self.search_service.get_astar_time() or "No results yet")
        layout.addWidget(self.astar_time_result_label)

        fringe_time_title_label = QLabel('Fringe time')
        layout.addWidget(fringe_time_title_label)
        self.fringe_time_result_label = QLabel(self.search_service.get_fringe_time() or "No results yet")
        layout.addWidget(self.fringe_time_result_label)

        buttons_group = self.get_buttons_group_box()
        layout.addWidget(buttons_group)

        self.setLayout(layout)

    def get_buttons_group_box(self):
        buttons_group = QGroupBox()
        buttons_layout = QHBoxLayout()

        map_change_dialog_button = QPushButton('set map')
        map_change_dialog_button.clicked.connect(self.set_map)
        buttons_layout.addWidget(map_change_dialog_button)

        scenario_change_button = QPushButton('set scenario')
        scenario_change_button.clicked.connect(self.set_scenario)
        buttons_layout.addWidget(scenario_change_button)

        run_astar_button = QPushButton('run A* fast')
        run_astar_button.clicked.connect(self.search_service.time_astar)
        buttons_layout.addWidget(run_astar_button)

        run_fringe_button = QPushButton('run Fringe Search fast')
        run_fringe_button.clicked.connect(self.search_service.time_fringe)
        buttons_layout.addWidget(run_fringe_button)

        buttons_group.setLayout(buttons_layout)
        return buttons_group

    def set_map(self, map_dir=None):
        filename = QFileDialog.getOpenFileName(parent=self,
                                                   caption='Choose Map file',
                                                   directory=map_dir or '.')
        if filename:
            self.search_service.set_map(filename)
            self.chosen_map_value_label.setText(filename)

    def set_scenario(self):
        pass
