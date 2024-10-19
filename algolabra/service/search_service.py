from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
import time
from decimal import Decimal

from algolabra.astar.astar_thread import AstarThread
from algolabra.fringe.timed_fringe import timed_fringe_search
from algolabra.astar.astar import timed_astar_search
from algolabra.fringe.fringe_thread import FringeThread
from algolabra.fringe.fringe_testbed import fringe_search as timed_testbed
from algolabra.common_search_utils.timed_search import timed_search
from algolabra.common_search_utils.check_solution import handle_path
# from algolabra.fringe.vertaisarvio import find_path

class SearchService(QObject):

    operate = pyqtSignal()

    def __init__(self, scenario_service=None):
        super().__init__()
        self.scenario_service = scenario_service

    # SEARCH ALGO METHODS

    def run_timed_fringe(self, start, goal, citymap):
        cost, timers, route, rounded, inexact = timed_fringe_search(start, goal, citymap)
        return [cost, *timers, rounded, inexact]

    def run_fringe_for_bucket(self, bucket: int):
        results = []
        map_data = self.scenario_service.get_map_data()
        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):
            results.append(self.run_timed_fringe(start, goal, map_data))
            print(f"{scenario_id} done.")
        return results

    def start_fringe_thread(self, bucket, index, map_slots, data_slots):
        """
        Runs the fringe version made for the Live Tab. It just sends default non-blocking signals now
        from another thread. GUI keeps visited/expanded/status counts used in output.
        """
        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, index)
        map_data = self.scenario_service.get_map_data()

        instanced_thread = FringeThread(self, start, goal, map_data, map_slots, data_slots)
        instanced_thread.finished.connect(instanced_thread.deleteLater)
        instanced_thread.start()

    def start_astar_thread(self, bucket, index, map_slots, data_slots):
        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, index)
        map_data = self.scenario_service.get_map_data()

        instanced_thread = AstarThread(self, start, goal, map_data, map_slots, data_slots)
        instanced_thread.finished.connect(instanced_thread.deleteLater)
        instanced_thread.start()

    def run_timed_astar(self, start, goal, citymap):
        cost, timers, route, rounded, inexact = timed_astar_search(start, goal, citymap)
        return [cost, *timers, rounded, inexact]

    def run_astar_for_bucket(self, bucket: int):
        results = []
        map_data = self.scenario_service.get_map_data()
        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):
            results.append(self.run_timed_astar(start, goal, map_data))
            print(f"{scenario_id} done.")
        return results

    def run_timed_testbed(self, start, goal, citymap):
        start_times = [time.perf_counter(), time.process_time(), time.thread_time()]
        # route, cost, visited, expanded = find_path(start, goal, citymap)
        route, cost, visited, expanded = None, None, None, None
        end_times = [time.perf_counter(), time.process_time(), time.thread_time()]
        timers = [a - b for a, b in zip(end_times, start_times)]

        # steps, straight, diag =  handle_path(route)
        # cost = diag * Decimal('1.4142135623730950488') + straight

        return [cost, *timers, visited, expanded, False, False]

    def run_testbed_for_bucket(self, bucket: int):
        results = []
        map_data = self.scenario_service.get_map_data()
        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):
            results.append(self.run_timed_testbed(start, goal, map_data))
            print(f"{scenario_id} done.")
        return results

    @pyqtSlot()
    def handle_results(self):
        print("handling results...done")
