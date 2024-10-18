from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from algolabra.ui.search_tabs import SearchTab, get_control_area

class FringeTab(SearchTab):
    def __init__(self, parent=None, scenario_service=None, search_service=None):
        super().__init__(parent=parent, scenario_service=scenario_service, search_service=search_service)

        self.expanded = 0
        self.visited = 0
        self.flimit = 0

        self.visited_value_label = None
        self.expanded_value_label = None
        self.flimit_value_label = None

        run_button, control_area = get_control_area("Fringe Live")
        self.layout.addWidget(control_area)
        run_button.clicked.connect(self.run_fringe)

        self.layout.addWidget(self.get_fringe_info_box())
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)

    def run_fringe(self):
        self.search_service.start_fringe_live_thread(self.bucket_box.currentIndex(), self.scenario_box.currentIndex(),
                                                self.scene.get_slots(), (self.visit, self.expand, self.flimit_changed))

    @pyqtSlot(int, int)
    def visit(self):
        self.visited += 1
        self.visited_value_label.setText(str(self.visited))

    @pyqtSlot(int, int)
    def expand(self):
        self.expanded += 1
        self.expanded_value_label.setText(str(self.expanded))

    @pyqtSlot(str)
    def flimit_changed(self, new_flimit: str):
        self.flimit = new_flimit
        self.flimit_value_label.setText(new_flimit)

    def get_fringe_info_box(self):
        container = QWidget()
        layout = QHBoxLayout()

        flimit_label = QLabel("FLimit:")
        layout.addWidget(flimit_label)

        self.flimit_value_label = QLabel("None")
        layout.addWidget(self.flimit_value_label)

        visited_label = QLabel("Visited:")
        layout.addWidget(visited_label)

        self.visited_value_label = QLabel("None")
        layout.addWidget(self.visited_value_label)

        expanded_label = QLabel("Expanded:")
        layout.addWidget(expanded_label)

        self.expanded_value_label = QLabel("None")
        layout.addWidget(self.expanded_value_label)

        container.setLayout(layout)
        return container