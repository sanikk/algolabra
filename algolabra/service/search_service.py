from PyQt6.QtCore import QThread, pyqtSignal, QObject

from algolabra.fringe.timed_fringe import timed_fringe_search
from algolabra.fringe.fringe_with_signals import FringeSearch
from algolabra.astar.astar import astar


class SearchService(QObject):

    operate = pyqtSignal()

    def __init__(self, tilesize=8):
        super().__init__()
        self.tilesize = tilesize

        self.astar_time = None
        self.fringe_time = None

        self.worker_thread = QThread()
        self.fringe_connections = None

    # SEARCH ALGO METHODS

    def run_timed_fringe(self, start, goal, citymap):
        cost, timers, route = timed_fringe_search(start, goal, citymap)
        self.fringe_time = timers
        return [cost, *timers]

    def run_timed_astar(self):
        new_time = "123.456"
        self.astar_time = new_time
        return new_time

    def playbyplay_fringe(self, start, goal, citymap):

        self.fringe.fringe_search(start, goal, citymap)
        pass

    def playbyplay_astar(self, start, goal, citymap):
        pass

    def get_astar_time(self):
        return self.astar_time

    def get_fringe_time(self):
        return self.fringe_time

#################################################################
# class Worker(QObject):
#
#     Q_OBJECT
# public slots
#     def doWork(parameter):
#         result = QString()
#         /* ... here is the expensive or blocking operation ... */
#         resultReady.emit(result)
#
# signals
#    def resultReady(result):
########################################################################
# class Controller(QObject):
#
#     Q_OBJECT
#     workerThread = QThread()
# public
#     Controller() {
#         worker = Worker()
#         worker.moveToThread(workerThread)
#         workerThread.finished.connect(worker.deleteLater)
#         self.operate.connect(worker.doWork)
#         worker.resultReady.connect(self.handleResults)
#         workerThread.start()
    def run_fringe_in_another_thread(self, start, goal, citymap, connections=None):
        worker = FringeSearch(start, goal, citymap, connections)

        self.worker_thread.finished.connect(worker.deleteLater)

        self.connect_fringe_worker(worker)

        worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.operate.emit()

    def connect_fringe_worker(self, worker):
        self.operate.connect(worker.do_search)
        worker.result_ready.connect(self.handle_results)
        flimit_change, node_visit, node_expansion = self.fringe_connections
        worker.flimit_set.connect(flimit_change)
        worker.node_visited.connect(node_visit)
        worker.node_expanded.connect(node_expansion)

        # self.scenario_service.upload_fringe_connections = [self.flimit_change, self.node_visit, self.node_expansion]


    def handle_results(self):
        print("handling results...done")

    def get_fringe_connections(self, fringe_connections):
        print(f"search_service get_fringe_connections {fringe_connections=}")
        self.fringe_connections = fringe_connections
#    ~Controller() {
#        workerThread.quit()
#        workerThread.wait()
#
# public slots
#    def handleResults():
# signals
#    def operate():