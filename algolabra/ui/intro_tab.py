from tokenize import group

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QGroupBox, QPushButton, QComboBox, QTableWidget, QTableWidgetItem


class IntroTab(QWidget):
    def __init__(self, parent=None, scenario_service=None):
        super().__init__(parent=parent)
        self.scenario_service = scenario_service

        layout = QVBoxLayout()

        layout.addWidget(self.get_scenario_box())
        layout.addWidget(self.get_groupbox("A*", self.scenario_service.get_astar_time, self.scenario_service.run_astar_fast, "Run A* fast"))
        layout.addWidget(self.get_groupbox("Fringe search", self.scenario_service.get_fringe_time, self.scenario_service.run_fringe_fast, "Run Fringe search fast"))

        self.setLayout(layout)

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

        bucketbox = QComboBox()
        layout.addWidget(bucketbox)

        table = self.get_scenario_table()

        layout.addWidget(table)

        def set_scenario_file():
            ret = QFileDialog.getOpenFileName(parent=self,
                                              caption='Choose Scenario file',
                                              directory='.')
            if ret:
                self.scenario_service.set_scenario_file(ret[0])
                scenario_file_box.setText(ret[0] or "No scenario file chosen yet")
                update_bucketbox()

        def update_bucketbox():
            bucketbox.clear()
            bucketbox.addItems(self.scenario_service.get_bucket_list())

        def update_table():
            table.clear()
            data = self.scenario_service.get_bucket(bucketbox.currentIndex())

            [[[table.setItem(rownumber, columnnumber, QTableWidgetItem(f"{columndata[0]},{columndata[1]}"))]
             if isinstance(columndata, tuple) else
                [table.setItem(rownumber, columnnumber, QTableWidgetItem(f"{columndata}"))]
              for columnnumber, columndata in enumerate(datarow)]
             for rownumber, datarow in enumerate(self.scenario_service.get_bucket(bucketbox.currentIndex()))]

        scenario_file_button.clicked.connect(set_scenario_file)
        bucketbox.currentIndexChanged.connect(update_table)

        groupbox.setLayout(layout)
        return groupbox



    def get_scenario_table(self):
        table = QTableWidget()
        table.setRowCount(10)
        labels = ["id", "bucket", "start", "goal", "cost"]
        table.setColumnCount(len(labels))
        table.setHorizontalHeaderLabels(labels)
        return table
