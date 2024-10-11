from algolabra.fringe.timed_fringe import timed_fringe_search
from algolabra.fringe.fringe_with_signals import FringeSearch
from algolabra.astar.astar import astar


class SearchService:
    def __init__(self, tilesize=8):
        self.tilesize = tilesize

        self.astar_time = None
        self.fringe_time = None

        self.fringe = FringeSearch()

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
