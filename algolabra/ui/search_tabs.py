from decimal import Decimal

from PyQt6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QGraphicsView, QComboBox, QLabel
from PyQt6.QtCore import pyqtSlot, QRect, QRectF

from algolabra.ui.map_scene import MapScene


def get_control_area(search_name: str):
    control_group = QGroupBox()
    control_layout = QHBoxLayout()

    run_search_button = QPushButton(f"run {search_name} slower")
    control_layout.addWidget(run_search_button)
    control_group.setLayout(control_layout)

    return run_search_button, control_group


class SearchTab(QWidget):
    def __init__(self, parent=None, scenario_service=None, search_service=None):
        super().__init__(parent=parent)
        self.scenario_service = scenario_service
        self.search_service = search_service

        self.scene = MapScene(scenario_service=scenario_service, search_service=search_service)
        self.view = QGraphicsView(self.scene)
        self.view.scale(10, 10)

        self.bucket_box = None
        self.scenario_box = None

        self.layout = layout = QVBoxLayout()
        layout.addWidget(self.get_common())

    def get_common(self):
        container = QWidget()
        layout = QVBoxLayout()
        self.bucket_box = bucket_box = QComboBox()
        layout.addWidget(bucket_box)
        self.scenario_box = scenario_box = QComboBox()
        layout.addWidget(scenario_box)
        container.setLayout(layout)

        # connect stuff

        @pyqtSlot()
        def update_bucket_box():
            bucket_box.clear()
            bucket_box.addItems(self.scenario_service.get_bucket_list())

        @pyqtSlot(int)
        @pyqtSlot()
        def update_scenario_box():
            scenario_box.clear()
            scenario_box.addItems(self.scenario_service.get_full_strings(bucket_box.currentIndex()))

        self.scenario_service.map_changed.connect(update_bucket_box)
        self.scenario_service.map_changed.connect(update_scenario_box)
        bucket_box.currentIndexChanged.connect(update_scenario_box)

        def scenario_changer():
            self.scene.scenario_changed(bucket_box.currentIndex(), scenario_box.currentIndex())
            self.set_view(bucket_box.currentIndex(), scenario_box.currentIndex())

        bucket_box.currentIndexChanged.connect(scenario_changer)
        scenario_box.currentIndexChanged.connect(scenario_changer)
        return container

    def set_view(self, bucket, index, extra_view=20):
        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, index)
        delta_x = max(start[0], goal[0]) - min(start[0], goal[0])
        delta_y = max(start[1], goal[1]) - min(start[1], goal[1])
        viewsize = min(self.scenario_service.get_map_size() - 1, max(delta_x, delta_y) + 2 * extra_view)
        qr = QRectF(
            max(min(start[0], goal[0]) - extra_view, 0),
            max(min(start[1], goal[1]) - extra_view, 0),
            viewsize,
            viewsize
        )
        self.view.setSceneRect(qr)

class AstarTab(SearchTab):
    def __init__(self, parent=None, scenario_service=None, search_service=None):
        super().__init__(parent=parent, scenario_service=scenario_service, search_service=search_service)

        run_button, control_area = get_control_area("A*")
        self.layout.addWidget(control_area)
        run_button.clicked.connect(self.run_astar)

        self.layout.addWidget(self.view)

        self.setLayout(self.layout)

    def run_astar(self):
        self.search_service.playbyplay_astar(self.bucket_box.currentIndex(), self.scenario_box.currentIndex())

class FringeTab(SearchTab):
    def __init__(self, parent=None, scenario_service=None, search_service=None):
        super().__init__(parent=parent, scenario_service=scenario_service, search_service=search_service)

        self.expanded = 0
        self.visited = 0
        self.flimit = 0

        self.visited_value_label = None
        self.expanded_value_label = None
        self.flimit_value_label = None

        run_button, control_area = get_control_area("Fringe")
        self.layout.addWidget(control_area)
        run_button.clicked.connect(self.run_fringe)

        self.layout.addWidget(self.get_info_box())

        # self.scene = MapScene(scenario_service=scenario_service, search_service=search_service)

        self.layout.addWidget(self.view)

        self.setLayout(self.layout)

    def run_fringe(self):
        self.search_service.start_fringe_thread(self.bucket_box.currentIndex(), self.scenario_box.currentIndex(),
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

    def get_info_box(self):
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
