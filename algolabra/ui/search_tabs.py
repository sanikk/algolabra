from PyQt6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from algolabra.service.search_service import SearchService


class SearchTab(QWidget):
    def __init__(self, search_name, search_func, parent=None, search_service=None):
        super().__init__(parent=None)
        self.search_service = search_service

        layout = QVBoxLayout()
        control_area = get_control_area(search_name, search_func)
        layout.addWidget(control_area)
        self.setLayout(layout)


class AstarTab(QWidget):
    def __init__(self, parent=None, search_service=None):
        super().__init__(parent=None)
        self.search_service = search_service

        layout = QVBoxLayout()
        control_area = get_control_area('A*',search_service.playbyplay_astar)
        layout.addWidget(control_area)
        self.setLayout(layout)



class FringeTab(QWidget):
    def __init__(self, parent=None, search_service=None):
        super().__init__(parent=None)
        self.search_service = search_service
        self.control_area = get_control_area('Fringe', search_service.playbyplay_fringe)


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

