from PyQt6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QGraphicsView
from algolabra.ui.map_scene import MapScene


def get_control_area(search_name: str, scenario_service):
    control_group = QGroupBox()
    control_layout = QHBoxLayout()

    run_search_button = QPushButton(f"run {search_name} slower")

    control_layout.addWidget(run_search_button)

    control_group.setLayout(control_layout)

    return control_group

def get_info_area(scenario_service=None):
    pass
    # info_group = Q

class SearchTab(QWidget):
    def __init__(self, parent=None, scenario_service=None):
        super().__init__(parent=parent)
        self.scenario_service = scenario_service
        self.scene = MapScene(scenario_service=scenario_service)
        # self.scene = scene

        self.layout = QVBoxLayout()
        common_box = QWidget()
        self.layout.addWidget(common_box)
        self.setLayout(self.layout)

class AstarTab(SearchTab):
    def __init__(self, parent=None, scenario_service=None):
        super().__init__(parent=parent, scenario_service=scenario_service)

        control_area = get_control_area("A*", scenario_service)
        self.layout.addWidget(control_area)

        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)

class FringeTab(SearchTab):
    def __init__(self, parent=None, scenario_service=None):
        super().__init__(parent=parent, scenario_service=scenario_service)

        control_area = get_control_area("Fringe", scenario_service)
        self.layout.addWidget(control_area)

        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

