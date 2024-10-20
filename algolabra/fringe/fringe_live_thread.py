from decimal import Decimal, getcontext, FloatOperation, Inexact, Rounded
from PyQt6.QtCore import QThread

from algolabra.fringe.doublelinkedlist import Node, DoubleLinkedList
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children

from algolabra.ui.mysignals import FringeSignals


class FringeLiveThread(QThread):
    """
    Version for livetab. I try to send signals live,
    but my available hardware is limited at the moment.

    So to make ok demo I have a lighter version too.
    """
    def __init__(self, parent, start, goal, citymap, scene_slots, data_slots):
        super().__init__(parent)

        self.signals = FringeSignals()
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
        self.fringe_search(self.start_node, self.goal_node, self.citymap)

    def fringe_search(self, start: tuple[int, int], goal: tuple[int, int], citymap: list):
        """
        Implementation for octile maps. No extra data collection or status prints.
        :param start: starting point (x, y)
        :param goal:  goal point (x, y)
        :param citymap:  map
        :return: cost and route if available
        """
        diag_cost = Decimal('1.4142135623730950488')
        fmax = 10000000
        start_node = Node(*start, None, None)
        fringe = DoubleLinkedList(node=start_node)
        cache = [[None for a in line] for line in citymap]

        cache[start_node.y][start_node.x] = 0, None
        flimit = heuristics(start_node, *goal, diag_cost)
        ############
        self.signals.flimit_set.emit(str(flimit))
        ############
        found = False
        found_cost = 0

        while not found and fringe.head:
            fmin = fmax
            for node in fringe:
                ############
                self.signals.node_visited.emit(node.x, node.y)
                g, parent = cache[node.y][node.x]
                f = g + heuristics(node, *goal, diag_cost)
                if f > flimit:
                    fmin = min(f, fmin)
                    continue
                if node.x == goal[0] and node.y == goal[1]:
                    print(f"Rounded: {getcontext().flags[Rounded]}, Inexact: {getcontext().flags[Inexact]}")
                    print(f"Found route with cost {g}")
                    self.signals.result_ready.emit(g)
                    found = True
                    found_cost = g
                    break

                ############
                self.signals.node_expanded.emit(node.x, node.y)
                for x, y, cost in children(node, citymap, diag_cost):
                    g_child = g + cost
                    if cache[y][x]:
                        g_cached, parent = cache[y][x]
                        if g_child >= g_cached:
                            continue
                    fringe.add_child(x, y, node)
                    cache[y][x] = g_child, (node.x, node.y)
                fringe.remove_node(node)
            if not found:
                flimit = fmin
                self.signals.flimit_set.emit(str(flimit))
                # print(f"  {flimit=}, {expanded=}, {visited=}")
        if found:
            route = [goal]
            while route[-1] != start:
                x,y = route[-1]
                route.append(cache[y][x][1])
            return found_cost, route
