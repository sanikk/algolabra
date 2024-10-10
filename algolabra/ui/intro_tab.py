from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QGroupBox, QPushButton, QComboBox, QTableWidget, QTableWidgetItem


class IntroTab(QWidget):
    def __init__(self, parent=None, scenario_service=None):
        super().__init__(parent=parent)
        self.scenario_service = scenario_service
        self.bucketbox = None
        self.table = None

        layout = QVBoxLayout()

        layout.addWidget(self.get_scenario_box())
        layout.addWidget(self.astar_box())
        layout.addWidget(self.fringe_box())

        self.setLayout(layout)

        self.scenario_service.map_changed.connect(self.update_table)
        self.scenario_service.map_changed.connect(self.update_bucketbox)
        self.bucketbox.currentIndexChanged.connect(self.update_table)

    def astar_box(self):
        groupbox = QGroupBox("A*")
        layout = QVBoxLayout()

        result_label = QLabel("No results yet")
        layout.addWidget(result_label)

        button = QPushButton("Run A*")

        def updater():
            data = self.scenario_service.run_astar_fast(bucket=self.bucketbox.currentIndex())
            result_label.setText(data)

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
            data = self.scenario_service.run_fringe_fast(bucket=self.bucketbox.currentIndex())
            [[self.table.setItem(i, j + 9, QTableWidgetItem("{:.8f}".format(item))) for j, item in enumerate(line)] for i, line in enumerate(data)]
        button.clicked.connect(updater)
        layout.addWidget(button)

        groupbox.setLayout(layout)
        return groupbox


    @pyqtSlot(str)
    def update_bucketbox(self, trash):
        self.bucketbox.clear()
        self.bucketbox.addItems(self.scenario_service.get_bucket_list())


    def get_scenario_table(self):
        table = QTableWidget()
        table.setRowCount(10)
        labels = ["id", "bucket", "start", "goal", "cost",
        "A* cost", "perf_time", "proc_time", "thread_time",
        "Fringe cost", "perf_time", "proc_time", "thread_time"]
        table.setColumnCount(len(labels))
        table.setHorizontalHeaderLabels(labels)
        return table

    @pyqtSlot(int)
    @pyqtSlot(str)
    def update_table(self, trash):
        table = self.table
        table.clearContents()
        data = self.scenario_service.get_bucket_strings(self.bucketbox.currentIndex())
        if data:
            [[table.setItem(y, x, QTableWidgetItem(item)) for x, item in enumerate(line)] for y, line in enumerate(data)]

    def get_scenario_box(self):
        groupbox = QGroupBox("Scenario")
        layout = QVBoxLayout()

        self.bucketbox = QComboBox()
        layout.addWidget(self.bucketbox)

        self.table = self.get_scenario_table()
        layout.addWidget(self.table)

        groupbox.setLayout(layout)
        return groupbox
