from PyQt6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QComboBox, QLabel
from PyQt6.QtCore import pyqtSlot, QRectF

from algolabra.ui.bucket_box import get_common

class LogTab(QWidget):
    def __init__(self, parent=None, scenario_service=None, search_service=None):
        super().__init__(parent=parent)
        self.scenario_service = scenario_service
        self.search_service = search_service

        self.bucket_box = None
        self.scenario_box = None

        self.layout = layout = QVBoxLayout()
        layout.addWidget(get_common(self))
        control_group = QGroupBox()
        control_layout = QHBoxLayout()

        run_search_button = QPushButton(f"run Fringe with Logging")
        control_layout.addWidget(run_search_button)
        control_group.setLayout(control_layout)

        layout.addWidget(control_group)
        self.setLayout(layout)
        run_search_button.clicked.connect(self.run_with_logging)

    def run_with_logging(self):
        self.search_service.run_fringe_with_logging(self.bucket_box.currentIndex(), self.scenario_box.currentIndex())
