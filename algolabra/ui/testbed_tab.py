from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QPushButton, QComboBox, QTableWidget, QTableWidgetItem


class TestbedTab(QWidget):
    def __init__(self, parent=None, scenario_service=None, search_service=None):
        super().__init__(parent=parent)
        self.scenario_service = scenario_service
        self.search_service = search_service

        self.bucketbox = None
        self.table = None

        layout = QVBoxLayout()
        layout.addWidget(self.get_scenario_box())
        layout.addWidget(self.testbed_box())
        layout.addWidget(self.fringe_box())
        self.setLayout(layout)

        self.scenario_service.map_changed.connect(self.update_bucketbox)
        self.bucketbox.currentIndexChanged.connect(self.prepare_table)

    @pyqtSlot()
    def prepare_table(self):
        self.table.clearContents()
        data = self.scenario_service.get_bucket_strings(self.bucketbox.currentIndex())
        if data:
            [[self.table.setItem(y, x, QTableWidgetItem(item)) for x, item in enumerate(line)] for y, line in enumerate(data)]

    def testbed_box(self):
        groupbox = QGroupBox("Testbed")
        layout = QVBoxLayout()

        result_label = QLabel("No results yet")
        layout.addWidget(result_label)

        def updater():
            data = self.search_service.run_testbed_for_bucket(bucket=self.bucketbox.currentIndex())
            if data:
                items = self.prep_data_for_table(data)
                [[self.table.setItem(i, j + 5, item) for j, item in enumerate(line)] for i, line in enumerate(items)]
        button = QPushButton("Run Testbed")
        button.clicked.connect(updater)
        layout.addWidget(button)

        groupbox.setLayout(layout)
        return groupbox

    def fringe_box(self):
        # TODO add a progress bar while running bucket
        # https://doc.qt.io/qt-6/qprogressbar.html
        groupbox = QGroupBox("Basecase")
        layout = QVBoxLayout()

        result_label = QLabel("No results yet")
        layout.addWidget(result_label)

        button = QPushButton("Run Basecase")
        def updater():
            data = self.search_service.run_fringe_for_bucket(bucket=self.bucketbox.currentIndex())
            if data:
                items = self.prep_data_for_table(data)
                [[self.table.setItem(i, j + 11, item) for j, item in enumerate(line)] for i, line in enumerate(items)]
        button.clicked.connect(updater)
        layout.addWidget(button)

        groupbox.setLayout(layout)
        return groupbox

    def prep_data_for_table(self, data):
        if not data:
            return []
        items = [[QTableWidgetItem("{:.8f}".format(item)) for item in line[:6]] for line in data]
        # color every cost green
        [item[0].setBackground(QBrush(QColor(163, 230, 181))) for item in items]
        # color Rounded or Inexact results red
        [item[0].setBackground(QBrush(QColor(214, 148, 176))) for item, line in zip(items, data) if
         not data[6] or not data[7]]
        return items

    @pyqtSlot()
    def update_bucketbox(self):
        self.prepare_table()
        self.bucketbox.clear()
        self.bucketbox.addItems(self.scenario_service.get_bucket_list())

    def get_scenario_table(self):
        table = QTableWidget()
        table.setRowCount(10)

        scenario_columns = ["id", "bucket", "start", "goal", "cost",]
        testbed_columns = ["Testbed cost", "perf_time", "proc_time", "thread_time",
            "nodes_visited", "nodes_expanded",]
        basecase_columns = ["Basecase cost", "perf_time", "proc_time", "thread_time",
            "nodes_visited", "nodes_expanded",]
        labels = [*scenario_columns, *testbed_columns, *basecase_columns]

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
