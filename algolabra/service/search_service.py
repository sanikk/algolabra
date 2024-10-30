import logging
from decimal import Decimal

from PyQt6.QtCore import pyqtSignal, QObject

from algolabra.common_search_utils.result_utils import timered

from algolabra.astar.astar_thread import AstarThread
from algolabra.astar.astar import astar
from algolabra.fringe.fringe_thread import FringeThread
from algolabra.fringe.fringe_with_logging import fringe_search_with_logging

# I import different versions here.
from algolabra.fringe.fringe_with_linked_map import fringe_search as basecase_search
from algolabra.fringe.fringe_with_two_deques import fringe_search as testbed_search

class SearchService(QObject):
    """
    Service class that runs the searches and passes the results along.
    Formatting etc should happen here but i wanted to keep this lightweight,
    so it's easy to test many different kinds of internal setups. So put something at
    end of search to output nicely.

    in:
    start, goal, citymap, diag_cost

    out:
    cost, route[, visited, expanded], Inexact, Rounded.

    The handle_results function should be able to handle 4 or 6 fields.
    Gui might interpret 0 visitors, 0 expanded as Inexact=False, Rounded=False.

    """

    operate = pyqtSignal()

    def __init__(self, scenario_service=None):
        super().__init__()
        self.scenario_service = scenario_service
        logging.basicConfig(filename='fringe.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s')

    # SEARCH ALGO METHODS
    # FRINGE
    @timered
    def run_timed_fringe(self, start, goal, citymap, diag_cost):
        """
        Small runner for basecase fringe search.
        The decorator should handle timing.

        :param start: start in a valid format. If it works it works.
        :param goal: goal. see above.
        :param citymap: map to use.
        :param diag_cost: cost of diagonal movement. int|Decimal|float have been tested to work. float causes some
                        slowdowns with the heuristics function.
        """
        return basecase_search(start, goal, citymap, diag_cost)

    def run_fringe_for_bucket(self, bucket: int):
        """
        Runs the scenarios in the chosen bucket.

        Just passes the results through.
        """
        results = []
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):
            results.append(self.run_timed_fringe(start, goal, map_data, diag_cost))
            print(f"{scenario_id} done.")
        return results

    # TESTBED
    @timered
    def run_timed_testbed(self, start, goal, citymap, diag_cost):
        """
        Small runner for testcase search.
        The decorator should handle timing.

        :param start: start in a valid format. If it works it works.
        :param goal: goal. see above.
        :param citymap: map to use.
        :param diag_cost: cost of diagonal movement. int|Decimal|float have been tested to work. float causes some
                slowdowns with the heuristics function.
        """
        return testbed_search(start, goal, citymap, diag_cost)


    def run_testbed_for_bucket(self, bucket: int):
        """
        Runs the scenarios in the chosen bucket.

        Just passes the results through.
        """
        results = []
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):
            results.append(self.run_timed_testbed(start, goal, map_data, diag_cost))
            print(f"{scenario_id} done.")
        return results



    def start_fringe_thread(self, bucket, scenario_index, map_slots, data_slots):
        """
        Runs the fringe version made for the Fringe Tab. It just sends default non-blocking signals now
        from another thread. GUI keeps visited/expanded/status counts used in output.
        """
        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, scenario_index)
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        instanced_thread = FringeThread(self, start, goal, map_data, map_slots, data_slots, diag_cost)
        instanced_thread.finished.connect(instanced_thread.deleteLater)
        instanced_thread.start()

    # A*

    def start_astar_thread(self, bucket: int, scenario_index: int, map_slots: list, data_slots: list) -> None:
        """
        Runs the A* version made for the AstarTab. It just sends default non-blocking signals now
        from another thread. GUI keeps visited/expanded/status counts used in output.

        :param bucket: index of bucket
        :param scenario_index: index of scenario in bucket
        :param map_slots: list of 3 Slots:
        :param data_slots: list of 3 Slots:
        """
        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, scenario_index)
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        instanced_thread = AstarThread(self, start, goal, map_data, map_slots, data_slots, diag_cost)
        instanced_thread.finished.connect(instanced_thread.deleteLater)
        instanced_thread.start()

    @timered
    def run_timed_astar(self, start: tuple[int, int], goal: tuple[int, int], citymap: list, diag_cost: int|float|Decimal) -> tuple:
        """
        Small runner for A* search.
        The decorator should handle timing.

        @param start: (x, y) of start
        @param goal: (x,y) of goal
        @param citymap: map as list, or equivalent
        @param diag_cost: cost of diagonal movement as int/float/decimal

        @return: tuple ()
        """
        return astar(start, goal, citymap, diag_cost)

    def run_astar_for_bucket(self, bucket: int):
        """
        Runs the scenarios in the chosen bucket.

        Just passes the results through.
        """
        results = []
        map_data = self.scenario_service.get_map_data()
        diag_cost = self.scenario_service.get_diag_cost()

        for scenario_id, start, goal in self.scenario_service.get_data_from_bucket(bucket):
            results.append(self.run_timed_astar(start, goal, map_data, diag_cost))
            print(f"{scenario_id} done.")
        return results


    # LOGGING

    def run_fringe_with_logging(self, bucket, scenario, logger=None):
        """
        runs fringe with logging enabled.

        There will be messages for visited, expanded, over flimit, found, etc.

        """
        fringe_search_with_logging(*self.scenario_service.get_scenario_start_and_goal(bucket, scenario), self.scenario_service.get_map_data(), self.scenario_service.get_diag_cost(), bucket, scenario, logger)


