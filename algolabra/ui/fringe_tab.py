from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from algolabra.ui.search_tabs import SearchTab

class FringeTab(SearchTab):
    def __init__(self, parent=None, scenario_service=None, search_service=None):
        super().__init__(parent=parent, scenario_service=scenario_service, search_service=search_service)

        run_button, control_area = self.get_control_area("Fringe Live")
        self.layout.addWidget(control_area)
        run_button.clicked.connect(self.run_fringe)

        self.layout.addWidget(self.get_fringe_info_box())
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)

    def run_fringe(self):
        self.search_service.start_fringe_thread(self.bucket_box.currentIndex(), self.scenario_box.currentIndex(),
                                                self.scene.get_slots(), (self.visit, self.expand, self.flimit_changed))


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