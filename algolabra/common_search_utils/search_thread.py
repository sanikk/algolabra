from PyQt6.QtCore import QThread, QObject
from algolabra.ui.search_signals import SearchSignals


class SearchThread(QThread):
    """
    Simple QThread wrapper class for a search.
    """
    def __init__(self, parent: QObject, start: tuple[int, int], goal: tuple[int, int], citymap: list, scene_slots: list, data_slots: list):
        """

        :param parent: parent of QThread.
        :param start: start node
        :param goal: goal node
        :param citymap: map as list of lists
        :param scene_slots: QtSlots from MapScene
        :param data_slots: QtSlots from SearchTab
        """
        super().__init__(parent)
        self.signals = SearchSignals()
        self.connect_slots(scene_slots, data_slots)

        self.start_node = start
        self.goal_node = goal
        self.citymap = citymap

    def connect_slots(self, scene_slots, data_slots):
        """
        Connects Signals placed in the search to Slots in the GUI.

        :param scene_slots: QtSlots from MapScene
        :param data_slots:  QtSlots from a SearchTab
        :return: None
        """
        self.signals.node_visited.connect(scene_slots[0])
        self.signals.node_visited.connect(data_slots[0])
        self.signals.node_expanded.connect(scene_slots[1])
        self.signals.node_expanded.connect(data_slots[1])
        self.signals.flimit_set.connect(scene_slots[2])
        self.signals.flimit_set.connect(data_slots[2])

    def run(self):
        """
        Overrides the method from QThread. Implement this in subclass.
        :return:
        """
        pass