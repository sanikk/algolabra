class SearchService:
    def __init__(self):
        self.chosen_map = None
        pass

    def time_fringe(self):
        pass

    def time_astar(self):
        pass

    def playbyplay_fringe(self):
        pass

    def playbyplay_aster(self):
        pass

    def get_chosen_map(self):
        return self.chosen_map

    def set_chosen_map(self, new_map):
        self.chosen_map = new_map