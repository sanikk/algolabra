from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget, QComboBox, QVBoxLayout


def get_common(parent_tab):

    # setup stuff

    container = QWidget()
    layout = QVBoxLayout()
    parent_tab.bucket_box = bucket_box = QComboBox()
    layout.addWidget(bucket_box)
    parent_tab.scenario_box = scenario_box = QComboBox()
    layout.addWidget(scenario_box)
    container.setLayout(layout)

    # connect stuff

    @pyqtSlot()
    def update_bucket_box():
        bucket_box.clear()
        bucket_box.addItems(parent_tab.scenario_service.get_bucket_list())

    @pyqtSlot(int)
    @pyqtSlot()
    def update_scenario_box():
        scenario_box.clear()
        scenario_box.addItems(parent_tab.scenario_service.get_full_strings(bucket_box.currentIndex()))

    parent_tab.scenario_service.map_changed.connect(update_bucket_box)
    parent_tab.scenario_service.map_changed.connect(update_scenario_box)
    bucket_box.currentIndexChanged.connect(update_scenario_box)
    return container



def connect_scenario_change(p):
    def scenario_changer():
        p.scene.scenario_changed(p.bucket_box.currentIndex(), p.scenario_box.currentIndex())
        p.set_view(p.bucket_box.currentIndex(), p.scenario_box.currentIndex())

    p.bucket_box.currentIndexChanged.connect(scenario_changer)
    p.scenario_box.currentIndexChanged.connect(scenario_changer)
