from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QGroupBox, QHBoxLayout, QPushButton


class IntroTab(QWidget):
    def __init__(self, parent=None, search_service=None):
        super().__init__(parent=parent)
        self.search_service = search_service

        layout = QVBoxLayout()

        # make widget
        # layout.addWidget(widget)

        chosen_map_label = QLabel('Chosen map')
        layout.addWidget(chosen_map_label)
        self.chosen_map_value_label = QLabel(self.search_service.get_chosen_map() or "No map chosen yet")
        layout.addWidget(self.chosen_map_value_label)

        # log_path_title_label = QLabel('Log path')
        # layout.addWidget(log_path_title_label)
        # self.log_path_value_label = QLabel(self._path_service.get_log_path())
        # layout.addWidget(self.log_path_value_label)
        buttons_group = self.get_buttons_group_box()
        layout.addWidget(buttons_group)

        self.setLayout(layout)

    def get_buttons_group_box(self):
        buttons_group = QGroupBox()
        buttons_layout = QHBoxLayout()

        map_change_dialog_button = QPushButton('set map')
        map_change_dialog_button.clicked.connect(self.set_map)
        buttons_layout.addWidget(map_change_dialog_button)

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
