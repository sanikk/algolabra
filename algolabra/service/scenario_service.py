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
        self.map_data = None
        self.map_title = None

    def get_map_data(self):
        return self.map_data

    def get_map_title(self):
        return self.map_title

    def get_map_size(self):
        return len(self.map_data)

    def set_map(self, map_path=None):
        if not map_path:
            return
        self.map_file = map_path
        self.map_data = read_map(self.map_file)
        self.map_changed.emit()

        # SCENARIO METHODS

    def read_scenarios(self):
        if self.scenario_file:
            self.map_title, self.scenarios = read_scenarios(self.scenario_file)

    def get_data_from_bucket(self, bucket):
        """
        Returns id, start, goal of scenarios in bucket.
        """
        return [(a[0], a[2], a[3]) for a in self.scenarios.get(bucket, [])]

    def get_bucket_strings(self, bucket: int):
        """
        Get scenarios with individual cols as strings.

        used in intro_tab prepare_table
        """
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
        """
        Return list of bucket indexes.

        used in intro_tab.bucket_box
        """
        return [str(a) for a in self.scenarios.keys()]

    def get_scenario_file(self):
        return self.scenario_file

    def set_scenario_file(self, filepath):
        if filepath:
            self.scenarios.clear()
            self.scenario_file = filepath
            self.read_scenarios()
            if self.map_title:
                map_path = Path(filepath).parent / self.map_title
                if Path(map_path).exists():
                    self.set_map(map_path)

    def get_scenario_start_and_goal(self, bucket, index):
        scenario = self.scenarios[bucket][index]
        return scenario[2], scenario[3]
