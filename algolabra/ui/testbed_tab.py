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
        layout.addWidget(self.basecase_box())
        self.setLayout(layout)

        self.scenario_service.map_changed.connect(self.update_bucketbox)
        self.bucketbox.currentIndexChanged.connect(self.prepare_table)

    @pyqtSlot()
    def update_bucketbox(self):
        """
        Slot() function that preps and fills table when bucketbox needs to be updated.

        :return: None
        """
        self.prepare_table()
        self.bucketbox.clear()
        self.bucketbox.addItems(self.scenario_service.get_bucket_list())

    @pyqtSlot()
    def prepare_table(self):
        """
        Gets data from SearchService and loads it into the table.

        Unless it's changed
        0-4 bucket 5-10 testcase 11-16 basecase

        cost, perf_time, proc_time, thread_time, visired, expanded, Rounded, Inexact
        last 2 are shown as green/red color. Logic is bad there(and!) but no time.
        :return:
        """
        self.table.clearContents()
        data = self.scenario_service.get_bucket_strings(self.bucketbox.currentIndex())
        if data:
            [[self.table.setItem(y, x, QTableWidgetItem(item)) for x, item in enumerate(line)] for y, line in enumerate(data)]

    def testbed_box(self):
        """
        makes and returns the box for testbed.
        there's the button, and the updater. also label but not used.

        :return:
        """
        groupbox = QGroupBox("Testbed")
        layout = QVBoxLayout()

        result_label = QLabel("No results yet")
        layout.addWidget(result_label)

        def testbed_updater():
            data = self.search_service.run_fringe_for_testcase_bucket(bucket=self.bucketbox.currentIndex())
            if data:
                items = self.prep_data_for_table(data)
                [[self.table.setItem(i, j + 5, item) for j, item in enumerate(line)] for i, line in enumerate(items)]
        button = QPushButton("Run Testbed")
        button.clicked.connect(testbed_updater)
        layout.addWidget(button)

        groupbox.setLayout(layout)
        return groupbox

    def basecase_box(self):
        """
        makes and returns the box for basecase
        there's the button, and the updater. also label but not used.

        :return:
        """
        # TODO add a progress bar while running bucket, printing {id} done for now
        # https://doc.qt.io/qt-6/qprogressbar.html
        groupbox = QGroupBox("Basecase")
        layout = QVBoxLayout()

        result_label = QLabel("No results yet")
        layout.addWidget(result_label)

        button = QPushButton("Run Basecase")
        def basecase_updater():
            data = self.search_service.run_fringe_for_basecase_bucket(bucket=self.bucketbox.currentIndex())
            if data:
                items = self.prep_data_for_table(data)
                [[self.table.setItem(i, j + 11, item) for j, item in enumerate(line)] for i, line in enumerate(items)]
        button.clicked.connect(basecase_updater)
        layout.addWidget(button)

        groupbox.setLayout(layout)
        return groupbox

    def prep_data_for_table(self, data: list):
        """
        Preps data from search_service for your viewing pleasure. :)
        There are next to no checks. If last two values are bool they are used to color the result def:red or
        green if both are False.

        cost, perf_time, proc_time, thread_time, visited, expanded, Rounded, Inexact

        :param data: data from search_service (cost, timer1, timer2, timer3, [visited, expanded,] Rounded, Inexact)

        :return: QTableWidgetItems prepped for scenario_table
        """
        if not data:
            return []
        items = [[QTableWidgetItem("{:.8f}".format(item)) for item in line[:6]] for line in data]
        # color every cost green
        [item[0].setBackground(QBrush(QColor(163, 230, 181))) for item in items]

            # paint result red/green only if there is data on Rounded, Inexact
        if type(data[-2]) == bool:
            [item[0].setBackground(QBrush(QColor(163, 230, 181))) for item in items]
            [item[0].setBackground(QBrush(QColor(214, 148, 176))) for item, data in zip(items, data) if
                not data[-2] or not data[-1]]
        return items



    def get_scenario_table(self) -> QTableWidget:
        """
        Builds and returns a scenario_table.

        Columns are grouped.

        :return: QTableWidget
        """
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

    def get_scenario_box(self) -> QGroupBox:
        """
        Builds and returns the scenario_box that holds bucket_box and scenario_table.
        Also sets self.bucketbox, self.table.

        :return: QGroupBox with a bucketbox
        """
        groupbox = QGroupBox("Scenario")
        layout = QVBoxLayout()

        self.bucketbox = QComboBox()
        layout.addWidget(self.bucketbox)

        self.table = self.get_scenario_table()
        layout.addWidget(self.table)

        groupbox.setLayout(layout)
        return groupbox
