from tokenize import group

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
        # layout.addWidget(self.get_groupbox("A*", self.scenario_service.get_astar_time, self.scenario_service.run_astar_fast, "Run A* fast"))
        # layout.addWidget(self.get_groupbox("Fringe search", self.scenario_service.get_fringe_time, self.scenario_service.run_fringe_fast, "Run Fringe search fast"))

        self.setLayout(layout)
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
        groupbox = QGroupBox("Fringe search")
        layout = QVBoxLayout()

        result_label = QLabel("No results yet")
        layout.addWidget(result_label)

        button = QPushButton("Run Fringe")

        def updater():
            data = self.scenario_service.run_fringe_fast(bucket=self.bucketbox.currentIndex())
            # result_label.setText(data)
            # [
            #    (1, [0.00998287700349465, 0.009089730000000018, 0.009089126000000003]),
            #    (2.8284271247461903, [0.009297609038185328, 0.008531057000000009, 0.00853570299999995]),
            # ]
            # "{:.2f}".format(13.949999999999999)
            [[self.table.setItem(i, j + 5, QTableWidgetItem("{:.8f}".format(item))) for j, item in enumerate(line)] for i, line in enumerate(data)]

        button.clicked.connect(updater)
        layout.addWidget(button)

        groupbox.setLayout(layout)
        return groupbox

    def get_groupbox(self, title, result_getter, runner_func, button_text):
        groupbox = QGroupBox(title)
        layout = QVBoxLayout()

        result_label = QLabel(result_getter() or "No results yet")
        layout.addWidget(result_label)

        button = QPushButton(button_text)
        def updater():
            data = runner_func()
            result_label.setText(data)
        button.clicked.connect(updater)
        layout.addWidget(button)

        groupbox.setLayout(layout)
        return groupbox

    def get_scenario_box(self):
        groupbox = QGroupBox("Scenario")
        layout = QVBoxLayout()

        scenario_file_box = QLabel(f"file: {self.scenario_service.get_scenario_file()}" or "No scenario file chosen yet")
        layout.addWidget(scenario_file_box)

        scenario_file_button = QPushButton("Change file")
        layout.addWidget(scenario_file_button)

        self.bucketbox = QComboBox()
        layout.addWidget(self.bucketbox)

        self.table = self.get_scenario_table()

        layout.addWidget(self.table)

        def set_scenario_file():
            ret = QFileDialog.getOpenFileName(parent=self,
                                              caption='Choose Scenario file',
                                              directory='.')
            if ret:
                self.scenario_service.set_scenario_file(ret[0])
                scenario_file_button.setText(ret[0] or "Change file")
                update_bucketbox()

        def update_bucketbox():
            self.bucketbox.clear()
            self.bucketbox.addItems(self.scenario_service.get_bucket_list())

        def update_table():
            table = self.table
            table.clearContents()
            data = self.scenario_service.get_bucket(self.bucketbox.currentIndex())
            # ugly but works for now. we just insert data into the table as strings.
            [[[table.setItem(rownumber, columnnumber, QTableWidgetItem(f"{columndata[0]},{columndata[1]}"))]
             if isinstance(columndata, tuple) else
                [table.setItem(rownumber, columnnumber, QTableWidgetItem(f"{columndata}"))]
              for columnnumber, columndata in enumerate(datarow)]
             for rownumber, datarow in enumerate(self.scenario_service.get_bucket(self.bucketbox.currentIndex()))]

        scenario_file_button.clicked.connect(set_scenario_file)
        self.bucketbox.currentIndexChanged.connect(update_table)

        groupbox.setLayout(layout)
        return groupbox



    def get_scenario_table(self):
        table = QTableWidget()
        table.setRowCount(10)
        labels = ["id", "bucket", "start", "goal", "cost"
        # [time.perf_counter(), time.process_time(), time.thread_time()]
        , "A* cost", "perf_time", "proc_time", "thread_time",
        "Fringe cost", "perf_time", "proc_time", "thread_time"]
        table.setColumnCount(len(labels))
        table.setHorizontalHeaderLabels(labels)
        return table
