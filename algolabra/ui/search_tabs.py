from PyQt6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QGraphicsView
from algolabra.ui.map_scene import MapScene

class SearchTab(QWidget):
    def __init__(self, parent=None, search_name=None, search_func=None, scenario_service=None):
        super().__init__(parent=None)
        self.scenario_service = scenario_service

        layout = QVBoxLayout()
        control_area = get_control_area(search_name, search_func)
        layout.addWidget(control_area)

        self.scene = MapScene(self.scenario_service.get_map_list(), scenario_service=scenario_service)
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.setLayout(layout)

def get_control_area(search_name: str, search_runner):
    control_group = QGroupBox()
    control_layout = QHBoxLayout()

    run_search_label = QLabel(f"run {search_name} slower")
    control_layout.addWidget(run_search_label)

    run_search_button = QPushButton('run')
    run_search_button.clicked.connect(search_runner)
    control_layout.addWidget(run_search_button)

    control_group.setLayout(control_layout)
    return control_group

