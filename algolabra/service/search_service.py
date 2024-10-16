from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot

from algolabra.fringe.timed_fringe import timed_fringe_search
from algolabra.astar.astar import astar, timed_astar_search
from algolabra.fringe.fringe_thread import FringeThread


class SearchService(QObject):

    operate = pyqtSignal()

    def __init__(self, scenario_service=None):
        super().__init__()
        self.scenario_service = scenario_service

        self.astar_time = None
        self.fringe_time = None

    # SEARCH ALGO METHODS

    def run_timed_fringe(self, start, goal, citymap):
        cost, timers, route = timed_fringe_search(start, goal, citymap)
        self.fringe_time = timers
        return [cost, *timers]

    def run_fringe_for_bucket(self, bucket: int):
        results = []
        map_data = self.scenario_service.get_map_data()
        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):
            results.append(self.run_timed_fringe(start, goal, map_data))
            print(f"{scenario_id} done.")
        return results

    def start_fringe_thread(self, bucket, index, map_slots, data_slots):
        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, index)
        map_data = self.scenario_service.get_map_data()

        instanced_thread = FringeThread(self, start, goal, map_data, map_slots, data_slots)
        instanced_thread.start()

    def run_timed_astar(self, start, goal, citymap):
        cost, timers, route = timed_astar_search(start, goal, citymap)
        self.astar_time = timers
        return [cost, *timers]

    def run_astar_for_bucket(self, bucket: int):
        results = []
        map_data = self.scenario_service.get_map_data()
        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):
            results.append(self.run_timed_astar(start, goal, map_data))
            print(f"{scenario_id} done.")
        return results

    def playbyplay_astar(self, start, goal, citymap):
        pass

    def get_astar_time(self):
        return self.astar_time

    def get_fringe_time(self):
        return self.fringe_time

    @pyqtSlot()
    def handle_results(self):
        print("handling results...done")

    def get_update(self):
        return [(0,0), (0,1), (1, 0), (1, 1)], [(6, 6), (6, 7), (7, 6), (7, 7)], 3