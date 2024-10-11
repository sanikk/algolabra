from algolabra.fileIO.read_files import read_map, read_scenarios
from pathlib import Path
from PyQt6.QtCore import pyqtSignal, QObject


class ScenarioService(QObject):

    map_changed = pyqtSignal()

    def __init__(self, scenario_file=None):
        super().__init__()

        self.scenario_file = scenario_file
        self.scenarios = {}

        self.map_file = None
        self.map_list = None
        self.map_name = None

    def get_map_list(self):
        return self.map_list

    def get_map_name(self):
        return self.map_name

    def set_map(self, map_path=None):
        if not map_path:
            return
        self.map_file = map_path
        self.map_list = read_map(self.map_file)
        self.map_changed.emit()

        # SCENARIO METHODS

    def read_scenarios(self):
        if self.scenario_file:
            self.map_name, self.scenarios = read_scenarios(self.scenario_file)

    def get_bucket_strings(self, bucket: int):
        bucket = self.scenarios.get(bucket, [])
        if bucket:
            return [[str(a[0]), str(a[1]), f"({a[2][0]}, {a[2][1]})", f"({a[3][0]}, {a[3][1]})", str(a[4])] for a in bucket]
        return bucket

    def get_full_strings(self, bucket: int):
        bucket = self.scenarios.get(bucket, [])

        if bucket:
            return [f"id: {a[0]}, start: ({a[2][0]},{a[2][1]}), goal: ({a[3][0]},{a[3][1]}), ideal: {a[4]}" for a in bucket]
        return bucket

    def get_bucket_list(self):
        return [str(a) for a in self.scenarios.keys()]

    def get_scenario_file(self):
        return self.scenario_file

    def set_scenario_file(self, filepath):
        if filepath:
            self.scenarios.clear()
            self.scenario_file = filepath
            self.read_scenarios()
            if self.map_name:
                map_path = Path(filepath).parent / self.map_name
                if Path(map_path).exists():
                    self.set_map(map_path)

    def get_scenario_start_and_goal(self, bucket, index):
        scenario = self.scenarios[bucket][index]
        return scenario[2], scenario[3]
