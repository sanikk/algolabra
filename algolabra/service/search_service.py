from algolabra.scenarios.map_component import read_map, read_scenarios


class SearchService:
    def __init__(self, map_path=None, scenario_file_path=None, tilesize=8):
        self.tilesize = tilesize

        self.scenario_file_path = scenario_file_path
        self.scenarios = None
        if scenario_file_path:
            self.read_scenarios()

        # id, start, goal, ideal_solution
        self.chosen_scenario = [26,	(187, 480), (256, 404), 104.58073578]

        self.map_path = map_path
        self.citymap = None
        if map_path:
            self.read_city_map()

        self.astar_time = None
        self.fringe_time = None

    def read_city_map(self):
        if not self.map_path:
            return None
        self.citymap = read_map(self.map_path)

    def read_scenarios(self):
        if not self.scenario_file_path:
            return None
        self.scenarios = read_scenarios(self.scenario_file_path)

    def time_fringe(self):
        new_time = None
        self.fringe_time = new_time


    def time_astar(self):
        new_time = None
        self.astar_time = new_time


    def playbyplay_fringe(self):
        pass

    def playbyplay_astar(self):
        pass

    def get_map_path(self):
        return self.map_path

    def get_citymap(self):
        return self.citymap

    def set_citymap(self, map_path=None):
        if not map_path:
            return
        self.map_path = map_path
        self.read_city_map()

    def get_astar_time(self):
        return self.astar_time

    def get_fringe_time(self):
        return self.fringe_time

    def get_scenario(self):
        return self.chosen_scenario