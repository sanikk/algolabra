from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QPushButton, QComboBox, QTableWidget, QTableWidgetItem


class IntroTab(QWidget):
    def __init__(self, parent=None, scenario_service=None, search_service=None):
        super().__init__(parent=parent)
        self.scenario_service = scenario_service
        self.search_service = search_service

        self.bucketbox = None
        self.table = None

        layout = QVBoxLayout()

        layout.addWidget(self.get_scenario_box())
        layout.addWidget(self.astar_box())
        layout.addWidget(self.fringe_box())

        self.setLayout(layout)

        self.scenario_service.map_changed.connect(self.prepare_table)
        self.scenario_service.map_changed.connect(self.update_bucketbox)
        self.bucketbox.currentIndexChanged.connect(self.prepare_table)

    @pyqtSlot()
    def prepare_table(self):
        self.table.clearContents()
        data = self.scenario_service.get_bucket_strings(self.bucketbox.currentIndex())
        if data:
            [[self.table.setItem(y, x, QTableWidgetItem(item)) for x, item in enumerate(line)] for y, line in enumerate(data)]

    def astar_box(self):
        groupbox = QGroupBox("A*")
        layout = QVBoxLayout()

        result_label = QLabel("No results yet")
        layout.addWidget(result_label)

        button = QPushButton("Run A*")

        def updater():
            data = self.search_service.run_astar_for_bucket(bucket=self.bucketbox.currentIndex())
            if data:
                # [self.table.setItem(i, 5, QTableWidgetItem("{:.8f}".format(item))) for i, item in enumerate(data)]
                 # for i, line in enumerate(data):
                 #    print(f"{line=}")
                 #    for j, item in enumerate(line):
                 #        print(f"{item=}")
                 #        self.table.setItem(i, j + 5, QTableWidgetItem("{:.8f}".format(item)))
                    # print(line)
                 [[self.table.setItem(i, j + 5, QTableWidgetItem("{:.8f}".format(item))) for j, item in enumerate(line)]
                 for i, line in enumerate(data)]

        button.clicked.connect(updater)
        layout.addWidget(button)

        groupbox.setLayout(layout)
        return groupbox

    def fringe_box(self):
        # TODO add a progress bar while running bucket
        # https://doc.qt.io/qt-6/qprogressbar.html
        groupbox = QGroupBox("Fringe search")
        layout = QVBoxLayout()

        result_label = QLabel("No results yet")
        layout.addWidget(result_label)

        button = QPushButton("Run Fringe")

        def updater():
            data = self.search_service.run_fringe_for_bucket(bucket=self.bucketbox.currentIndex())
            [[self.table.setItem(i, j + 9, QTableWidgetItem("{:.8f}".format(item))) for j, item in enumerate(line)] for i, line in enumerate(data)]

        button.clicked.connect(updater)
        layout.addWidget(button)

        groupbox.setLayout(layout)
        return groupbox

    @pyqtSlot()
    def update_bucketbox(self):
        self.bucketbox.clear()
        self.bucketbox.addItems(self.scenario_service.get_bucket_list())

    def get_scenario_table(self):
        table = QTableWidget()
        table.setRowCount(10)
        # scenario columns
        labels = ["id", "bucket", "start", "goal", "cost",
        # A* columns
        "A* cost", "perf_time", "proc_time", "thread_time",
        # fringe columns
        "Fringe cost", "perf_time", "proc_time", "thread_time",]
                  # "nodes_visited", "nodes_expanded"
        table.setColumnCount(len(labels))
        table.setHorizontalHeaderLabels(labels)
        return table

    def get_scenario_box(self):
        groupbox = QGroupBox("Scenario")
        layout = QVBoxLayout()

        self.bucketbox = QComboBox()
        layout.addWidget(self.bucketbox)

        self.table = self.get_scenario_table()
        layout.addWidget(self.table)

        groupbox.setLayout(layout)
        return groupbox
