from algolabra.scenarios.map_component import read_map, read_scenarios

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

    # def get_scenario(self, bucket, scenario):
    #     if bucket := self.get_bucket(bucket):
    #         return bucket[scenario]

    def get_scenario_file(self):
        return self.scenario_file

    def set_scenario_file(self, filepath):
        if filepath:
            self.scenario_file = filepath
            self.read_scenarios()

    def get_scenarios(self):
        return self.scenarios

    # PASSTHRU FOR TIME DATA for now
    def get_astar_time(self):
        return self.search_service.get_astar_time()

    def run_astar_fast(self):
        return self.search_service.run_timed_astar()

    def get_fringe_time(self):
        return self.search_service.get_fringe_time()

    def run_fringe_fast(self):
        return self.search_service.run_timed_fringe()
