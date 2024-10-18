from PyQt6.QtCore import QThread

class SearchThread(QThread):
    """
    Version for livetab. I try to send signals live,
    but my available hardware is limited at the moment.

    So to make ok demo I have a lighter version too.
    """
    def __init__(self, parent, start, goal, citymap, signals, scene_slots, data_slots):
        super().__init__(parent)
        self.signals = signals
        self.connect_slots(scene_slots, data_slots)

        self.start_node = start
        self.goal_node = goal
        self.citymap = citymap

    def connect_slots(self, scene_slots, data_slots):
        self.signals.node_visited.connect(scene_slots[0])
        self.signals.node_visited.connect(data_slots[0])
        self.signals.node_expanded.connect(scene_slots[1])
        self.signals.node_expanded.connect(data_slots[1])
        self.signals.flimit_set.connect(scene_slots[2])
        self.signals.flimit_set.connect(data_slots[2])

    def run(self):
        pass