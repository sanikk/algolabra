from PyQt6.QtCore import QThread, pyqtSignal, QObject, Qt, pyqtSlot

from algolabra.fringe.timed_fringe import timed_fringe_search
from algolabra.fringe.fringe_with_signals import FringeSearch
from algolabra.astar.astar import astar


class SearchService(QObject):

    operate = pyqtSignal()

    def __init__(self, scenario_service=None, tilesize=8):
        super().__init__()
        self.tilesize = tilesize
        self.scenario_service = scenario_service

        self.astar_time = None
        self.fringe_time = None

        self.worker_thread = QThread()
        self.fringe_connections = None

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

    def playbyplay_fringe(self, bucket, index):
        print("playbyplay_fringe")

        start, goal = self.scenario_service.get_scenario_start_and_goal(bucket, index)
        print(f"playbyplay {start=}, {goal=}")
        map_data = self.scenario_service.get_map_data()
        self.run_fringe_in_another_thread(start, goal, map_data)
        # self.search_service.playbyplay_fringe(scenario[2], scenario[3], self.map_list)
        # self.fringe_search(start, goal, citymap)

    def run_timed_astar(self, bucket):
        new_time = "123.456"
        self.astar_time = new_time
        return new_time


    def playbyplay_astar(self, start, goal, citymap):
        pass

    def get_astar_time(self):
        return self.astar_time

    def get_fringe_time(self):
        return self.fringe_time

    def run_fringe_in_another_thread(self, start, goal, citymap, connections=None):
        worker = FringeSearch(start, goal, citymap, connections)

        self.worker_thread.finished.connect(worker.deleteLater)

        # self.connect_fringe_worker(worker)
        self.operate.connect(worker.do_search)
        worker.result_ready.connect(self.handle_results)
        # flimit_change, node_visit, node_expansion = self.fringe_connections
        # worker.flimit_set.connect(flimit_change)
        # worker.node_visited.connect(node_visit, type=Qt.ConnectionType.BlockingQueuedConnection)
        # worker.node_visited.connect(node_visit, type=Qt.ConnectionType.QueuedConnection)
        # worker.node_expanded.connect(node_expansion, type=Qt.ConnectionType.BlockingQueuedConnection)
        # worker.node_visited.connect(node_visit, type=Qt.ConnectionType.QueuedConnection)

        worker.moveToThread(self.worker_thread)
        # self.worker_thread.start(QThread.Priority.LowestPriority)
        self.worker_thread.start()
        self.operate.emit()

    @pyqtSlot()
    def handle_results(self):
        print("handling results...done")



