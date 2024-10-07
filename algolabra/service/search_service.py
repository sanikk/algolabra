from algolabra.fringe.timed_fringe import timed_fringe_search
from algolabra.scenarios.map_component import read_map, read_scenarios


class SearchService:
    def __init__(self, map_path=None, scenario_file_path=None, tilesize=8):
        self.tilesize = tilesize

        self.astar_time = None
        self.fringe_time = None

        self.scenario_file_path = scenario_file_path
        self.map_file_path = map_path

        self.scenario_list = None
        self.chosen_scenario = None
        self.citymap = None
        self.map_title = None

        # TODO remove this, dev stuph
        # id, start, goal, ideal_solution
        self.chosen_scenario = [26,	(187, 480), (256, 404), 104.58073578]

        if scenario_file_path:
            self.read_scenarios()

        if map_path:
            self.read_city_map()

    # MAP METHODS

    def read_city_map(self):
        if not self.map_file_path:
            return None
        self.citymap = read_map(self.map_file_path)

    def get_map_path(self):
        return self.map_file_path

    def get_citymap(self):
        return self.citymap

    def set_citymap(self, map_path=None):
        if not map_path:
            return
        self.map_file_path = map_path
        self.read_city_map()

    def get_map_title(self):
        return self.map_title


    # SCENARIO METHODS

    def read_scenarios(self):
        if not self.scenario_file_path:
            return None
        self.map_title, self.scenario_list = read_scenarios(self.scenario_file_path)

    def get_scenario(self):
        return self.chosen_scenario

    def get_scenario_file_path(self):
        return self.scenario_file_path

    def set_scenario_file_path(self, filepath):
        if filepath:
            self.scenario_file_path = filepath

    # SEARCH ALGO METHODS

    def time_fringe(self):
        cost, timers, route = timed_fringe_search()
        new_time = None
        self.fringe_time = new_time


    def time_astar(self):
        new_time = "123.456"
        self.astar_time = new_time
        return new_time


    def playbyplay_fringe(self):
        pass

    def playbyplay_astar(self):
        pass


    def get_astar_time(self):
        return self.astar_time

    def get_fringe_time(self):
        return self.fringe_time


