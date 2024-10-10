from PyQt6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QGraphicsView
from algolabra.ui.map_scene import MapScene


def get_control_area(search_name: str, search_runner, scenario_service):
    control_group = QGroupBox()
    control_layout = QHBoxLayout()

    chosen_map_label = QLabel(scenario_service.get_map_name())
    control_layout.addWidget(chosen_map_label)

    build_map_button = QPushButton("build map")
    control_layout.addWidget(build_map_button)

    run_search_button = QPushButton(f"run {search_name} slower")
    run_search_button.clicked.connect(search_runner)
    control_layout.addWidget(run_search_button)

    control_group.setLayout(control_layout)


    return control_group

def get_info_area(scenario_service=None):
    pass
    # info_group = Q

class AstarTab(QWidget):
    def __init__(self, scenario_service=None, scene=None):
        print(f"astartab init {scene=}")
        super().__init__(parent=None)
        self.scenario_service = scenario_service
        self.scene = scene

        layout = QVBoxLayout()
        control_area = get_control_area("A*", self.scenario_service.playbyplay_astar, scenario_service)
        layout.addWidget(control_area)

        self.view = QGraphicsView(self.scene)
        # self.scenario_service.map_changed.connect(self.change_map)
        layout.addWidget(self.view)

        self.setLayout(layout)

    def change_map(self):
        self.scene.set_bg_image()

class FringeTab(QWidget):
    def __init__(self, scenario_service=None, scene=None):
        super().__init__(parent=None)
        self.scenario_service = scenario_service
        self.scene = scene

        layout = QVBoxLayout()
        control_area = get_control_area("Fringe", self.scenario_service.playbyplay_fringe, scenario_service)
        layout.addWidget(control_area)

        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.setLayout(layout)