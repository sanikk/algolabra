from algolabra.fileIO.read_files import read_map, read_scenarios
from pathlib import Path
from PyQt6.QtCore import pyqtSignal, QObject


class ScenarioService(QObject):

    map_changed = pyqtSignal()

    # TODO self.search_service => self.service.
    # we link with self.search.playbyplay....
    # this is way too crowded
    def __init__(self, search_service=None):
        super().__init__()
        self.search_service = search_service

        self.scenario_file = None
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
                self.set_map(map_path)

    # PASSTHRU FOR TIME DATA for now
    def get_astar_time(self):
        return self.search_service.get_astar_time()

    def run_astar_fast(self, bucket):
        return self.search_service.run_timed_astar()

    def get_fringe_time(self):
        return self.search_service.get_fringe_time()

    def run_fringe_fast(self, bucket):
        results = []
        for scenario_id, bucket, start, goal, ideal_cost in self.scenarios.get(bucket, []):
            results.append(self.search_service.run_timed_fringe(start, goal, self.map_list))
            print(f"{scenario_id} done.")
        return results

    def playbyplay_fringe(self, bucket, index):
        print("playbyplay_fringe")

        start, goal = self.get_scenario_start_and_goal(bucket, index)
        print(f"playbyplay {start=}, {goal=}")
        self.search_service.run_fringe_in_another_thread(start, goal, self.map_list)
        # self.search_service.playbyplay_fringe(scenario[2], scenario[3], self.map_list)

    def playbyplay_astar(self, bucket, index):
        scenario = self.scenarios[bucket][index]
        if scenario:
            return self.search_service.playbyplay_astar()

    # Connecting ppl
    def connect_fringe(self, flimit_connection, node_visited_connection, node_expanded_connection):
        self.search_service.fringe.flimit_set.connect(flimit_connection)
        self.search_service.fringe.node_visited.connect(node_visited_connection)
        self.search_service.fringe.node_expanded.connect(node_expanded_connection)

    def upload_fringe_connections(self, fringe_connections):
        self.search_service.get_fringe_connections(fringe_connections)


    def get_scenario_start_and_goal(self, bucket, index):
        scenario = self.scenarios[bucket][index]
        return scenario[2], scenario[3]
