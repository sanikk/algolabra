from algolabra.scenarios.map_component import read_map, read_scenarios
from pathlib import Path

class ScenarioService:
    def __init__(self, search_service=None):
        self.search_service = search_service

        self.scenario_file = None
        self.scenarios = {}

        self.map_file = None
        self.map_list = None
        self.map_name = None

    def get_map_file(self):
        return self.map_file

    def get_map_list(self):
        return self.map_list

    def set_map(self, map_path=None):
        if not map_path:
            return
        self.map_file = map_path
        self.map_list = read_map(self.map_file)

    def get_map_name(self):
        return self.map_name

        # SCENARIO METHODS

    def read_scenarios(self):
        if self.scenario_file:
            self.map_name, self.scenarios = read_scenarios(self.scenario_file)

    def get_bucket(self, bucket: int):
        return self.scenarios.get(bucket, [])

    def get_bucket_list(self):
        return [str(a) for a in self.scenarios.keys()]

    def get_scenario_file(self):
        return self.scenario_file

    def set_scenario_file(self, filepath):
        if filepath:
            self.scenario_file = filepath
            self.read_scenarios()
            if self.map_name:
                map_path = Path(filepath).parent / self.map_name
                self.set_map(map_path)

    def get_scenarios(self):
        return self.scenarios

    # PASSTHRU FOR TIME DATA for now
    def get_astar_time(self):
        return self.search_service.get_astar_time()

    def run_astar_fast(self, bucket):
        return self.search_service.run_timed_astar()

    def get_fringe_time(self):
        return self.search_service.get_fringe_time()

    def run_fringe_fast(self, bucket):
        results = []
        print("scenario service run_fringe_fast prints")
        for scenario_id, bucket, start, goal, ideal_cost in self.scenarios.get(bucket, []):
            results.append(self.search_service.run_timed_fringe(start, goal, self.map_list))
        print(f"{results=}")
        # [
        #    (1, [0.00998287700349465, 0.009089730000000018, 0.009089126000000003]),
        #    (2.8284271247461903, [0.009297609038185328, 0.008531057000000009, 0.00853570299999995]),
        # ]
        return results