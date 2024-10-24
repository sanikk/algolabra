from PyQt6.QtCore import pyqtSignal, QObject

from algolabra.common_search_utils.result_utils import timered
from algolabra.astar.astar_thread import AstarThread
from algolabra.fringe.timed_fringe import fringe_search as testbed_search
from algolabra.astar.astar import astar
from algolabra.fringe.fringe_thread import FringeThread
from algolabra.fringe.fringe_with_loggings import fringe_search_with_logging
from algolabra.fringe.new_loggings import fringe_search_with_logging

# import testbed cases here as testbed_timed or testbed_search

from algolabra.fringe.dequef import fringe_search as intro_tab_search
from algolabra.fringe.dequef import fringe_search as basecase_search



class SearchService(QObject):

    operate = pyqtSignal()

    def __init__(self, scenario_service=None):
        super().__init__()
        self.scenario_service = scenario_service

    # SEARCH ALGO METHODS
    # FRINGE
    @timered
    def run_timed_fringe(self, start, goal, citymap, diag_cost):
        return intro_tab_search(start, goal, citymap, diag_cost)

    def run_fringe_for_bucket(self, bucket: int):
        results = []
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):

            results.append(self.run_timed_fringe(start, goal, map_data, diag_cost))
            # print(results[-1])
            print(f"{scenario_id} done.")
        return results

    @timered
    def run_timed_fringe_two(self, start, goal, citymap, diag_cost):
        return basecase_search(start, goal, citymap, diag_cost)

    def run_fringe_for_bucket_two(self, bucket: int):
        results = []
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):

            results.append(self.run_timed_fringe_two(start, goal, map_data, diag_cost))
            # print(results[-1])
            print(f"{scenario_id} done.")
        return results

    def start_fringe_thread(self, bucket, index, map_slots, data_slots):
        """
        Runs the fringe version made for the Fringe Tab. It just sends default non-blocking signals now
        from another thread. GUI keeps visited/expanded/status counts used in output.
        """
        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, index)
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        instanced_thread = FringeThread(self, start, goal, map_data, map_slots, data_slots, diag_cost)
        instanced_thread.finished.connect(instanced_thread.deleteLater)
        instanced_thread.start()

    # A*

    def start_astar_thread(self, bucket, index, map_slots, data_slots):
        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, index)
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        instanced_thread = AstarThread(self, start, goal, map_data, map_slots, data_slots, diag_cost)
        instanced_thread.finished.connect(instanced_thread.deleteLater)
        instanced_thread.start()

    @timered
    def run_timed_astar(self, start, goal, citymap, diag_cost):
        return astar(start, goal, citymap, diag_cost)

    def run_astar_for_bucket(self, bucket: int):
        results = []
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):
            for i in range(10):
                results.append(self.run_timed_astar(start, goal, map_data, diag_cost))
            print(f"{scenario_id} done.")
        return results

    # TESTBED
    @timered
    def run_timed_testbed(self, start, goal, citymap, diag_cost):
        # return testbed_search(start, goal, citymap, diag_cost)
        return testbed_search(start, goal, citymap, diag_cost)


    def run_testbed_for_bucket(self, bucket: int):
        results = []
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):
            results.append(self.run_timed_testbed(start, goal, map_data, diag_cost))
            print(f"{scenario_id} done.")
        return results

    # LOGGING

    def run_fringe_with_logging(self, bucket, scenario):
        fringe_search_with_logging(*self.scenario_service.get_scenario_start_and_goal(bucket, scenario), self.scenario_service.get_map_data(), bucket, scenario, self.scenario_service.get_diag_cost())


