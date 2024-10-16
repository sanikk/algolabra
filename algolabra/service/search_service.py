from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot

from algolabra.astar.astar_thread import AstarThread
from algolabra.fringe.timed_fringe import timed_fringe_search
from algolabra.astar.astar import timed_astar_search
from algolabra.fringe.fringe_thread import FringeThread


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

    @pyqtSlot()
    def handle_results(self):
        print("handling results...done")
