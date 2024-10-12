from decimal import Decimal
from PyQt6.QtCore import QThread

from algolabra.fringe.doublelinkedlist import Node, DoubleLinkedList
from algolabra.common_search_utils.heuristics import heuristics
from algolabra.common_search_utils.children import children

from algolabra.ui.mysignals import FringeSignals
from algolabra.common_search_utils.timed_search import timed_search

class FringeThread(QThread):
    def __init__(self, parent, start, goal, citymap, map_slots, data_slots):
        super().__init__(parent)
        self.signals = FringeSignals()
        self.start_node = start
        self.goal_node = goal
        self.citymap = citymap

        print(f"fringe_thread {data_slots=}")

        self.signals.node_visited.connect(map_slots[0])
        self.signals.node_visited.connect(data_slots[0])
        self.signals.node_expanded.connect(map_slots[1])
        self.signals.node_expanded.connect(data_slots[1])
        self.signals.flimit_set.connect(map_slots[2])
        self.signals.flimit_set.connect(data_slots[2])

    def run(self):
        cost, timers, route = timed_search(self.fringe_search, self.start_node, self.goal_node, self.citymap)
        print(timers)


    def fringe_search(self, start: tuple[int, int], goal: tuple[int, int], citymap: list):
        """
        Implementation for octile maps. No extra data collection or status prints.
        :param start: starting point (x, y)
        :param goal:  goal point (x, y)
        :param citymap:  map
        :return: cost and route if available
        """
        diag_cost = Decimal(2).sqrt()
        start_node = Node(*start)
        fringe = DoubleLinkedList(node=start_node)
        cache = [[None for a in line] for line in citymap]

        cache[start_node.y][start_node.x] = Decimal(0), None
        flimit = heuristics(start_node, *goal, diag_cost)
        # print(f"{type(flimit)=}")
        ############
        self.signals.flimit_set.emit(str(flimit))
        expanded = 0
        visited = 0
        ############
        found = False
        found_cost = Decimal(0)

        while not found and fringe.head:
            fmin = Decimal(1000000)
            for node in fringe:
                ############
                self.signals.node_visited.emit(node.x, node.y)
                visited += 1
                ############
                g, parent = cache[node.y][node.x]
                f = g + heuristics(node, *goal, diag_cost)
                if f > flimit:
                    fmin = min(f, fmin)
                    continue
                if node.x == goal[0] and node.y == goal[1]:
                    print(f"Found route with cost {g}")
                    print(f"{expanded=}, {visited=}")
                    self.signals.result_ready.emit(g)
                    found = True
                    found_cost = g
                    break

                ############
                self.signals.node_expanded.emit(node.x, node.y)
                expanded += 1
                ############
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
                # flimit = fmin
                # add a bit of the magic sauce
                flimit = fmin + Decimal(0.00001)
                # print(f"{type(flimit)=}")
                ############
                self.signals.flimit_set.emit(str(flimit))
                print(f"{flimit=}, {expanded=}, {visited=}")
                ############
        if found:
            route = [goal]
            while route[-1] != start:
                x,y = route[-1]
                route.append(cache[y][x][1])
            return found_cost, route

