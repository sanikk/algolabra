class SearchService:
    def __init__(self):
        self.chosen_map = None
        self.astar_time = None
        self.fringe_time = None

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

    def get_chosen_map(self):
        return self.chosen_map

    def set_chosen_map(self, new_map):
        self.chosen_map = new_map

    def get_astar_time(self):
        return self.astar_time

    def get_fringe_time(self):
        return self.fringe_time